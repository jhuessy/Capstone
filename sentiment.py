def sentiment_viz():
    #Imports
    import mysql.connector
    import sqlalchemy as db
    import pandas as pd 
    from bokeh.plotting import figure, output_file, show
    from bokeh.models.widgets import DateRangeSlider,TextInput,Dropdown
    from bokeh.models.widgets.inputs import AutocompleteInput
    from bokeh.models import Panel, Tabs
    from bokeh.layouts import column
    from bokeh.embed import components
    import numpy as np
    import datetime
    #query mysql for article data and aggregate by day
    con = db.create_engine('mysql+mysqlconnector://*******************')
    df = pd.read_sql('SELECT * FROM articles', con=con)
    df['publishedAt'] = pd.to_datetime(df['publishedAt'])
    df['date_only']=df['publishedAt'].apply(lambda x: x.date())
    dailycounts=df.groupby(by='date_only').agg({'preds':['count','mean']})
    dailycounts.columns=['volume','sentiment_net']
    dailycounts['date'] = dailycounts.index
    publist = df['source_name'].unique().tolist() 
    pollist = [] #pd.read_sql('SELECT * FROM politicians',con=con)
    
    #Sentiment Valence Chart
    pnet = figure(plot_width=1000, plot_height=300, x_axis_type='datetime')
    pnet.toolbar.logo = None
    pnet.toolbar_location = None
    pnet.background_fill_color = "lavender"
    #News Volume Chart
    pvol = figure(plot_width=1000, plot_height=100, x_axis_type='datetime')
    pvol.toolbar.logo = None
    pvol.toolbar_location = None
    pvol.background_fill_color = "bisque"

   #Render data lines
    pnet.line(dailycounts['date'], 
       dailycounts['sentiment_net'], 
       line_width=2,
      color='purple')
    pvol.line(dailycounts['date'], 
       dailycounts['volume'], 
       line_width=2,color='orange')
    #Menu objects
    polmenu = AutocompleteInput(completions=pollist,title='Politician (case sensitive)')
    pubmenu = AutocompleteInput(completions=publist,title='Publication (case sensitive)')
    date_slider = DateRangeSlider(start=min(dailycounts['date']), end=max(dailycounts['date']), 
                          value=(min(dailycounts['date']),max(dailycounts['date'])), step=1, title="Date Range")
    #create components to be rendered in html
    script,div = components(column(pnet,pvol,polmenu,pubmenu,date_slider))
    print(dailycounts.head())
    return script,div

