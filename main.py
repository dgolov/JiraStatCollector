from config import JIRA_URL, JIRA_TOKEN, JIRA_PASSWORD
from client import JiraClient
from typing import List, Union


class Mapper:
    def __init__(self, tickets_list: List[dict]):
        self.tickets_list = tickets_list
        self.result = {}

    def map_tickets(self) -> None:
        for ticket in self.tickets_list:
            summary: str = self._get_summary(ticket_data=ticket)
            if not summary:
                print(f"[-] Get summary error for ticket data - {ticket}")
                continue
            self._increment_summary_count(summary=summary)

    def _increment_summary_count(self, summary: str) -> None:
        summary_count: Union[int, None] = self.result.get(summary)
        if not summary_count:
            self.result[summary] = 1
        else:
            self.result[summary] = summary_count + 1

    @staticmethod
    def _get_summary(ticket_data: dict) -> str:
        fields = ticket_data.get("fields", {})
        return fields.get("summary")


def start():
    client = JiraClient(url=JIRA_URL, token=JIRA_TOKEN, password=JIRA_PASSWORD)
    client.auth()
    tickets = client.get_tickets()
    if not tickets:
        print(f"[-] Get tickets error")
        return
    mapper = Mapper(tickets_list=tickets)
    mapper.map_tickets()
    print("-----------------------------")
    print_result(result=mapper.result, total_count=len(tickets))


def print_result(result: dict, total_count: int) -> None:
    print("Результат за неделю:")
    for key, value in result.items():
        print(f"{key}: {value}")
    print(f"\nВсего: {total_count}")


if __name__ == '__main__':
    print("[#] Start")
    start()
