import logging
from config.config import Config
from simple_salesforce import Salesforce, SalesforceLogin

class SalesforceAPI:
    def __init__(self):
        self.sf = self.get_salesforce_instance()  # Initialize Salesforce instance
        self.logger = logging.getLogger(__name__)


    def get_salesforce_instance(self):
        try:
            session_id, instance = SalesforceLogin(username=Config.SALESFORCE_USERNAME, 
                                                    password=Config.SALESFORCE_PASSWORD, 
                                                    security_token=Config.SALESFORCE_SECURITY_TOKEN)
            return Salesforce(instance=instance, session_id=session_id)
        except Exception as e:
            self.logger.error(f"Error while initiating salesforce instance: {str(e)}")


    def fetch_data(self, query):
        try:
            query_records = self.sf.query_all(query)
            self.logger.info("fetched data from salesforce")
            return query_records
        except Exception as e:
            self.logger.error(f"Error while fetching data from salesforce: {str(e)}")            


    def delete_records(self, record_ids):
        try:
            batch = self.sf.bulk.Account.delete(record_ids)
            self.sf.bulk.wait_for_batch(batch)
            self.logger.info("deleted data from salesforce")
        except Exception as e:
            self.logger.error(f"Error while deleting data from salesforce: {str(e)}")
