# pip install --upgrade google-cloud-storage

from google.cloud import storage


bucket_name = '20220615-datastore'
storage_client = storage.Client()
bucket = storage_client.bucket(bucket_name)
blob = bucket.blob('20220615')
blob.upload_from_filename('C:\\Users\\mickh\\OneDrive\\01_Developer\\20220615.txt')


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        f"File {source_file_name} uploaded to {destination_blob_name}."
    )
