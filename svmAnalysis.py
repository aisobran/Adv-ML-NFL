# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 11:49:55 2015

@author: Adithya
"""
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn import cross_validation
from sklearn.pipeline import Pipeline
from temporalPivot import playByPlay
from sklearn.preprocessing import MinMaxScaler

pbp = playByPlay()
pbp.select("CAR",2014)
preppedData = pbp.temporal(20)


pipeline = Pipeline([('min/max scaler',MinMaxScaler(feature_range=(0.0, 1.0))),
                     ('svm',SVC(kernel='poly',C=100,degree=5))])
print "Classifier created"

print "Train Classification report:"
pipeline.fit(preppedData['train'],preppedData['label'])

y_true, y_pred = preppedData['label'], pipeline.predict(preppedData['train'])
print classification_report(y_true,y_pred)
print accuracy_score(y_true,y_pred)

print "CrossValidation:"
scores = cross_validation.cross_val_score(pipeline,preppedData['train'],preppedData['label'],cv=10)
print scores.mean()

print "Test Classification report:"
pipeline.fit(preppedData['train'][:-300],preppedData['label'][:-300])

y_true, y_pred = preppedData['label'][-300:], pipeline.predict(preppedData['train'][-300:])
print classification_report(y_true,y_pred)
print accuracy_score(y_true,y_pred)


def testRunner():
	pipeline = Pipeline([
        ('min/max scaler', MinMaxScaler(feature_range=(0.0, 1.0))),
        ('svm',SVC(kernel='poly',C=100,degree=2))])
	pbp.testingFrameworkByTeam(pipeline,year=2009,9)

def temporalTest():
	pipeline = Pipeline([
        ('min/max scaler', MinMaxScaler(feature_range=(0.0, 1.0))),
        ('svm',SVC(kernel='poly',C=100,degree=2))])
	pbp.temporalLengthOptimization(pipeline,'NE')


testRunner()
temporalTest()