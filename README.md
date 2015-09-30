#Purpose
The NFL is highly unpredictable, being highly notorious for unexpected results. As a consequence, NFL prediction is a fertile ground for assessing the performance of various machine learning tools. 

The purpose of this project is to explore the effectivess of advanced machine learning techniques using multiple tiers of NFL data. This project proposes machine learning techniques can be used to predict the next play given a series of previous plays, the winner of a game, and the performance of a player in a single game. These predictions could be useful when applied to live play calling strategy, personnel analysis, sports betting, and fantasy football.

This project will also compare various machine learning algorithms and assess their strengths and weaknesses. We also examine the effect of data aggregation as data can be trained on a play level, drive level, quarter level, half level, game level, or season level.


#Data Sets
1. Play by play Data: Consists of summary of each play in each game including, time, down, yards to go, pass/run, distance, current score, as well as other metrics. From 2009-present.
2. NFL Combine data: A set of metrics used to measure the athleticism of players as well as one test the measue mental aptitude.
3. Coach history: Head coach, offensive coordinator, defensive coordinator
4. Rosters: The players that make up a team
5. Weather: Weather of games 
6. Injury History: Football is a contact sport with high frequency of injuries. 

#Algorithms
1. ANNs - Deep Belief, Recurrent, Fuzzy
2. SVMs with Kernel Transformations
3. Reinforcement Learning
4. Ensemble of the above

#Optimizations
1. Gradient Descent
2. Particle Swarm Optimization
3. Simulated Annealing
4. MaxWalkSat
5. Differtiating Evolution

#Study Plan

1. Data aggregation
2. Data pre-processing: Parsing of play by play data, mapping coaches to teams
3. ML Implementation
4. Optimization Implementation
5. Ensemble Implementation
6. Evalutation of models
7. Comperison of performance of different tiers of data

#Testing Validity

1. Accuracy of predicting type of next play(run, pass, punt, field goal), strategic location of next play(left, right, inside, deep, short, middle)
2. Accuracy of predicting play performacne in a game
3. Accuracy of predicting winners
4. Regression accuracy of predicting scores


#Potential Challenges
The size of the dataset is relatively small as each teams plays 16 regular season games and run approximantly 50-60 playes per game. We hope to mitage this issue by training on the historical data going back 6 years. It could be assumed coaches talented enough to earn multi million dollar contracts do not have predictable tendencies as they would be exploited by opposing coaches. 

#References

1. http://www.cs.cornell.edu/courses/cs6780/2010fa/projects/warner_cs6780.pdf
2. http://ttic.uchicago.edu/~kgimpel/papers/machine-learning-project-2006.pdf
