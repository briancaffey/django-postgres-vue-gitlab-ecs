import csv
import datetime
from io import StringIO

import celery
from celery.task import task

from apps.banking.models import StatementFile, Transaction


class BaseTask(celery.Task):
    pass


@task(bind=True, base=BaseTask)
def process_statement_file(self, statement_file_id):

    """
    This functions accepts one argument: the ID of a statement file
    It then opens the file, creates transactions and then uploads all
    of the transactions with one bulk create database operation
    """

    statement_file = StatementFile.objects.get(
        id=statement_file_id
    ).statement_file
    file_data = statement_file.read().decode("utf-8")
    csv_data = csv.DictReader(
        StringIO(file_data), delimiter=","
    )

    transactions = []
    for row in csv_data:
        date = datetime.datetime.strptime(
            row["Posted Date"], "%m/%d/%Y"
        )
        description = row["Payee"]
        address = row["Address"]
        amount = row["Amount"]
        transaction = Transaction(
            date=date,
            description=description,
            location=address,
            amount=amount,
            source_file_id=statement_file_id,
        )
        transactions.append(transaction)

    Transaction.objects.bulk_create(transactions)
    return
