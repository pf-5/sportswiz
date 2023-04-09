import json

def response(body={}, status=200, cors=True):

    headers = {
        'Access-Control-Allow-Headers': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
    } if cors else {}

    return {
        'statusCode': status,
        'headers': headers,
        'body': json.dumps(body)
    }
