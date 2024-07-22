from atlassian import Jira
from exceptions import JiraError
from tqdm import tqdm
from typing import List, Union


class JiraClient:
    def __init__(self, url: str, token: Union[str, None] = None, password: Union[str, None] = None):
        self.url = url
        self.token = token
        self.password = password
        self.jira = None
        self.fields = ["summary", "status", 'created']

    def auth(self) -> None:
        print(f"[#] Getting jira client")
        try:
            if self.token:
                self.jira = Jira(url=self.url, token=self.token, verify_ssl=False)
            else:
                self.jira = Jira(url=self.url, password=self.password, verify_ssl=False)
        except Exception as e:
            print(f"[#] Getting jira client error - {e}")

    def get_tickets(self) -> Union[List[dict], None]:
        print(f"[#] Get tickets")
        original_jql: str = self._get_jql()
        try:
            return self._batch_load(jql=original_jql, batch_size=300, fields=self.fields)
        except JiraError:
            print(f"[-] Wrong {original_jql}. Couldn't get issues count")
            return

    @staticmethod
    def _get_jql():
        try:
            with open("jql.txt", mode="r", encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError:
            print(f"[-] File jql.txt is not found")
            return input("Please input jql > ")

    def _batch_load(self, jql: str, fields: list = '*all', batch_size: int = 200) -> List[dict]:
        initial = 0
        issues_list = []

        try:
            issues_count = self.jira.jql(jql, limit=1, fields=fields)['total']
        except KeyError:
            raise JiraError

        batch_count = issues_count // batch_size + 1
        if batch_count > 1:
            print(f"[#] Loading batches from Jira. Need to download {issues_count} issues")

        with tqdm(total=batch_count) as progress_bar:
            while initial < issues_count:
                try:
                    result = self.jira.jql(jql, limit=batch_size, start=initial, fields=fields)
                    issues_list.extend(result['issues'])
                    initial += batch_size
                    progress_bar.update(1)
                except KeyError:
                    break
        return issues_list
