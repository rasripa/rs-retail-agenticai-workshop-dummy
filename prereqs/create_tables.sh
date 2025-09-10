# create required dynamodb tables
pip install dynamodb-json -q
echo "managing Dynamo DB Tables ..."
python create_tables.py --mode create

