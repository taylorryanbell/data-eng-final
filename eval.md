# Capstone Final Review

## STEP 1 - SET UP (Creating a repo in GitHub)
- [ ] Was the Project forked from the original repo at https://www.github.com/adam-street/data-eng-final ?
- [ ] Was a python `.py` program created in their repo?
- [ ] Was a `requirements.txt` file created in their repo?
	- [ ] Does `requirements.txt` include `apache-beam[gcp]`?

---
## STEP 2 - JENKINS
- [ ] Is there a .gitignore? files like...
          .idea
- [ ] Was a Jenkins project created with the programmer's name and an appropriate title?
- [ ] Does it connect to the appropriate GitHub properly?
	- [ ] Webhook inside GitHub settings: `http://3.21.225.172:8081/github-webhook/`
	- [ ] Correct Repo URL inside Jenkins under Source Code Management > Git
	- [ ] Correct branch name under Branches to Build (matches GitHub)
	- [ ] Build Trigger set up to accept `GitHub hook trigger for GITScm polling`
- [ ] Under Build, does the Shell Execution have a script which will properly:
		- create a new project folder in `/var/dataflow/` with the correct naming convention: `[first-name]-[last-name]-final-project`
		- copy the proper files from `./` into the newly created project folder
		- create a virtual environment
		- activate the virtual environment
		- use pip to install packages via `requirements.txt`
			- (must contain apache-beam[gcp], may contain other things, explain why)
		- export the GOOGLE_APPLICATION_CREDENTIALS to use the given link `/var/dataflow/york-cdf-start-b0964900c176.json`
			- (file provided by Adam on server to take care of credentials)
		- run the python file to execute a Dataflow pipeline
	- An example of the code that can accomplish the above:
	`mkdir -p /var/dataflow/taylor-bell-final-project/
	cp ./main.py /var/dataflow/taylor-bell-final-project/
	cp ./requirements.txt /var/dataflow/taylor-bell-final-project/
	cd /var/dataflow/taylor-bell-final-project/
	python3 -m venv env
	. ./env/bin/activate
	export GOOGLE_APPLICATION_CREDENTIALS="/var/dataflow/york-cdf-start-b0964900c176.json"
	python3 -m pip install -r requirements.txt
	python3 main.py`
	- Show console output for last Jenkins build/run
        - Did it do what it was supposed to do?
        - Finished: SUCCESS
        - Can student explain the output reasonably indicating they are not lost?

---
## STEP 3 - THE PYTHON PROGRAM: Apache Beam
- Open Main.py (can be any program name but should make sense for the purpose
	- Can student explain execution path through their code?
	- Do they have a `if __main__ == '__main__':` statement?
- [ ] Uses `import apache_beam`, and any other necessary packages?
- [ ] Contains an apache beam pipeline (`with beam.Pipeline() as pipeline` as example)
- [ ] Pulls data from the three appropriate BigQuery tables?
        -    `york-cdf-start.final_input_data.customers`
        -   `york-cdf-start.final_input_data.product_views`
        -   `york-cdf-start.final_input_data.orders`
- [ ] Transforms the data in any required ways?
    - for instance, changing the data types to meet the appropriate requirements of the given schema in the Readme;
    - or combining data if necessary (through some method like PTransform or SQL query), to create the output data in dictionary form
- [ ] Uses `DataflowRunner` via the PipelineOptions to process the beam pipeline in Google Cloud Dataflow?
- [ ] Uses the other required pipeline options provided in the Readme
  - `opt = PipelineOptions(
        project="york-cdf-start",
        region="us-central1",
        runner="DataflowRunner",
        temp_location="gs://york_temp_files/tmp/",
        staging_location="gs://york_temp_files/staging",
        job_name="taylor-bell-final-job",
    )`
- [ ] Outputs data to two new BigQuery tables with the appropriate naming convention:
    - `york-cdf-start.final-[firstname]-[lastname].cust_tier_code-sku-total_no_of_product_views`
    - `york-cdf-start.final-[firstname]-[lastname].cust_tier_code-sku-total_sales_amount`
- [ ] Does the program create the correct schemas, specified in the Readme
- [ ] Does the student understand how the schemas are being created
- [ ] Is the student accounting for "mode: REQUIRED" appropriately in the schema?
- [ ] Is duplicate data accounted for in output tables, and how?
- [ ] Program runs without error (A couple Warnings are expected)

---
## STEP 4 - GOOGLE CLOUD PLATFORM
- When the program runs, does it do the following?
	- [ ] Inside Google Cloud Dataflow: A new job is generated with type Batch, and a name that follows the naming convention: `[first-name]-[last-name]-final-job`
	- [ ] ![Screen Shot 2022-01-08 at 11 06 29 AM](https://user-images.githubusercontent.com/94078849/148653145-a9205f6e-4612-4939-bd99-07fa36cbf386.png)

	- [ ] Inside BigQuery: The two new tables are created with the naming convention given in the previous section.

---
## STEP 5 - CHECKING THE DATA
- [ ] The table called `cust_tier_code-sku-total_no_of_product_views` should have 1990 rows, and it should contain the designated columns:
		- cust_tier_code (STRING), Required
		- sku (INTEGER), Required
		- total_no_of_product_views (INTEGER), Required
- [ ] The table called `cust_tier_code-sku-total_sales_amount` should have 1943 rows, and it should contain the designated columns:
		- cust_tier_code (STRING), Required
		- sku (INTEGER), Required
		- total_sales_amount (FLOAT), Required

---
## STEP 6 - CHECKING THE REPORT
The link to the publicly visible Data Studio report should be visible at the top of the programmer's GitHub repo's Readme.
- [ ] The 6 sums:
    - All product_views: 10,000
    - All sales: $17,471,263.20
    - Free tier product_views: 5,051
    - Free tier sales: $9,106,300.57
    - Paid tier product_views: 4,949
    - Paid tier sales: $8,364,962.63
- [ ] The Column chart: A single chart which Blends both output tables from the individual's BigQuery final dataset. Display should be a total of 4 vertical columns: Free tier product_views, Free tier sales; followed up Paid tier product_views, and Paid Tier sales. The chart ought to show axes labels, and a legend for which bar represents which section of data.
- [ ] The Three bar graphs
    - Total sales per Sku
    - Total sales per Sku (Free tier only)
    - Total sales per Sku (Paid tier only)
