# Databricks notebook source

from pyspark.sql import functions as F

data = [
    (1, "Fabric", "Connectivity issue", "High"),
    (2, "Databricks", "Resource exhaustion", "Critical"),
    (3, "Fabric", "Authentication issue", "Medium"),
    (4, "Fabric", "Connectivity issue", "Critical"),
    (5, "Databricks", "Connectivity issue", "Low"),
    (6, "Fabric", "Resource exhaustion", "High"),
]

columns = ["id", "product", "category", "severity"]

df = spark.createDataFrame(data, columns)




# COMMAND ----------

fabric_incidents = df.filter(df.product == "Fabric")
fabric_incidents.show()

# COMMAND ----------

fabric_incidents = df.filter(df.severity == "Critical")
fabric_incidents.show() 

# COMMAND ----------

from pyspark.sql.functions import count

category_summary = (
    df.groupBy("category")
    .agg(count("*").alias("incident_count"))
    .orderBy("incident_count", ascending=False)
)

category_summary.show()

# COMMAND ----------


product_severity_summary = (
    df.groupBy("severity")
    .agg(F.count("*").alias("incident_count"))
    .orderBy("incident_count", ascending=False)
)

product_severity_summary.show()

# COMMAND ----------


critical_summary = (
    df.filter(df.severity == "Critical")
      .groupBy("product", "category")
      .count()
)

critical_summary.show()


# COMMAND ----------


filtered_df = (df.filter(F.col("severity").isin("High","Critical")).select("id","product","severity")
)
filtered_df.show()


# COMMAND ----------

cleaned = (
    df.withColumn("product",F.trim(F.col("product")))
    .withColumn("category",F.trim(F.col("category")))
)

cleaned.show()

# COMMAND ----------

cleaned = (
    df.withColumn("product",F.trim(F.col("product")))
    .withColumn("category",F.trim(F.col("category")))
)

invalid = cleaned.filter(
    F.col("category").isNull() | (F.trim(F.col("category")) == "")
)

valid = cleaned.filter(
    F.col("category").isNotNull() & (F.col("category") != "")
)

valid.show()