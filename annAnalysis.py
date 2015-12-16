import pickle
import math
from sknn.mlp import Classifier, Layer
from sknn import ae
from sklearn.pipeline import Pipeline
from temporalPivot import playByPlay
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report



pbp = playByPlay()	#instantiate object
pbp.select("CAR", 2014)	#select team and year, this is done in place 
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

	learningRate = [0.05, 0.005, 0.001, 0.0001, 0.00001]
	units = [5, 50, 100, 200]
	type = ['Rectifier', 'Sigmoid', 'Sigmoid', 'Tanh', 'Linear', 'Softmax', 'Gaussian']
	#type = ['Rectifier', 'Linear', 'Gaussian']
	iterations=[25, 50, 100, 200]

	best = {}
	best['learningRate'] = 0.05
	best['units'] = 4
	best['type'] = 'Rectifier'
	best['iterations'] = 5
	best['trainingAccuracy'] = 0.0

	for l in learningRate:
		for i in iterations:
			for type0 in type:
				for u0 in units:

					pipeline = Pipeline([
			        ('min/max scaler', MinMaxScaler(feature_range=(0.0, 1.0))),
			        ('nn', Classifier(layers=[
			        	Layer(type0, units=u0),
			        	Layer("Softmax")], 
			        	n_iter=i))])

					best = testModel(data, pipeline, best, l, u0, type0, i)

					for type1 in type:
						for u1 in units:
							
							pipeline = Pipeline([
					        ('min/max scaler', MinMaxScaler(feature_range=(0.0, 1.0))),
					        ('nn', Classifier(layers=[
					        	Layer(type0, units=u0),
					        	Layer(type1, units=u1),
					        	Layer("Softmax")], 
					        	n_iter=i))])

							best = testModel(data, pipeline, best, l, str(u0) +","+ str(u1), type0+","+type1, i)

							for type2 in type:
								for u2 in units:
									
									pipeline = Pipeline([
							        ('min/max scaler', MinMaxScaler(feature_range=(0.0, 1.0))),
							        ('nn', Classifier(layers=[
							        	Layer(type0, units=u0),
							        	Layer(type1, units=u1),
							        	Layer(type2, units=u2),
							        	Layer("Softmax")], 
							        	n_iter=i))])

									best = testModel(data, pipeline, best, l, str(u0) +","+ str(u1) + ","+str(u2), type0+","+type1+","+type2, i)

	print "bestOverall===================================="
	print "trainingAccuracy" + " = "  + str(best['trainingAccuracy'])
	print "learningRate" + " = "  + str(best['units'])
	print "units" + " = "  + str(best['type'])
	print "type" + " = "  + str(best['iterations'])
	print "iterations" + " = "  + str(best['learningRate'])

def testModel(data, model, b, l, u, t, i ):

	model.fit(data['train'], data['label'])
	prediction = model.predict(data['train'])
	results = accuracy_score(data['label'], prediction)

	print "trainingAccuracy" + " = "  + str(results)
	print "learningRate" + " = "  + str(l)
	print "units" + " = "  + str(u)
	print "type" + " = "  + str(t)
	print "iterations" + " = "  + str(i)

	if results > b['trainingAccuracy']:
		b['trainingAccuracy'] = results
		b['learningRate'] = l
		b['units'] = u
		b['type'] = t
		b['iterations'] = i

	return b

def autoEncoderOptimization(data):
	rbm = ae.AutoEncoder(
			layers=[
				ae.Layer("Tanh", units=300),
				ae.Layer("Sigmoid", units=200),
				ae.Layer("Tanh", units=100)
			],
			learning_rate=0.002,
			n_iter=10
		)

	rbm.fit(data["train"])

	model = Classifier(
			layers=[
				Layer("Tanh", units=300),
				Layer("Sigmoid", units=200),
				Layer("Tanh", units=100),
				Layer("Rectifier", units=100),
				Layer("Rectifier", units=50),
				Layer("Softmax")
			],
		)

	rbm.transfer(model)

	model.fit(data["train"], data["label"])

	prediction = model.predict(data["train"])

	print accuracy_score(data["label"], prediction)

def testRunner():
	for y in [2013]:
		pipeline = Pipeline([
	        ('min/max scaler', MinMaxScaler(feature_range=(0.0, 1.0))),
	        ('neural network', Classifier(layers=[
	        	Layer("Rectifier", units=200),
	        	Layer("Gaussian", units=200),
	        	#Layer("Maxout", units=100, pieces=2),
	        	Layer("Softmax")],
	        learning_rate=0.001, 
	        n_iter=25))])
		print "YEAR ====" + str(y)
		pbp.testingFrameworkByTeam(pipeline, y, 9, 0.6)

def temporalTest():
	pipeline = Pipeline([
        ('min/max scaler', MinMaxScaler(feature_range=(0.0, 1.0))),
        ('neural network', Classifier(layers=[
        	Layer("Rectifier", units=200),
        	Layer("Gaussian", units=200),
        	#Layer("Maxout", units=100, pieces=2),
        	Layer("Softmax")],
        learning_rate=0.001, 
        n_iter=25))])
	pbp.temporalLengthOptimization(pipeline)

def unitSizeAnalysis(data):

	units = range(3,35) + [200, 300, 400, 500, 600, 700, 800, 900]

	validationSplit = 0.6

	split = math.floor(len(data['label']) * validationSplit)

	trainingSplit = {'train': data['train'][:split], 'label': data['label'][:split]}
	testingSplit = {'train': data['train'][split:], 'label': data['label'][split:]}

	for i in units:	
		pipeline = Pipeline([
	        ('min/max scaler', MinMaxScaler(feature_range=(0.0, 1.0))),
	        ('neural network', Classifier(layers=[
	        	Layer("Rectifier", units=i),
	        	Layer("Gaussian", units=i),
	        	#Layer("Maxout", units=100, pieces=2),
	        	Layer("Softmax")],
	        learning_rate=0.001, 
	        n_iter=25))])

		pipeline.fit(trainingSplit['train'], trainingSplit['label'])
		testAcc = accuracy_score(testingSplit['label'], pipeline.predict(testingSplit['train']))
		trainingAcc = accuracy_score(trainingSplit['label'], pipeline.predict(trainingSplit['train']))

		print str(i) + "," + str(testAcc) + "," + str(trainingAcc)


#temporalTest()
#unitSizeAnalysis(preppedData)
testRunner()
#pbp.test()


#neuralCombo(preppedData)
#autoEncoderOptimization(preppedData)



	# grid = [		#left maxout out
	# 	{'nn__learning_rate':[0.05, 0.01, 0.005, 0.001, 0.0001, 0.00001],
	# 		'nn__hidden0__units': [4, 8, 10, 50, 100, 200], 
	# 		'nn__hidden0__type':['Rectifier', 'Sigmoid', 'Sigmoid', 
	# 					'Tanh', 'ExpLin', 'Linear', 'Softmax', 'Gaussian'],
	# 		'nn__hidden1__units': [4, 8, 10, 50, 100, 200], 
	# 		'nn__hidden1__type':['Rectifier', 'Sigmoid', 'Sigmoid', 
	# 					'Tanh', 'ExpLin', 'Linear', 'Softmax', 'Gaussian'],			
	# 	}
	# ]

	# gs = GridSearchCV(pipeline, param_grid=grid)
	# gs.fit(data['train'], data['label'])

	# print "Best parameters set found on development set:"
	# print gs.best_params_ 
	# print("Grid scores on development set:")
	# for params, mean_score, scores in gs.grid_scores_:
	# 	print("%0.3f (+/-%0.03f) for %r"
 #              % (mean_score, scores.std() * 2, params))
	# print("Detailed classification report:")
	# print("The scores are computed on the full evaluation set.")
	# y_true, y_pred = y_test, gs.predict(data['train'])
	# print(classification_report(y_true, y_pred))

	# with open('gs_data.pk1', 'wb') as output:
	# 	pickle.dump(gs, output, pickle.HIGHEST_PROTOCOL)




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