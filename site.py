from flask import Flask, request, render_template, redirect
from ratingform import *
from sentiment import *
from flask import jsonify
from jinja2 import Template
import os
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


if __name__ == '__main__':  
    app.run(host='0.0.0.0',debug=True)

@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response
