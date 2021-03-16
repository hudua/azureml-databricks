# Databricks notebook source
# MAGIC %md #### Distributed Deep Learning with Azure Databricks

# COMMAND ----------

# MAGIC %md #### Let's create a mount point

# COMMAND ----------

# dbutils.fs.mount(
#   source = "wasbs://<container-name>@<storage-account-name>.blob.core.windows.net",
#   mount_point = "/mnt/<mount-name>",
#   extra_configs = {"fs.azure.account.key.<storage-account-name>.blob.core.windows.net":<key>})

# COMMAND ----------

# MAGIC %md #### Deep learning distributed

# COMMAND ----------

# MAGIC %md We will cover some patterns of using Azure Databricks, leveraging distributed computations for deep learning on image classification

# COMMAND ----------

from PIL import Image 
from pyspark.sql.types import StringType, StructType, DoubleType, StructField
import matplotlib.pyplot as plt

import tensorflow.keras
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras import backend as K

# COMMAND ----------

(x_train, y_train), (x_test, y_test) = mnist.load_data()

# COMMAND ----------

n = 10

fig, ax = plt.subplots(1, n, figsize=(10, 2))
for idx, image in enumerate(x_train[:10]):
    ax[idx].imshow(image, cmap=plt.cm.Greys)
    ax[idx].set_xticks([])
    ax[idx].set_yticks([])
    ax[idx].set_title(y_train[idx], fontsize=18)

display(fig.figure)

# COMMAND ----------

# MAGIC %md #### Now let's train a number of deep learning models in parallel

# COMMAND ----------

import pandas as pd

DropoutA = [0.5,0.45,0.4]
DropoutB = [0.25,0.2,0.15]
Model = ['Model1', 'Model2', 'Model3']

models = pd.DataFrame({'Model': Model, 'DropoutA':DropoutA, 'DropoutB': DropoutB})
models_df_tune = spark.createDataFrame(models)

# COMMAND ----------

display(models_df_tune)

# COMMAND ----------

# MAGIC %md #### Distributed Deep Learning Model - Hyperparameter tuning
# MAGIC 
# MAGIC ![spark-architecture](https://training.databricks.com/databricks_guide/gentle_introduction/spark_cluster_tasks.png)

# COMMAND ----------

import random
def runDLModelHyper(row):
  (x_train, y_train), (x_test, y_test) = mnist.load_data()
  x_train = x_train[:5000][:][:]
  y_train = y_train[:5000]
  # input image dimensions
  img_rows, img_cols = 28, 28
  # number of classes (digits) to predict
  num_classes = 10

  x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
  x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
  input_shape = (img_rows, img_cols, 1)

  x_train = x_train.astype('float32')
  x_test = x_test.astype('float32')
  x_train /= 255
  x_test /= 255
  print('x_train shape:', x_train.shape)
  print(x_train.shape[0], 'train samples')
  print(x_test.shape[0], 'test samples')

  # convert class vectors to binary class matrices
  y_train = tensorflow.keras.utils.to_categorical(y_train, num_classes)
  y_test = tensorflow.keras.utils.to_categorical(y_test, num_classes)
  
  model = Sequential()
  model.add(Conv2D(32, kernel_size=(3, 3),
                   activation='relu',
                   input_shape=input_shape))
  model.add(Conv2D(64, (3, 3), activation='relu'))
  model.add(MaxPooling2D(pool_size=(2, 2)))
  #model.add(Dropout(0.25))
  model.add(Dropout(row.DropoutA))
  model.add(Flatten())
  model.add(Dense(128, activation='relu'))
  model.add(Dropout(random.random()/3))
  model.add(Dropout(row.DropoutB))
  model.add(Dense(num_classes, activation='softmax'))

  model.compile(loss=tensorflow.keras.losses.categorical_crossentropy,
                optimizer=tensorflow.keras.optimizers.Adadelta(),
                metrics=['accuracy'])
  batch_size = 500
  epochs = 1

  model.fit(x_train, y_train,
            batch_size=batch_size,
            epochs=epochs,
            verbose=1,
            validation_data=(x_test, y_test))
  
  score = model.evaluate(x_test, y_test, verbose=0)
  score = float(score[1])
  
  return(row.Model, row.DropoutA, row.DropoutB, score)

# COMMAND ----------

schema = StructType([
  StructField("ModelLocation", StringType(), False),
  StructField("DropoutA", DoubleType(), False),
  StructField("DropoutB", DoubleType(), False),
  StructField("Accuracy", DoubleType(), False)
                    ])

# COMMAND ----------

models_df_tune = models_df_tune.repartition('DropoutA')
models_df_tune.rdd.getNumPartitions()

# COMMAND ----------

results_df = models_df_tune.rdd.map(runDLModelHyper).toDF(schema)

# COMMAND ----------

display(results_df)

# COMMAND ----------

# MAGIC %md #### Distributed Deep Learning Model - Combined with Azure Machine Learning services
# MAGIC 
# MAGIC ![spark-architecture](https://azuremlstudioreadstorage.blob.core.windows.net/edmonton/Capture.JPG)
