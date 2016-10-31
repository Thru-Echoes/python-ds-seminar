# First Rodeo: Python Computing for Data Science - Oct 14 

import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn import preprocessing
import seaborn as sns
import pandas as pd
import numpy as np
import requests
from io import StringIO

boston = datasets.load_boston() # Boston house-prices
X = boston['data']   # 13 features (e.g. crime, # rooms, age, etc.)
Y = boston['target'] # response (median house price)

sns.set(style="white")
sns.set_context("poster")
df = pd.DataFrame(X,columns=boston.feature_names)
df["target"]  = boston['target']
sns.pairplot(df[['AGE','DIS','RAD','TAX']])

###########################################################################

boston = datasets.load_boston() ; X = boston['data'] ; Y = boston['target']
from sklearn import linear_model
clf = linear_model.LinearRegression()

from sklearn.cross_validation import cross_val_score

def print_cv_score_summary(model, xx, yy, cv):
    scores = cross_val_score(model, xx, yy, cv=cv, n_jobs=1)
    print("mean: {:3f}, stdev: {:3f}".format(
        np.mean(scores), np.std(scores)))

def splitScale(ddat, nPart):
    try:
        from sklearn.model_selection import train_test_split
    except:
        print("Could not import sklearn.cross_validation for train_test_split")
    
    np.random.shuffle(ddat)
    numObs = ddat.shape[0]
    numCol = ddat.shape[1] - 1
    xddat = ddat[:, 1:numCol]
    yddat = ddat[:, numCol]
    
    # remember: many methods work better on scaled X
    xScaled = preprocessing.scale(xddat)
    xTrain, xTest, yTrain, yTest = train_test_split(xScaled, yddat, train_size = nPart, random_state = 1738)
    #xddat.iloc[xTrain] # return dataframe train
    return (xTrain, xTest, yTrain, yTest)
    
    
# Bring in data 
dat_file = requests.get("http://archive.ics.uci.edu/ml/machine-learning-databases/00243/yacht_hydrodynamics.data")
data = StringIO(dat_file.text)
ddat = np.loadtxt(data)
xDat, xTest, yDat, yTest = splitScale(ddat, 0.7)
