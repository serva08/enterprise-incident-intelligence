# Databricks notebook source

raw_df = spark.table("raw_olist_orders")

print("Row count:", raw_df.count())

raw_df.printSchema()

display(raw_df.limit(10))


# COMMAND ----------

#How many orders are marked "delivered"?
from pyspark.sql.functions import col

orders_delivered = (
    raw_df.filter(col("order_status") == "delivered")
    .count()
)
print("Orders delivered:", orders_delivered)



# COMMAND ----------


from pyspark.sql import functions as F

orders = (
    raw_df
    .select(
        "order_id",
        "order_status",
        "order_purchase_timestamp",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    )
    .withColumn(
        "purchased_at",
        F.to_timestamp("order_purchase_timestamp")
    )
    .withColumn(
        "delivered_at",
        F.to_timestamp("order_delivered_customer_date")
    )
    .withColumn(
        "estimated_delivery_date",
        F.to_date("order_estimated_delivery_date")
    )
)

display(orders.limit(10))


# COMMAND ----------

#The business wants to measure whether completed deliveries happened after the promised date.


delivered_orders = (
    orders
    .filter(F.col("order_status") == "delivered")
    .filter(F.col("delivered_at").isNotNull())
    .filter(F.col("estimated_delivery_date").isNotNull())
    .filter(F.col("purchased_at").isNotNull())
)

delivery_df = (
    delivered_orders
    .withColumn(
        "delivery_days",
        F.datediff(
            F.to_date("delivered_at"),
            F.to_date("purchased_at")
        )
    )
    .withColumn(
        "days_late",
        F.greatest(
            F.datediff(
                F.to_date("delivered_at"),
                F.col("estimated_delivery_date")
            ),
            F.lit(0)
        )
    )
    .withColumn(
        "is_late",
        F.when(F.col("days_late") > 0, 1).otherwise(0)
    )
    .filter(F.col("delivery_days") >= 0)
)


summary = (
    delivery_df
    .agg(
        F.count("*").alias("total_deliveries"),
        F.sum("is_late").alias("late_deliveries"),
        F.round(
            F.avg("is_late") * 100, 2
        ).alias("late_delivery_pct"),
        F.round(
            F.avg("delivery_days"), 2
        ).alias("avg_delivery_days"),
        F.round(
            F.avg("days_late"), 2
        ).alias("avg_days_late")
    )
)

display(summary)



# COMMAND ----------

#Use the concepts from Days 7 and 8 to calculate the late-delivery percentage by purchase month.

monthly = (
    delivery_df
    .withColumn(
                "purchase_month",
                F.date_trunc("month", F.col("purchased_at"))
    )
    .groupBy("purchase_month")
    .agg(
                F.round(
                    F.avg("is_late") * 100, 2
                ).alias("late_delivery_pct")
    )
    .withColumn(
                "month_year",
                F.date_format("purchase_month", "MMMM yyyy")
    )
    .orderBy("purchase_month")
)


display(monthly)
