from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate()

#####################
# test table access #
#####################
df = spark.sql('select * from test')
df.show(5)

##############################
# test user defined function #
##############################
def squared(s):
  return s * s
spark.udf.register("squaredWithPython", squared)

from pyspark.sql.functions import udf
from pyspark.sql.types import DoubleType
squared_udf = udf(squared, DoubleType())

df.select("pressure3", squared_udf("pressure3").alias("pressure3_squared")).show(5)

#############################
# test dbfs data read/write #
#############################
the_list = [
  '/mnt/fs1/sensorpressure_yielddata - Copy (4).csv'
]
df_python = spark.read.format('csv').options(header='true', inferSchema='true').load(the_list)

df_python.write.parquet("/mnt/fs1/proto5.parquet")

##########################
# test SQL DB connection #
##########################

jdbcHostname = "predmainserver.database.windows.net"
jdbcDatabase = "sampledb"
jdbcPort = 1433
jdbcUrl = "jdbc:sqlserver://{0}:{1};databaseName={2};user={3};password={4}".format(jdbcHostname, 
jdbcPort, jdbcDatabase, "hudua", secret1)
connectionProperties = {
  "driver" : "com.microsoft.sqlserver.jdbc.SQLServerDriver"
}

pushdown_query = "(select * from test_data) query"
sparkDf = spark.read.jdbc(url=jdbcUrl, table=pushdown_query, properties=connectionProperties)

sparkDf.show(5)

df_python.limit(100).write.jdbc(url=jdbcUrl, table="testoutput", mode="overwrite", properties=connectionProperties)
