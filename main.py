#
# York B2E Capstone Project
# Taylor Bell
# 2022.1.5
# Description: This program will create an apache beam pipeline which runs via Dataflow, and will build every time the
#       app repo is updated on GitHub. This pipeline will read from three tables in BigQuery and then create two more.
#

# imports
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io.gcp.internal.clients import bigquery


class ChangeDataType(beam.DoFn):
    def process(self, element):
        element["cust_tier_code"] = str(element["cust_tier_code"])
        element["sku"] = int(element["sku"])
        yield element


def run():

    # set pipeline options for Google Cloud Dataflow
    opt = PipelineOptions(
        project="york-cdf-start",
        region="us-central1",
        runner="DataflowRunner",
        temp_location="gs://york_temp_files/tmp/",
        staging_location="gs://york_temp_files/staging",
        job_name="taylor-bell-final-job",
    )

    # schemas for creating the new tables
    export_1_schema = {
        'fields': [
            {'name': 'cust_tier_code', 'type': 'STRING', 'mode': 'REQUIRED'},
            {'name': 'sku', 'type': 'INTEGER', 'mode': 'REQUIRED'},
            {'name': 'total_no_of_product_views', 'type': 'INTEGER', 'mode': 'REQUIRED'}
        ]
    }
    export_2_schema = {
        'fields': [
            {'name': 'cust_tier_code', 'type': 'STRING', 'mode': 'REQUIRED'},
            {'name': 'sku', 'type': 'INTEGER', 'mode': 'REQUIRED'},
            {'name': 'total_sales_amount', 'type': 'FLOAT', 'mode': 'REQUIRED'}
        ]
    }

    # table references for both new tables
    out_table1 = bigquery.TableReference(
        projectId="york-cdf-start",
        datasetId="final_taylor_bell",
        tableId="cust_tier_code-sku-total_no_of_product_views"
    )
    out_table2 = bigquery.TableReference(
        projectId="york-cdf-start",
        datasetId="final_taylor_bell",
        tableId="cust_tier_code-sku-total_sales_amount"
    )

    # establish Apache Beam pipeline
    with beam.Pipeline(options=opt) as pipeline:

        # read in data from BigQuery using SQL queries
        data1 = pipeline | "ReadFromBigQuery1" >> beam.io.ReadFromBigQuery(
            query="DROP TABLE IF EXISTS `york-cdf-start.final_taylor_bell.cust_tier_code-sku-total_no_of_product_views` " \
                  "WITH CTE AS ( " \
                  "SELECT c.CUST_TIER_CODE as cust_tier_code, SKU as sku, COUNT(p.SKU) as total_no_of_product_views " \
                  "FROM `york-cdf-start.final_input_data.product_views` as p " \
                  "JOIN `york-cdf-start.final_input_data.customers` as c ON p.CUSTOMER_ID = c.CUSTOMER_ID " \
                  "GROUP BY sku, cust_tier_code " \
                  "ORDER BY total_no_of_product_views DESC " \
                  ") SELECT cust_tier_code, sku, total_no_of_product_views FROM CTE " \
                  "ORDER BY cust_tier_code, total_no_of_product_views DESC;",
            use_standard_sql=True
        )
        data2 = pipeline | "ReadFromBigQuery2" >> beam.io.ReadFromBigQuery(
            query="DROP TABLE IF EXISTS `york-cdf-start.final_taylor_bell.cust_tier_code-sku-total_sales_amount` "
                  "WITH CTE AS ( " \
                  "SELECT c.CUST_TIER_CODE as cust_tier_code, SKU as sku, SUM(o.ORDER_AMT) as total_sales_amount " \
                  "FROM `york-cdf-start.final_input_data.orders` as o " \
                  "JOIN `york-cdf-start.final_input_data.customers` as c ON o.CUSTOMER_ID = c.CUSTOMER_ID " \
                  "GROUP BY sku, cust_tier_code " \
                  "ORDER BY total_sales_amount DESC " \
                  ") SELECT cust_tier_code, sku, total_sales_amount FROM CTE " \
                  "ORDER BY cust_tier_code, total_sales_amount DESC;",
            use_standard_sql=True
        )

        # convert data types
        converted1 = data1 | "ChangeDataType1" >> beam.ParDo(ChangeDataType())
        converted2 = data2 | "ChangeDataType2" >> beam.ParDo(ChangeDataType())

        # write to two new bigquery tables
        converted1 | "Write1" >> beam.io.WriteToBigQuery(
            out_table1,
            schema=export_1_schema,
            create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
            custom_gcs_temp_location="gs://york-trb/tmp"
        )
        converted2 | "Write2" >> beam.io.WriteToBigQuery(
            out_table2,
            schema=export_2_schema,
            create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
            custom_gcs_temp_location="gs://york-trb/tmp"
        )


if __name__ == '__main__':
    run()  # execute ETL pipeline
