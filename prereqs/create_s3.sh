#!/bin/bash
# Copyright 2024 Amazon.com and its affiliates; all rights reserved.
# This file is AWS Content and may not be duplicated or distributed without permission

# Script to create an S3 bucket and upload files from a directory

# Default values
MODE="create"
BUCKET_PREFIX="anycompany-retail"
DIRECTORY="data_files/anycompany-dataset"
S3_PREFIX="anycompany_profile"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --mode)
      MODE="$2"
      shift 2
      ;;
    --bucket-prefix)
      BUCKET_PREFIX="$2"
      shift 2
      ;;
    --directory)
      DIRECTORY="$2"
      shift 2
      ;;
    --s3-prefix)
      S3_PREFIX="$2"
      shift 2
      ;;
    --bucket-name)
      BUCKET_NAME="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Validate required parameters
if [ "$MODE" = "create" ]; then
  if [ -z "$BUCKET_PREFIX" ]; then
    echo "Error: --bucket-prefix is required for create mode"
    exit 1
  fi
  if [ -z "$DIRECTORY" ]; then
    echo "Error: --directory is required for create mode"
    exit 1
  fi
  
  # Execute Python script for create mode
  python3 create_s3.py --mode create --bucket-prefix "$BUCKET_PREFIX" --directory "$DIRECTORY" --s3-prefix "$S3_PREFIX" --bucket-name "$BUCKET_NAME"
  
elif [ "$MODE" = "delete" ]; then
  if [ -z "$BUCKET_NAME" ]; then
    echo "Error: --bucket-name is required for delete mode"
    exit 1
  fi
  
  # Execute Python script for delete mode
  python3 create_s3.py --mode delete --bucket-name "$BUCKET_NAME"
  
else
  echo "Error: Invalid mode. Use 'create' or 'delete'"
  exit 1
fi
