from NGPIris.hcp import HCPManager
import json
# import boto3

# with open('D:/Dokument/accounts/hcp/credentials.json') as f:
#   c = json.load(f)

hcpm = HCPManager(credentials_path="D:/Dokument/accounts/hcp/credentials.json")
# hcpm.set_bucket("umea")
#
# hcpm.search_objects("trams")

# hcpm.list_buckets()
# # hcpm.attach_bucket("umea")
#
# hcpm.test_connection()
#
# objects = hcpm.get_objects()
#
#
# hcpm.test_connection()

#
# #
# session = boto3.session.Session()
# #
# s3_client = session.client(
#     service_name='s3',
#     aws_access_key_id=c['aws_access_key_id'],
#     aws_secret_access_key=c['aws_secret_access_key'],
#     endpoint_url=c['endpoint'],
#     verify=False
# )
# #
# print(s3_client)
# print(s3_client.list_buckets())
