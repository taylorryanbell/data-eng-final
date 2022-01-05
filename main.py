#
# York B2E Capstone - Final Project
# Author: Taylor Bell
# 2022.01.04
#

# imports
import json
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


class ChangeData(beam.DoFn):
    def process(self, element):
        print(element)
        print(type(element))
        # new_string = json.loads(element.decode("UTF-8"))
        # print(new_string)

        # output = json.dumps(new_string).encode("UTF-8")
        yield element

def run():
    print("Hello, Jenkins!")

    opt = PipelineOptions(
        project="york-cdf-start",
        region="us-central1",
        temp_location="gs://york-trb/tmp",
        staging_location="gs://york-trb/staging",
        job_name="taylor-bell-final-job",
        save_main_session=True
    )

    out_table1_schema = {
        "fields": [
            {"name": "cust_tier_code", "type": "STRING", "mode": "REQUIRED"},
            {"name": "sku", "type": "INTEGER", "mode": "REQUIRED"},
            {"name": "total_no_of_product_views", "type": "INTEGER", "mode": "REQUIRED"}
        ]
    }
    out_table2_schema = {
        "fields": [
            {"name": "cust_tier_code", "type": "STRING", "mode": "REQUIRED"},
            {"name": "sku", "type": "INTEGER", "mode": "REQUIRED"},
            {"name": "total_sales_amount", "type": "FLOAT", "mode": "REQUIRED"}
        ]
    }

    out_test_schema = {
        "fields": [
            {"name": "order_id", "type": "INTEGER", "mode": "REQUIRED"},
            {"name": "customer_name", "type": "STRING", "mode": "REQUIRED"},
            {"name": "items", "type": "STRING", "mode": "REQUIRED"}
        ]
    }

    out_table1 = bigquery.TableReference(
        projectId=PROJECT_ID,
        datasetId=OUT_DATASET_ID,
        tableId=OUT_TABLE1_ID
    )

    out_table2 = bigquery.TableReference(
        projectId=PROJECT_ID,
        datasetId=OUT_DATASET_ID,
        tableId=OUT_TABLE2_ID
    )

    test_table = bigquery.TableReference(
        projectId=PROJECT_ID,
        datasetId="trb_testing",
        tableId="test-out-dataflow"
    )

    with beam.Pipeline(runner="DataflowRunner", options=opt) as pipeline:
        data = pipeline | "ReadFromBigQueryTest" >> beam.io.ReadFromBigQuery(
            "gs://york-trb/tmp",
            table="york-cdf-start:trb_testing.test-table"
        )

        change = data | "ChangeData" >> beam.ParDo(ChangeData())

        change | "WriteToBigQuery" >> beam.io.WriteToBigQuery(
            test_table,
            custom_gcs_temp_location="gs://york-trb/tmp",
            schema=out_test_schema,
            create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED
        )

        pass


if __name__ == '__main__':
    run()
    pass
