from flask import Flask, request, render_template, redirect
from test import *
from buildings import *
from rform import *
from ratingform import *
from sentiment import *
from flask import jsonify
from jinja2 import Template
import os
from zipreport import *
SECRET_KEY = os.urandom(32)
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route("/",methods = ['GET'])
def home():
    return render_template('home.html')

@app.route("/sentiment/",methods=['GET','POST'])
def sentiment():
    script,div = sentiment_viz()
    return render_template('sentiment.html',script=script,div=div)

#article ranking
@app.route("/rating/", methods = ['GET'])
def rating_get():
     form = RatingForm(request.form)
     train = pd.read_csv('/home/ec2-user/efs-mnt/data/train_data.csv', sep=',',names = ['index','text_out'], encoding='utf')
     sample = train.sample()
     extract = str(sample['text_out'].values)
     index = str(sample['index'].values)
     extractdef = index+extract       
     form.extracttext.default = extractdef
     form.process()
     return render_template('rating.html', form=form)

@app.route("/rating/", methods = ['POST'])
def rating_post():
     form=RatingForm(request.form)
     likert = request.form['rating']
     extract = request.form['extracttext']
     out_df = pd.DataFrame({'extract':[extract],'rating':[likert]})
     out_df.to_csv('/home/ec2-user/efs-mnt/data/train_data_rating.csv',mode='a',header=False)
     return redirect(request.url)
# Home page
@app.route("/zip/", methods=['GET', 'POST'])
def ziphome():
    """Home page of app with form"""
    # Create form
    form = ReusableForm()
    # On form entry and all conditions met

    if form.validate_on_submit():
            # Extract information
        zipcode = request.form['zipcode']
        input,script,div=get_report(zipcode=zipcode)
        return render_template('report.html', 
                               input=input,script=script,div=div)
    elif form.validate()==False:
        print("")
    # Send template information to index.html
    return render_template('index.html', form=form)
@app.route('/api/addresses/', methods=['GET'])
def addresses():
    reqargs = request.args.to_dict()
    zipcode = reqargs['zipcode']
    state = reqargs['state']
    results = get_address(zipcode,state)
    return jsonify(results)
@app.route('/api/buildings/',methods=['GET'])
def buildings():
   reqargs = request.args.to_dict()
   zipcode = reqargs['zipcode']
   results = get_buildings(zipcode)
   return jsonify(results)


if __name__ == '__main__':  
    app.run(host='0.0.0.0',debug=True)

#https://stackoverflow.com/questions/45583828/python-flask-not-updating-images

@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response
