import sys
import traceback
import json
from flask import request
import redis 

def log_info(_msg):
    print('INFO: {}'.format(_msg), file=sys.stdout, flush=True)


def log_error(_err):
    print('ERROR: {}'.format(str(_err)), file=sys.stderr)
    traceback.print_exc()
    sys.stderr.flush()

def connect_db():
    pool = redis.ConnectionPool(host='redis', port=6379, decode_responses=True)
    db = redis.Redis(connection_pool=pool)
    return db

def check_rsp_code(_rsp):
    if _rsp.status_code == 200:
        """
        try:
            values = json.loads(request.data)
        except Exception:
            raise ValueError("cannot parse json body {}".format(request.data))
        """
        return _rsp.json(),200
    else:
        return _rsp.json(), _rsp.status_code
        raise Exception(str(_rsp))
