# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 11:49:55 2015

@author: Adithya
"""
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.grid_search import GridSearchCV
from temporalPivot import playByPlay

pbp = playByPlay()
pbp.select("CAR",2015)
preppedData = pbp.temporal(20)

def svmModel(data):
    clf = SVC()
    parameters = {'kernel':['linear', 'poly', 'rbf', 'sigmoid'],
                  'C':[0.1,1,10],
                  'degree':[2,3,4]}
                  
    gs = GridSearchCV(clf,parameters)
    gs.fit(data['train'],data['label'])
    
    print "The best parameter set:"
    gs.best_params_
    
    print "Classification report:"
    y_true, y_pred = data['label'], gs.predict(data['train'])
    print classification_report(y_true,y_pred)
    

svmModel(preppedData)