from sknn.mlp import Classifier, Layer
from sklearn.pipeline import Pipeline
from temporalPivot import playByPlay
from sklearn.preprocessing import MinMaxScaler

pbp = playByPlay()	#instantiate object
pbp.select("CAR", 2015)	#select team and year, this is done in place 
preppedData = pbp.temporal(20)		#this will return the training and test data
									#as dict preppedData['train'], preppedData['label']


pipeline = Pipeline([
        ('min/max scaler', MinMaxScaler(feature_range=(0.0, 1.0))),
        ('neural network', Classifier(layers=[Layer("Softmax")], n_iter=25))])

pipeline.fit(preppedData['train'], preppedData['label'])

# print(preppedData['train'])
# print(preppedData['label'])

print pipeline.predict(preppedData['train'])