from scripts.core.logger import Logger
from datetime import datetime
import boto3
import os, io, pytz

class S3DataLakeWriter:
    def __init__(self):
        self.logger = Logger()
        self.bucket = os.getenv('S3_BUCKET_NAME')
        
        if not self.bucket:
            raise ValueError("S3_BUCKET_NAME environment variable is not set")
        self.s3 = boto3.client(
            's3',
            region_name=os.getenv('AWS_REGION')
        )

    def write_dataframe(self, df, dataset_name):
        if df.empty:
            self.logger.warning(f"{dataset_name} is empty, skipping")
            return

        # Convert object columns to string (handles UUID and other types)
        df = df.astype({col: str for col, dtype in df.dtypes.items() if dtype == object})
        IST = pytz.timezone('Asia/Kolkata')
        now = datetime.now(IST)
        file_key = (
            f"lake/{dataset_name}/"
            f"year={now.year}/"
            f"month={now.month:02d}/"
            f"day={now.day:02d}/"
            f"{dataset_name}.parquet"
        )

        # Write to parquet in memory and upload
        buffer = io.BytesIO()
        df.to_parquet(buffer, index=False, engine='pyarrow')
        buffer.seek(0)

        self.s3.put_object(
            Bucket=self.bucket,
            Key=file_key,
            Body=buffer.getvalue()
        )

        self.logger.info(f"Wrote {len(df)} rows → {file_key}")
        return file_key