%sh 
# Create JAR directory for Sedona
mkdir -p /dbfs/FileStore/jars/sedona/1.3.1-incubating

# Download the dependencies from Maven into DBFS
curl -o /dbfs/FileStore/jars/sedona/1.3.1-incubating/geotools-wrapper-1.3.0-27.2.jar "https://repo1.maven.org/maven2/org/datasyslab/geotools-wrapper/1.3.0-27.2/geotools-wrapper-1.3.0-27.2.jar"

curl -o /dbfs/FileStore/jars/sedona/1.3.1-incubating/sedona-python-adapter-3.0_2.12-1.3.1-incubating.jar "https://repo1.maven.org/maven2/org/apache/sedona/sedona-python-adapter-3.0_2.12/1.3.1-incubating/sedona-python-adapter-3.0_2.12-1.3.1-incubating.jar"

curl -o /dbfs/FileStore/jars/sedona/1.3.1-incubating/sedona-viz-3.0_2.12-1.3.1-incubating.jar "https://repo1.maven.org/maven2/org/apache/sedona/sedona-viz-3.0_2.12/1.3.1-incubating/sedona-viz-3.0_2.12-1.3.1-incubating.jar"


################################################################################

%sh 

# Create init script directory for Sedona
mkdir -p /dbfs/FileStore/sedona/

# Create init script
cat > /dbfs/FileStore/sedona/sedona-init.sh <<'EOF'
#!/bin/bash
#
# File: sedona-init.sh
# Author: Erni Durdevic
# Created: 2021-11-01
# 
# On cluster startup, this script will copy the Sedona jars to the cluster's default jar directory.
# In order to activate Sedona functions, remember to add to your spark configuration the Sedona extensions: "spark.sql.extensions org.apache.sedona.viz.sql.SedonaVizExtensions,org.apache.sedona.sql.SedonaSqlExtensions"

cp /dbfs/FileStore/jars/sedona/1.3.1-incubating/*.jar /databricks/jars

EOF
