import os

from dotenv import load_dotenv


load_dotenv()


JIRA_URL = os.environ.get('JIRA_URL')
JIRA_TOKEN = os.environ.get('JIRA_TOKEN')
JIRA_PASSWORD = os.environ.get('JIRA_PASSWORD')
