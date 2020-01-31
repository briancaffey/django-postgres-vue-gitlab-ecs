# Notes on building a personal finance / banking record system

## Source data

Using BofA CSV files from monthly statements. Here's a sample line:

```
['Posted Date', 'Reference Number', 'Payee', 'Address', 'Amount']
['12/12/2019', '24801979345726842597445', 'HONEY GROW # 100 PHILADELPHIA PA', 'PHILADELPHIA  PA ', '-11.99']
```

Let's use the date, description, location and amount.

## Django Setup

First, create a new app in our project called banking:

```
django startapp banking
```

To store the data in python, let's create some models

Since the data for each line item is consistent, let's create fields for each column in the CSV:

BankTransaction
Month: DateField
Description: CharField
Location: CharField
Amount: FloatField
Type: SmallIntegerField (0 for debit, 1 for credit)

Statement File
Month: DateField
File: FileField
Status: SmallIntegerField (processed, processing, errors)

add these models in `banking/models.py` and then run `django migrate`

register the models in the admin

create urls, views and serializers for our api

next, create a function that will create transactions from a statement file, we can do this in the notebook

Tests

Let's create a serializer for the StatementFile model

This will allow us to create new statement files from post requests and optionally process the files as we upload them


Now we can test out this serializer with a test