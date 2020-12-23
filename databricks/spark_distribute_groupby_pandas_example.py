df1 = spark.read.csv("dbfs:/FileStore/shared_uploads/hudua@microsoft.com/adult.csv", header = True, inferSchema= True)

def user_defined_function(dataframe):
  import pandas as pd
  dataframe['coltest'] = dataframe['col11'] + 1
  max_value = dataframe['coltest'].max()
  return pd.DataFrame({
    'col1': dataframe['col1'].unique()[0],
    'col2': dataframe['col2'].unique()[0],
    'col3': dataframe['col3'].unique()[0],
    'col4': dataframe['col4'].unique()[0],
    'col5': dataframe['col5'].unique()[0],
    'value': [max_value]
  })
  
df = df1.groupBy('col1', 'col2', 'col3','col4', 'col5').applyInPandas(user_defined_function, schema = "col1 integer, col2 string, col3 double, col4 string, col5 double, value integer")
