# agent knowledge base
#pip install opensearch-py
#echo "deploying knowledge base ..."
#python knowledge_base.py --mode create

# create required dynamodb tables
pip3 install dynamodb-json -q
echo "managing Dynamo DB Tables ..."
python3 create_tables.py --mode create

# Create S3 bucket
echo "Creating S3 buckets ..."
python3 create_s3.py --mode create --bucket-prefix "anycompany-retail" --directory "data_files/anycompany-dataset" --s3-prefix "anycompany_profile"


