import json

import pytest

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.urls import reverse

from apps.core import constants as c
from apps.core.utils.testing_utils import login

from .models import StatementFile, Transaction


@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
@pytest.mark.django_db(transaction=True)
def test_upload_statement_file():

    client = login()

    filename = "test.csv"
    file_path = "apps/banking/fixtures/" + filename

    form = {"month": "2019-01-19"}

    with open(file_path, "rb") as fp:
        tmp_file = SimpleUploadedFile(
            filename, fp.read(), content_type="multipart/form-data",
        )
        data = {"form": json.dumps(form), "file": tmp_file}

        url = reverse("statements")
        client.post(
            f"{c.TEST_BASE_URL}{url}", data, format="multipart",
        )

    assert StatementFile.objects.all().count() == 1
    assert Transaction.objects.all().count() == 1
