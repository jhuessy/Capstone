# Capstone: Media Sentiment Analysis
Final Project for General Assembly Data Science Immersive

## Executive Summary
Much of current market for sentiment analysis focuses on social media posts about corporations, brands or intellectual properties.  What if we could apply these same techniques to the way politicians are covered by journalists?  The purpose of this application is to provide users with a near real-time look at media coverage of US politicians on a publically available platform.  Newly published articles are collected on an hourly basis and displayed via interactive charts.  The charts display the volume of relevant articles over time as well the net valence of the articles.  Users can filter the charts by one or more publications and one or more subjects (from a predetermined pool of almost 600 US national politicians).  

## Data Source
Data for this application is collected via [newsapi.org](newsapi.org)

## Methodology
### Data Collection
The list of politicians covered by the application is generated by scraping the wikipedia pages for the President's cabinet, the Senate and the House of representatives to ensure that the list of officeholders is up to date.  This list is then used to determine the scope of the request sent to the [newsapi.org](newsapi.org) API.  The resulting article content and metadata is then loaded into a database for future use.

### Classification
Training data was created using a bootstrapping method, where human coders would rate a small sample of articles, a logistic regression model was constructed using these ratings, and the articles the model classified with the greatest certainty were added to the training data.  The articles the model was least sure about were then manually coded and the process was repeated.

The classification of live data is done using a Random Forest Classifier fit on the training data.  This Classifier had an accuracy of XX on the training data and YY on the test data.


## Infrastructure
The application is hosted on an AWS EC2 instance running Amazon Linux.  The application itself is written in Python and uses Flask, UWSGI and Nginx for web hosting.  Interactive data visualizations are done in Bokeh.  Data is stored in MySQL.

A Dockerized version of the app is available.
