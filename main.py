#
# York B2E Capstone - Final Project
# Author: Taylor Bell
# 2022.01.04
#

# imports
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io.gcp.internal.clients import bigquery


# setting constants
PROJECT_ID = "york-cdf-start"
IN_DATASET_ID = "final_input_data"
IN_TABLE1_ID = "customers"
IN_TABLE2_ID = "product_views"
IN_TABLE3_ID = "orders"
OUT_DATASET_ID = "final-taylor-bell"
OUT_TABLE1_ID = "cust_tier_code-sku-total_no_of_product_views"
OUT_TABLE2_ID = "cust_tier_code-sku-total_sales_amount"


def run():
    print("Hello, Jenkins!")

    opt = PipelineOptions(project="york-cdf-start",
                          region="us-central1",
                          temp_location="gs://york_temp_files",
                          job_name="taylor-bell-final-job")

    table1_schema = {
        "fields": [
            {"name": "cust_tier_code", "type": "STRING", "mode": "REQUIRED"},
            {"name": "sku", "type": "INTEGER", "mode": "REQUIRED"},
            {"name": "total_no_of_product_views", "type": "INTEGER", "mode": "REQUIRED"}
        ]
    }
    table2_schema = {
        "fields": [
            {"name": "cust_tier_code", "type": "STRING", "mode": "REQUIRED"},
            {"name": "sku", "type": "INTEGER", "mode": "REQUIRED"},
            {"name": "total_sales_amount", "type": "FLOAT", "mode": "REQUIRED"}
        ]
    }

    out_table1 = bigquery.TableReference(
        projectId=PROJECT_ID,
        datasetId=OUT_DATASET_ID,
        tableId=OUT_TABLE1_ID)
    out_table2 = bigquery.TableReference(
        projectId=PROJECT_ID,
        datasetId=OUT_DATASET_ID,
        tableId=OUT_TABLE2_ID)

    test_table = bigquery.TableReference(
        projectId=PROJECT_ID,
        datasetId="trb_testing",
        tableId="test-table"
    )


    # runner="DataflowRunner", options=opt
    with beam.Pipeline() as pipeline:
        data = pipeline | "ReadFromBigQueryTest" >> beam.io.ReadFromBigQuery("gs://york-trb/tmp", table="york-cdf-start:trb_testing.test-table")

        data | beam.Map(print)
        pass


if __name__ == '__main__':
    run()