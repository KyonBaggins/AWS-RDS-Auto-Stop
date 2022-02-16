import boto3
from pprint import pprint

rds = boto3.client('rds')
uptime = 'shutdown'

def stop_db(id):
    try:
        resp = rds.stop_db_instance(DBInstanceIdentifier=id)
        return resp
    except Exception as e:
        if 'is not in available state.' in str(e):
            return f'{id} already stopped.'
    else:
        return f'{id} successfully stopped.'


def get_db_byuptime(uptime):
    dbs = rds.describe_db_instances()
    dblist = []
    for db in dbs['DBInstances']:
        id = db['DBInstanceIdentifier']
        arn = db['DBInstanceArn']
        tags = rds.list_tags_for_resource(
            ResourceName = arn
        )['TagList']
        for t in tags:
            if t['Key'].lower() == 'uptime' and t['Value'].lower() == uptime:
                dblist.append(id)
    return dblist


def lambda_handler(event, context):
    for d in get_db_byuptime(uptime):
        print(stop_db(d))
