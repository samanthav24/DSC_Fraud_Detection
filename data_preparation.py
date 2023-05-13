import numpy as np
import pandas as pd
import pickle
from imblearn.over_sampling import SMOTENC
from collections import Counter
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import seaborn as sns
sns.set_theme()


def exclude_current_mean(row, mean_account, num_transactions):
  """Function that calculates mean excluding the current transaction
        param: row: pd DataFrame row
               mean_account: 'meanDest' or 'meanOrig'
               num_transactions = total number of transactions
        returns: mean of mean_account excluding current transaction
  """
  mean = row[mean_account]
  amount = row['amount']
  return ((mean*num_transactions) - amount) / (num_transactions - 1)


""" Account for missing values """

# load the dataset
df = pd.read_csv ('paysim.csv')
df = df.rename(columns={'oldbalanceOrg': 'oldbalanceOrig'})

# if oldBalance = newBalance = 0, account is likely from external institution
df['externalDest'] = ((df['oldbalanceDest'] == 0) & (df['newbalanceDest'] == 0)).astype(int)
df['externalOrig'] = ((df['oldbalanceOrig'] == 0) & (df['newbalanceOrig'] == 0)).astype(int)

# Update the values in the 'newbalanceDest' column to 'oldbalanceDest +- amount'
df['newbalanceDest'] = df['oldbalanceDest'] + df['amount']
df['oldbalanceOrig'] = df['newbalanceOrig'] + df['amount']


""" Feature Engineering """

# gaussian noise std
num_transactions = df.shape[0]
std = 0.01*(df['amount'].quantile(0.75) - df['amount'].min())

# calculate the overall mean and max of both the destination and origin account (excluding current transaction) and add noise
df['num_Dest'] = df.groupby('nameDest')['nameDest'].transform('count')
df['meanDest'] = df.groupby('nameDest')['amount'].transform('mean')
df['meanDest'] = df.apply(exclude_current_mean('meanDest', num_transactions), axis=1)
df['meanDest'] += noise