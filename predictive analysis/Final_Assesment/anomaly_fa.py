# -*- coding: utf-8 -*-
"""Anomaly_FA.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1_04-UQ5UxUelhxUx5SGzE0QwtYlI5YAi
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

df=pd.read_csv(r'/content/anomaly_train (1).csv')

df.shape

df.head()

df.isnull().sum()

from sklearn.preprocessing import OneHotEncoder

ohe=OneHotEncoder(drop='first',dtype='int32')

ohe_fit=ohe.fit_transform(df[['Type','Location']])

ohe_fit.toarray().shape

ohe_fit.toarray()
ohe.categories_

df.drop(['Type','Location'],axis=1,inplace=True)

feature_names=ohe.get_feature_names_out().tolist()

df[feature_names]=ohe_fit.toarray()

df.head()

df.drop('TransactionID',axis=1,inplace=True)

df.drop('User',axis=1,inplace=True)

features_taken=['Amount','Time']

X=df[features_taken]

isolationf=IsolationForest(contamination=0.05)

isolationf.fit(X)

y_pred=isolationf.predict(X)

y_pred

df['anomaly_score']=isolationf.decision_function(X)

df['anomaly']=y_pred

df.head()

from sklearn.preprocessing import StandardScaler
ss=StandardScaler()

df[features_taken]=ss.fit_transform(df[features_taken])
anomalies=df[df['anomaly']<0]
plt.scatter(df['Time'],df['Amount'],color='r',label='normal')
plt.scatter(anomalies['Time'],anomalies['Amount'], color='y',label='anomalies')
plt.show()