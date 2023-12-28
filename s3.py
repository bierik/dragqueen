import boto3


class S3Client:
    def __init__(
        self,
        endpoint_url,
        bucket_name,
        access_key_id,
        secret_access_key,
    ):
        self.bucket_name = bucket_name
        self.endpoint_url = endpoint_url
        self.client = boto3.client(
            "s3",
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
        )

    def list(self):
        paginator = self.client.get_paginator("list_objects_v2")
        return paginator.paginate(
            Bucket=self.bucket_name, PaginationConfig={"MaxItems": 10}
        )

    def download(self, path, fio):
        return self.client.download_fileobj(self.bucket_name, path, fio)
