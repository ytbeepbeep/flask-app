import requests
from utils import SingletonDecorator

URL = "http://localhost:5002"

FUNCTIONS = {
    "GET": requests.get,
    "POST": requests.post,
    "DELETE": requests.delete
}

METHODS = ["GET", "POST", "DELETE"]

@SingletonDecorator
class DataService:

    @staticmethod
    def do_method(method, url, **kwds):
        if(method not in METHODS):
            raise "method not allowed"

        params = {}
        if 'params' in kwds:
            params = kwds['params']
        
        data = {}
        if 'data' in kwds:
            data = kwds['data']
        
        return FUNCTIONS[method](URL + url, params=params, data=data)

    @staticmethod
    def get(url, params):
        return DataService.do_method("GET", url, params=params)

    @staticmethod
    def post(url, data):
        return DataService.do_method("POST", url, data=data)

    @staticmethod
    def delete(url, params):
        return DataService.do_method("DELETE", url, params=params)

