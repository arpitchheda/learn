import pandas as pd 
## Download the zip file from http://files.grouplens.org/datasets/movielens/ml-1m.zip
ratings = pd.read_csv('ratings.dat', engine='python',sep='::', names=['userid', 'movieid', 'rating', 'timestamp'])
ratings.to_csv('ratings_pipe.dat',sep='|', header=False,index=False )
