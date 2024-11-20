import os
import pyspark as spark
# from pyspark.sql import functions as F

# PATH = r"D:\Курсы(образование)\Яндекс Специализации\BigData\Lesson_8 (big.csv)"
#
# shows_file = os.path.join(PATH, "shows-log.csv")
# clicks_file = os.path.join(PATH, "clicks-log.csv")


def process(a, b):
    # print(shows_file, clicks_file, sep='\n')

    conf = spark.SparkConf().setAppName("SparkApp").setMaster("local")
    sc = spark.SparkContext(conf=conf)

    data1 = [1, 2, 3, 4, 5]
    distData1 = sc.parallelize(data1)
