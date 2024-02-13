# -*- coding: utf-8 -*-
"""Entrega Python DEP17.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DNpFaNV2eLKoIboDdG-34flOFuckVNBT
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
import xgboost as xgb
from lightgbm import LGBMClassifier
import lightgbm as lgb
from sklearn.metrics import accuracy_score, log_loss
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

from sklearn.preprocessing import LabelEncoder

train_data = pd.read_csv('/content/drive/MyDrive/DEP17 AV/Análisis de Datos con Python/train.csv')
test_data = pd.read_csv('/content/drive/MyDrive/DEP17 AV/Análisis de Datos con Python/test.csv')
sample_submission_data = pd.read_csv('/content/drive/MyDrive/DEP17 AV/Análisis de Datos con Python/sample_submission.csv')

train_data.head()

train_data.info()

train_data.isnull().sum()

train_data.shape

train_data.describe()

train_data['Age'].hist( color='r')

train_data['HomePlanet'].value_counts()
sns.countplot(x = 'HomePlanet', hue = 'Transported' ,data = train_data)

for col_name in train_data.columns:
    if train_data[col_name].dtypes=='object':
        train_data[col_name] = train_data[col_name].fillna(train_data[col_name].mode()[0])
    else:
        train_data[col_name] = train_data[col_name].fillna(train_data[col_name].median())
print(train_data.shape)

for col_name in test_data.columns:
    if test_data[col_name].dtypes=='object':
        test_data[col_name] = test_data[col_name].fillna(test_data[col_name].mode()[0])
    else:
        test_data[col_name] = test_data[col_name].fillna(test_data[col_name].median())
print(test_data.shape)

encoder = LabelEncoder()
for col_name in train_data.columns:
    if train_data[col_name].dtypes == 'object':
        train_data[col_name] = encoder.fit_transform(train_data[col_name])

object_columns = test_data.select_dtypes(include='object').columns.difference(['PassengerId'])
encoder = LabelEncoder()
for col_name in object_columns:
    if test_data[col_name].dtype == 'object':
        test_data[col_name] = encoder.fit_transform(test_data[col_name])

plt.figure(figsize=(18,12))
sns.heatmap(train_data.corr(), annot=True, cmap='coolwarm', fmt=".2f")

X_train = train_data.drop(['Transported','PassengerId','Name','ShoppingMall'], axis=1)
y_train = train_data['Transported']
X_test = test_data.drop(['PassengerId','Name','ShoppingMall'], axis=1)

sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

model_XGB = XGBClassifier(learning_rate = 0.1 , max_depth = 4, n_estimators = 100)
model_XGB.fit(X_train, y_train)
XGB_pred = model_XGB.predict(X_test)

submission = pd.DataFrame({
    'PassengerId': test_data.PassengerId,
    'Transported': XGB_pred
})
submission['Transported'] = submission['Transported'].astype(bool)
print(submission.head())

