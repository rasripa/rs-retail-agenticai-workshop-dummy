# Copyright 2024 Amazon.com and its affiliates; all rights reserved.
# This file is AWS Content and may not be duplicated or distributed without permission

"""
This module contains code for creating an S3 bucket and uploading files from a directory
"""

import boto3
import os
import argparse
import uuid
import random
from botocore.exceptions import ClientError


class S3Bucket:
    """
    Support class that allows for:
        - Creation of an S3 bucket
        - Uploading files from a directory to the bucket
        - Deletion of the bucket and its contents
    """

    def __init__(self, suffix=None):
        """
        Class initializer
        """
        boto3_session = boto3.session.Session()
        self.region_name = boto3_session.region_name
        self.account_number = (
            boto3.client("sts", region_name=self.region_name)
            .get_caller_identity()
            .get("Account")
        )
        if suffix is not None:
            self.suffix = suffix
        else:
            self.suffix = str(uuid.uuid4())[:4]
        self.s3_client = boto3_session.client("s3", region_name=self.region_name)
        self.s3_resource = boto3_session.resource("s3", region_name=self.region_name)

    def create_bucket(self, bucket_name_prefix):
        """
        Create an S3 bucket with the given prefix and account-specific suffix
        
        Args:
            bucket_name_prefix: Prefix for the bucket name
            
        Returns:
            bucket_name: Name of the created bucket
        """
        resource_suffix = random.randrange(100, 999)
        bucket_name = f"{bucket_name_prefix}-{resource_suffix}-{self.region_name}"
        
        try:
            if self.region_name == "us-east-1":
                self.s3_client.create_bucket(Bucket=bucket_name)
            else:
                self.s3_client.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={"LocationConstraint": self.region_name}
                )
            print(f"Created S3 bucket: {bucket_name}")
            return bucket_name
        except ClientError as e:
            if e.response["Error"]["Code"] == "BucketAlreadyOwnedByYou":
                print(f"Bucket {bucket_name} already exists and is owned by you.")
                return bucket_name
            else:
                print(f"Error creating S3 bucket: {e}")
                return None

    def upload_directory(self, bucket_name, directory_path, prefix=""):
        """
        Upload all files from a directory to the S3 bucket
        
        Args:
            bucket_name: Name of the S3 bucket
            directory_path: Path to the directory containing files to upload
            prefix: Optional prefix for S3 object keys
            
        Returns:
            success: True if all files were uploaded successfully, False otherwise
        """
        if not os.path.isdir(directory_path):
            print(f"Error: {directory_path} is not a valid directory")
            return False
            
        try:
            file_count = 0
            for root, _, files in os.walk(directory_path):
                for file in files:
                    local_path = os.path.join(root, file)
                    relative_path = os.path.relpath(local_path, directory_path)
                    s3_key = os.path.join(prefix, relative_path).replace("\\", "/")
                    
                    self.s3_client.upload_file(local_path, bucket_name, s3_key)
                    file_count += 1
                    
            print(f"Successfully uploaded {file_count} files to s3://{bucket_name}/{prefix}")
            return True
        except Exception as e:
            print(f"Error uploading files to S3: {e}")
            return False

    def delete_bucket(self, bucket_name):
        """
        Delete an S3 bucket and all its contents
        
        Args:
            bucket_name: Name of the S3 bucket to delete
            
        Returns:
            success: True if the bucket was deleted successfully, False otherwise
        """
        try:
            bucket = self.s3_resource.Bucket(bucket_name)
            bucket.objects.all().delete()
            bucket.delete()
            print(f"Deleted S3 bucket: {bucket_name}")
            return True
        except Exception as e:
            print(f"Error deleting S3 bucket: {e}")
            return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="S3 Bucket Handler")
    parser.add_argument(
        "--mode",
        required=True,
        help="S3 Helper Module. One of: create, delete.",
    )
    parser.add_argument(
        "--bucket-prefix",
        help="Prefix for the S3 bucket name",
    )
    parser.add_argument(
        "--directory",
        help="Directory path containing files to upload",
    )
    parser.add_argument(
        "--s3-prefix",
        default="",
        help="Prefix for S3 object keys (optional)",
    )
    parser.add_argument(
        "--bucket-name",
        help="Name of the bucket to delete (for delete mode)",
    )

    args = parser.parse_args()
    s3_handler = S3Bucket()

    if args.mode == "create":
        if not args.bucket_prefix:
            print("Error: --bucket-prefix is required for create mode")
            exit(1)
        if not args.directory:
            print("Error: --directory is required for create mode")
            exit(1)
            
        bucket_name = s3_handler.create_bucket(args.bucket_prefix)
        if bucket_name:
            s3_handler.upload_directory(bucket_name, args.directory, args.s3_prefix)
            print(f"Bucket name: {bucket_name}")
            
    elif args.mode == "delete":
        if not args.bucket_name:
            print("Error: --bucket-name is required for delete mode")
            exit(1)
            
        s3_handler.delete_bucket(args.bucket_name)