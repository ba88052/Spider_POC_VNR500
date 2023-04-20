# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from google.cloud import bigquery

class BigQueryPipeline:

    def __init__(self, project_id, dataset_id, table_id):
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.table_id = table_id

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            project_id=crawler.settings.get('GCP_PROJECT_ID'),
            dataset_id=crawler.settings.get('BQ_DATASET_ID'),
            table_id=crawler.settings.get('BQ_TABLE_ID')
        )

    def open_spider(self, spider):
        self.client = bigquery.Client(project=self.project_id)

        # Create dataset if not exists
        dataset_ref = self.client.dataset(self.dataset_id)
        try:
            self.client.get_dataset(dataset_ref)
            print(dataset_ref, "already exist")
        except Exception as e:
            dataset = bigquery.Dataset(dataset_ref)
            self.client.create_dataset(dataset)
            print("create", dataset_ref)

        # Create table if not exists
        self.table_ref = dataset_ref.table(spider.bq_table_name)
        try:
            self.client.get_table(self.table_ref)
            print(self.table_ref, "already exist")
        except Exception as e:
            schema = [
                bigquery.SchemaField("YEAR", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("CHART_ID", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("INDEX", "STRING", mode="NULLABLE"),
                bigquery.SchemaField("COMPANY_LEADER", "JSON", mode="NULLABLE"),
                bigquery.SchemaField("COMPANY_NAME", "STRING", mode="NULLABLE"),
                bigquery.SchemaField("COMPANY_VNR500_Rating", "STRING", mode="NULLABLE"),
                bigquery.SchemaField("COMPANY_MDN", "STRING", mode="NULLABLE"),
                bigquery.SchemaField("COMPANY_STOCK_CODE", "STRING", mode="NULLABLE"),
                bigquery.SchemaField("COMPANY_HEADQUARTERS", "STRING", mode="NULLABLE"),
                bigquery.SchemaField("COMPANY_TEL", "STRING", mode="NULLABLE"),
                bigquery.SchemaField("COMPANY_FAX", "STRING", mode="NULLABLE"),
                bigquery.SchemaField("COMPANY_EMAIL", "STRING", mode="NULLABLE"),
                bigquery.SchemaField("COMPANY_WEB", "STRING", mode="NULLABLE"),
                bigquery.SchemaField("COMPANY_FOUNDED_YEAR", "STRING", mode="NULLABLE"),
                bigquery.SchemaField("COMPANY_SUMMARY", "STRING", mode="NULLABLE"),
                bigquery.SchemaField("COMPANY_NEWS", "JSON", mode="NULLABLE")
            ]
            table = bigquery.Table(self.table_ref, schema = schema)
            self.client.create_table(table)
            print("create", self.table_ref)
    
    def close_spider(self, spider):
        self.client.close()        
            
    def process_item(self, item, spider):
        item_data = dict(item)

        errors = self.client.insert_rows_json(self.table_ref, [item_data])
        if errors:
            raise Exception(f"Errors while streaming data to BigQuery: {errors}")

        return item



class SpiderPocVnr500Pipeline:
    def process_item(self, item, spider):
        return item
