# Project Overview

 1. Use apache beam create a data pipeline to aggregate data from three big query input tables.
 2. Use the new aggregated data create a Google Data Studio report to visualize the data.
 3. Use Jenkins to launch a new Dataflow job anytime code is merged into the main branch of your repo

# General Information
  - All project resourses including any that you create should be under the google cloud project id ```b2e-data-eng-final```
  
    ## Input Data Specs
    - The input data is stored in three big query tables under the ```b2e-data-eng-final.input``` schema

      ### customers

      | Field Name                | Type           |
      | ------------------------- | -------------- |
      | CUSTOMER_ID               | STRING         |
      | CUST_TIER_CODE            | INTEGER        |

      ### product_views
      | Field Name                | Type           |
      | ------------------------- | -------------- |
      | CUSTOMER_ID               | STRING         |
      | EVENT_TM                  | TIMESTAMP      |
      | SKU                       | STRING         |

      ### orders
      | Field Name                | Type           |
      | ------------------------- | -------------- |
      | CUSTOMER_ID               | STRING         |
      | TRANS_TM                  | TIMESTAMP      |
      | ORDER_NBR                 | STRING         |
      | SKU                       | INTEGER        |
      | ORDER_AMT                 | FLOAT          |

     ## Output Data Specs
    - Your pipeline should output the following tables under a schema with the following naming convention ```b2e-data-eng-final.[first-name]-[last-name]``` schema

      ### cust_tier_code-sku-total_no_of_product_views

      | Field Name                | Type           | Mode        |
      | ------------------------- | -------------- | ----------- |
      | cust_tier_code            | TEXT           | REQUIRED    |
      | sku                       | INTEGER        | REQUIRED    |
      | total_no_of_product_views | INTEGER        | REQUIRED    |

      ### cust_tier_code-sku-total_sales_amount

      | Field Name                | Type           | Mode        |
      | ------------------------- | -------------- | ----------- |
      | cust_tier_code            | TEXT           | REQUIRED    |
      | sku                       | INTEGER        | REQUIRED    |
      | total_sales_amount        | INTEGER        | REQUIRED    |
  
## Pipeline Details
  - Your pipeline should take the following input options
  
  
      | Name          | Default            | Description                                       |
      | ------------- | ------------------ | ------------------------------------------------- |
      | project       | b2e-data-eng-final | project ID                                        |
      | region        | us-central1        | regional endpoint name                            |
      | runner        | DataflowRunner     | pipeline runner that executes your pipeline       |
      | temp_location |                    | Cloud Storage path for Dataflow temporary files   |
   
   
  - Your pipeline should pull all the data from the following input tables
    - ```b2e-data-eng-final.input.customers```
    - ```b2e-data-eng-final.input.product_views```
    - ```b2e-data-eng-final.orders```
   
  - Your pipeline should then merge the input data from the input tables to create the following tables
    -  cust_tier_code-sku-total_no_of_product_views
        - The data in this table should be the result of grouping all of the records from the ```b2e-data-eng-final.input.product_views``` table by the customers's tier code, the products sku, and the count of records that match the tier code and sku combination.
    - cust_tier_code-sku-total_sales_amount
      - This data in this table should be the result of grouping all of the records from the ```b2e-data-eng-final.input.orders``` table by the customers's tier code, the products sku, and the sum of the order amount for records that match the tier code and sku combination.

## Report Details
  
