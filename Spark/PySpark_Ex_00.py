import findspark
findspark.init()

from pyspark import SparkContext
logFile = "C:/Spark/spark-3.0.2-bin-hadoop3.2/README.md"
sc = SparkContext("local", "first app")
logData = sc.textFile(logFile).cache()
numAs = logData.filter(lambda s: 'a' in s).count()
numBs = logData.filter(lambda s: 'b' in s).count()
print("Lines with a: %i, lines with b: %i" % (numAs, numBs))
