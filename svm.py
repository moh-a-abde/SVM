# -*- coding: utf-8 -*-
"""SVM.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1wPR5rrZRQLAK0Fk67eK-vg9fwJoATF5H
"""

#this function will input preprocessed encoded, complete, fully numerica data and send through a SVM

#for more information about SVM:
#SVM for imbalanced data classification:
#https://machinelearningmastery.com/cost-sensitive-svm-for-imbalanced-classification/
#Support Vector Machines for Machine Learning:
#https://machinelearningmastery.com/support-vector-machines-for-machine-learning/
#A tutorial on support Vector Machines for Pattern Recognition (PDF)
#http://research.microsoft.com/en-us/um/people/cburges/papers/svmtutorial.pdf
#Support Vector Machines from the SCIKIT Learn Documentation
#https://scikit-learn.org/stable/modules/svm.html
#https://www.analyticsvidhya.com/blog/2017/09/understaing-support-vector-machine-example-code/

#import libraries
import time
import os

import numpy as np
from numpy.random import randn
import pandas as pd

import math
from math import sqrt

import matplotlib.pyplot as plt
from matplotlib import pyplot
import seaborn as sns


import sklearn.preprocessing
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.metrics import accuracy_score, precision_score, f1_score, recall_score, multilabel_confusion_matrix
from sklearn.metrics import classification_report, mean_squared_error, confusion_matrix, balanced_accuracy_score
from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier, OneVsOneClassifier

#read the preprocessed data file
data = pd.read_csv('/content/Sensor_Final_Pre.csv')

#check data dimensions
data.shape

data.head()

#determine the features (X) and the labels to classify (y)
X = data.drop(['label'], axis = 1).values # X are features
y = data['label'].values                  # Y is the label (what we are classifying)

# This get the RAPIDS-Colab install files and test check your GPU.  Run this and the next cell only.
# Please read the output of this cell.  If your Colab Instance is not RAPIDS compatible, it will warn you and give you remediation steps.
!git clone https://github.com/rapidsai/rapidsai-csp-utils.git
!python rapidsai-csp-utils/colab/pip-install.py

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import cuml
from cuml.svm import SVC as cuSVC
import time

# Assuming you have a GPU setup and CUDA installed

# split data into training and remaining (validation + testing)
# first split (80% training, 20% remaining)
X_train, X_remaining, y_train, y_remaining = train_test_split(X, y, test_size=0.20)

# split the remaining data into validation and testing
# second split (50% of remaining for validation, 50% for testing)
X_val, X_test, y_val, y_test = train_test_split(X_remaining, y_remaining, test_size=0.50)

# normalize the data
sc = MinMaxScaler()
X_train = sc.fit_transform(X_train)
X_val = sc.transform(X_val)  # note: use transform, not fit_transform
X_test = sc.transform(X_test)  # note: use transform, not fit_transform

# start train time
startTrainTime = time.time()

# fit GPU-accelerated SVM to the training set
classifier = cuSVC(kernel='rbf', C=10, gamma=0.01)
classifier.fit(X_train, y_train)

# end train time
TrainTime = (time.time() - startTrainTime)

# start test time
startTestTime = time.time()

# test model on validation set
y_val_pred = classifier.predict(X_val)

# end validation time
ValTime = (time.time() - startTestTime)

# start test time for test set
startTestTime = time.time()

# test model on test set
y_test_pred = classifier.predict(X_test)

# end test time
TestTime = (time.time() - startTestTime)

# Calculate metrics
precision = precision_score(y_test, y_test_pred, average='macro')
bal_accuracy = balanced_accuracy_score(y_test, y_test_pred)
f1 = f1_score(y_test, y_test_pred, average='macro')
recall = recall_score(y_test, y_test_pred, average='macro')
MeanSq = sqrt(mean_squared_error(y_test, y_test_pred))

# Print training and testing times
print('Train time in seconds: ', TrainTime)
print('Validation prediction time in seconds: ', ValTime)
print('Test time in seconds: ', TestTime)

# Print metrics
print('Balanced Accuracy: ', bal_accuracy * 100.00)
print('Precision: ', precision * 100.00)
print('F1: ', f1 * 100.00)
print('Recall: ', recall * 100.00)
print('RMSE: ', MeanSq)

print(classification_report(y_test, y_test_pred, digits=4))

#see how many unique labels
label = (data['label']).unique()
print(label)

#data visualization
#plots the distribution of the labels from our data
zero = (data['label'] == 0).sum()
print(zero)
one = (data['label'] == 1).sum()
print(one)
two = (data['label'] == 2).sum()
print(two)

#Data to plot for label column
labels = 'Benign', 'DDOS', 'PortScan'
sizes = [zero, one, two]

# Plot
plt.pie(sizes, labels=labels,
autopct='%1.1f%%', shadow=True, startangle=140)
plt.axis('equal')
plt.show()