from boto3 import client


s3 = client(service='s3', url='https://clou.yanex.ru')


s3.list_objects(region='', bucket='', prefix='/ata/')
s3.copy_file
s3.move