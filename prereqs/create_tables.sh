# create required dynamodb tables
pip3 install dynamodb-json -q
echo "managing Dynamo DB Tables ..."
python3 create_tables.py --mode create

