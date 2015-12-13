import pickle
from sknn.mlp import Classifier, Layer
from sklearn.pipeline import Pipeline
from temporalPivot import playByPlay
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report

pbp = playByPlay()	#instantiate object
pbp.select("CAR", 2015)	#select team and year, this is done in place 
preppedData = pbp.temporal(20)		#this will return the training and test data
									#as dict preppedData['train'], preppedData['label']


def neuralCombo(data):
	pipeline = Pipeline([
        ('min/max scaler', MinMaxScaler(feature_range=(0.0, 1.0))),
        ('nn', Classifier(layers=[
        	Layer("Rectifier", units=100),
        	Layer("Sigmoid", units=100),
        	Layer("Softmax")], 
        	n_iter=25))])

	grid = [		#left maxout out
		{'nn__learning_rate':[0.05, 0.01, 0.005, 0.001, 0.0001, 0.00001],
			'nn__hidden0__units': [4, 8, 10, 50, 100, 200], 
			'nn__hidden0__type':['Rectifier', 'Sigmoid', 'Sigmoid', 
						'Tanh', 'ExpLin', 'Linear', 'Softmax', 'Gaussian'],
			'nn__hidden1__units': [4, 8, 10, 50, 100, 200], 
			'nn__hidden1__type':['Rectifier', 'Sigmoid', 'Sigmoid', 
						'Tanh', 'ExpLin', 'Linear', 'Softmax', 'Gaussian'],			
		}
	]

	gs = GridSearchCV(pipeline, param_grid=grid)
	gs.fit(data['train'], data['label'])

	print "Best parameters set found on development set:"
	print gs.best_params_ 
	print("Grid scores on development set:")
	for params, mean_score, scores in gs.grid_scores_:
		print("%0.3f (+/-%0.03f) for %r"
              % (mean_score, scores.std() * 2, params))
	print("Detailed classification report:")
	print("The scores are computed on the full evaluation set.")
	y_true, y_pred = y_test, gs.predict(data['train'])
	print(classification_report(y_true, y_pred))

	with open('gs_data.pk1', 'wb') as output:
		pickle.dump(gs, output, pickle.HIGHEST_PROTOCOL)

neuralCombo(preppedData)


# pipeline = Pipeline([
#         ('min/max scaler', MinMaxScaler(feature_range=(0.0, 1.0))),
#         ('neural network', Classifier(layers=[
#         	Layer("Rectifier", units=100),
#         	Layer("Sigmoid", units=100),
#         	Layer("Maxout", units=100, pieces=2),
#         	Layer("Softmax")], 
#         	n_iter=25))])

#pipeline.fit(preppedData['train'], preppedData['label'])

# print(preppedData['train'])
# print(preppedData['label'])

# prediction = pipeline.predict(preppedData['train'])

# print prediction

# results = accuracy_score(preppedData['label'], prediction)

# print results