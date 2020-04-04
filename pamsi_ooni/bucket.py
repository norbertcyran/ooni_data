from google.cloud import storage

MLAB_BUCKET = 'archive-measurement-lab'


def get_mlab_bucket() -> storage.Bucket:
    client = storage.Client.create_anonymous_client()
    return client.bucket(MLAB_BUCKET)
