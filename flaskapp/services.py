import requests
import os
from flaskapp.utils import SingletonDecorator

URL = os.environ['DATA_SERVICE']

FUNCTIONS = {
    "GET": requests.get,
    "POST": requests.post,
    "DELETE": requests.delete
}

METHODS = ["GET", "POST", "DELETE"]


class DataService:

    @staticmethod
    def do_method(method, url, **kwds):
        if method not in METHODS:
            raise "method not allowed"

        params = {}
        if 'params' in kwds:
            params = kwds['params']
        
        data = {}
        if 'data' in kwds:
            data = kwds['data']

        return FUNCTIONS[method](URL + url, params=params, json=data)

    @staticmethod
    def get(url, params = {}):
        print("Request to DS: GET %s"%url)
        return DataService.do_method("GET", url, params=params)

    @staticmethod
    def post(url, data = {}):
        print("Request to DS: POST %s"%url)
        return DataService.do_method("POST", url, data=data)

    @staticmethod
    def delete(url, params = {}):
        print("params")
        print(params)
        return DataService.do_method("DELETE", url, params=params)

