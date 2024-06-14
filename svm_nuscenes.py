# -*- coding: utf-8 -*-
"""SVM nuScenes.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ibXQmXGa_TAvE4GTHQKQxNI6WzktDlrt
"""

# uncomment and run to get nuscenes dataset
#!mkdir -p /data/sets/nuscenes  # Make the directory to store the nuScenes dataset in.

#!wget https://www.nuscenes.org/data/v1.0-mini.tgz  # Download the nuScenes mini split.

#!tar -xf v1.0-mini.tgz -C /data/sets/nuscenes  # Uncompress the nuScenes mini split.

!pip install nuscenes-devkit &> /dev/null  # Install nuScenes.

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
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn import metrics
from sklearn.metrics import accuracy_score, precision_score, f1_score, recall_score, multilabel_confusion_matrix
from sklearn.metrics import classification_report, mean_squared_error, confusion_matrix, balanced_accuracy_score
from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier, OneVsOneClassifier

from google.colab import drive
drive.mount('/content/drive')

##nuSCenes
import numpy as np
from nuscenes.nuscenes import NuScenes
from nuscenes.utils.data_classes import LidarPointCloud
from nuscenes.utils.geometry_utils import transform_matrix
from nuscenes.eval.detection.config import config_factory
from nuscenes.eval.detection.data_classes import DetectionBox
from nuscenes.eval.detection.evaluate import NuScenesEval
from sklearn.metrics import classification_report, accuracy_score

# Load the nuScenes dataset
nusc = NuScenes(version='v1.0-mini', dataroot='/data/sets/nuscenes', verbose=True)

# Initialize lists for features and labels
features = []
labels = []

# Iterate through samples and extract relevant data
for sample in nusc.sample:
    for ann_token in sample['anns']:
        ann = nusc.get('sample_annotation', ann_token)

        # Extract relevant features (e.g., position, dimensions)
        x, y, z = ann['translation']
        length, width, height = ann['size']

        # Append features and corresponding label
        features.append([x, y, z, length, width, height])
        labels.append(ann['category_name'])

# Convert to numpy arrays
features = np.array(features)
labels = np.array(labels)

# Extract unique labels
unique_labels = np.unique(labels)

# Print the unique labels
print(unique_labels)


# Split the data into training (60%) and temporary (40%) sets
X_train, X_temp, y_train, y_temp = train_test_split(features, labels, test_size=0.4, random_state=111)

# Split the temporary set into validation (50% of 40% = 20%) and test (50% of 40% = 20%) sets
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score

# Initialize the SVM model with specified parameters
svm_model = SVC(kernel='rbf', C=10, gamma=0.01, random_state=42)

# Train the SVM model
svm_model.fit(X_train, y_train)

# Validate the model on the validation set
y_val_pred = svm_model.predict(X_val)
print(f"Validation Accuracy: {accuracy_score(y_val, y_val_pred)}")

print(classification_report(y_val, y_val_pred, target_names=unique_labels))

# Make predictions on the test set
y_test_pred = svm_model.predict(X_test)

# Evaluate the model
print(f"Test Accuracy: {accuracy_score(y_test, y_test_pred)}")
print(classification_report(y_test, y_test_pred, target_names=unique_labels))

#k-fold
k = 10
skf = StratifiedKFold(n_splits=k, shuffle=True, random_state=111)
# Perform k-fold cross-validation
scores = cross_val_score(svm_model, features, labels, cv=skf)
# Print the cross-validation scores
print(f"Cross-validation scores: {scores}")
print(f"Mean cross-validation score: {scores-mean}")