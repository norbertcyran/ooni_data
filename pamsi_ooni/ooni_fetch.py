import datetime
import tarfile
from collections import defaultdict
from io import BytesIO
from typing import List, Dict

import yaml
from google.cloud import storage

from .bucket import get_mlab_bucket


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
