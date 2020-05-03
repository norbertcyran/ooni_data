import datetime
import tarfile
from collections import defaultdict
from io import BytesIO
from typing import List, Dict

import yaml
from google.cloud import storage

from .bucket import get_mlab_bucket
from .db import Session
from .models import TestResult


def populate_db() -> None:
    """Populate DB with data from cloud."""
    session = Session()

    bucket = get_mlab_bucket()
    results = []

    blobs = bucket.list_blobs(prefix='ooni')

    for blob in blobs:
        results.extend([
            _get_test_result_from_record(record)
            for record in _parse_blob(blob)
            if 'tampering' in record
        ])

    session.bulk_save_objects(results)
    session.commit()
    session.close()


def fetch_all_ooni_data() -> Dict[str, List[Dict]]:
    """Fetch all data from OONI. Return dict keys represent dates."""
    bucket = get_mlab_bucket()
    data = defaultdict(list)

    blobs = bucket.list_blobs(prefix='ooni')

    for blob in blobs:
        date = '/'.join(blob.name.split('/')[-4:-1])
        data[date].extend(_parse_blob(blob))

    return data


def fetch_ooni_from_date(date: datetime.date) -> List[dict]:
    """Fetch and parse data from a given data from OONI DB."""
    bucket = get_mlab_bucket()
    blobs = list(bucket.list_blobs(
        prefix=f'ooni/{date.strftime("%Y/%m/%d")}'
    ))
    data = []
    for blob in blobs:
        data.extend(_parse_blob(blob))

    return data


def _parse_blob(blob: storage.Blob) -> List[dict]:
    """Parse single archive into list of dicts."""
    stream = BytesIO(blob.download_as_string())
    tar = tarfile.open(fileobj=stream)

    data = []
    for data_file in tar.getmembers():
        test_result = {}
        for record in yaml.load_all(tar.extractfile(data_file), Loader=yaml.CLoader):
            if record:
                test_result.update(record)
        data.append(test_result)

    return data


def _get_test_result_from_record(record):
    return TestResult(
        country_code=record['probe_cc'],
        total_tampered=record['tampering'].get('total', False),
        header_field_name_tampered=record['tampering'].get(
            'header_field_name',
            False
        ),
        header_field_number_tampered=record['tampering'].get(
            'header_field_number',
            False
        ),
        header_field_value_tampered=record['tampering'].get(
            'header_field_value',
            False
        ),
        header_name_capitalization_tampered=record['tampering'].get(
            'header_name_capitalization',
            False
        ),
        header_name_diff=','.join(record['tampering'].get(
            'header_name_diff',
            []
        )),
        request_line_capitalization_tampered=record['tampering'].get(
            'request_line_capitalization',
            False
        ),
        start_time=datetime.datetime.fromtimestamp(record['start_time'])
    )
