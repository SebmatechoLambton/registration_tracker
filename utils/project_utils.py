import numpy as np
import pandas as pd


def custom_agg(series):
    return ','.join(str(item) if item is not None else '' for item in series)

# def custom_agg(series):
# 	return ','.join(series)

def extract_unique_and_count1(row):
    values = row.split(',')
    unique_value = values[0]
    count = len(values)
    return pd.Series([unique_value, count], index=['unique_value', 'count'])

def extract_unique_and_count2(row):
    values = row.split(',')
    count = len(values)
    return pd.Series([row, count], index=['unique_value', 'count'])

