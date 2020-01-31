from rest_framework import serializers


from .models import Transaction, StatementFile


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = '__all__'


class StatementFileSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(required=False)

    class Meta:
        model = StatementFile
        fields = (
            'month',
            'statement_file',
            'id'
        )
