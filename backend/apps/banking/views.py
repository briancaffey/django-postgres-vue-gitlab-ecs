import datetime
import json

from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from .models import StatementFile, Transaction
from .serializers import StatementFileSerializer, TransactionSerializer
from .tasks import process_statement_file

# Create your views here.


class TransactionViewSet(viewsets.ViewSet):
    def get(self, request):
        paginator = LimitOffsetPagination()
        transactions = Transaction.objects.all()
        result_page = paginator.paginate_queryset(transactions, request)
        serializer = TransactionSerializer(result_page, many=True)
        return_data = paginator.get_paginated_response(serializer.data)
        return return_data


class StatementViewSet(viewsets.ViewSet):
    def get(self, request):
        paginator = LimitOffsetPagination()
        statement_files = StatementFile.objects.all()
        result_page = paginator.paginate_queryset(statement_files, request)
        serializer = StatementFileSerializer(result_page, many=True)
        return_data = paginator.get_paginated_response(serializer.data)
        return return_data

    def post(self, request):
        form_data = json.loads(request.data["form"])
        # convert the date into a format that the serializer can handle
        # we could also do this on the frontend
        date = form_data["month"]
        formatted_date = (
            datetime.datetime.strptime(date, "%Y-%m-%d")
            .date()
            .strftime("%Y-%m-%d")
        )
        form_data.update(dict(month_year=formatted_date))
        source_file = request.FILES["file"]
        serializer_data = {
            **form_data,
            "statement_file": source_file,
        }
        serializer = StatementFileSerializer(data=serializer_data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        statement_file_id = int(serializer.data["id"])

        if True:
            print("getting here...")
            process_statement_file.delay(statement_file_id)

        return Response(serializer.data)
