#!/usr/bin/env python

import pprint
import json
import requests
import time
import getpass


class fortigate_api:

    def __init__(self, ip, un, pw, verify=False, proxies=None, disable_warnings=True):
        if disable_warnings:
            requests.packages.urllib3.disable_warnings()
        unpw = {'username':un,'secretkey':pw}
        self.verify = verify
        self.ip = ip
        self.proxies=proxies
        auth = requests.post('https://'+self.ip+'/logincheck', data=unpw, verify=self.verify, proxies=self.proxies)
        self.cookies = auth.cookies
        for cookie in self.cookies:
            if cookie.name == "ccsrftoken":
                csrftoken = cookie.value[1:-1]  # token stored as a list
                self.header = {"X-CSRFTOKEN": csrftoken}

    def __enter__(self):
        return self

    def __del__(self):
        requests.post('https://'+self.ip+'/logout', verify=self.verify, cookies=self.cookies, proxies=self.proxies)

    def __exit__(self, *args):
        pass

    def get(self, path, api='v2', params=None):
        if isinstance(path, list):
            path = '/'.join(path) + '/'
        return requests.get('https://'+self.ip+'/api/'+api+'/'+path, cookies=self.cookies, verify=self.verify, proxies=self.proxies, params=params)

    def put(self, path, api='v2', params=None, data=None):
        if isinstance(path, list):
            path = '/'.join(path) + '/'
        return requests.put('https://'+self.ip+'/api/'+api+'/'+path, headers=self.header,cookies=self.cookies,
                            verify=self.verify, proxies=self.proxies, params=params, json={'json': data})

    def post(self, path, api='v2', params=None, data=None, files=None):
        if isinstance(path, list):
            path = '/'.join(path) + '/'
        return requests.post('https://'+self.ip+'/api/'+api+'/'+path, headers=self.header,cookies=self.cookies,
                            verify=self.verify, proxies=self.proxies, params=params, json={'json': data},
                            files=files)

    def delete(self, path, api='v2', params=None, data=None):
        if isinstance(path, list):
            path = '/'.join(path) + '/'
        return requests.delete('https://'+self.ip+'/api/'+api+'/'+path, headers=self.header,cookies=self.cookies,
                            verify=self.verify, proxies=self.proxies, params=params, json={'json': data})

    def show(self, path, api='v2', params=None):
        response = json.loads(self.get(path, api=api, params=params).content)
        return response

    def edit(self, path, api='v2', params=None, data=None):
        response = json.loads(self.put(path, api=api, params=params, data=data).content)
        return response

    def create(self, path, api='v2', params=None, data=None, files=None):
        response = json.loads(self.post(path, api=api, params=params, data=data, files=files).content)
        return response

    def remove(self, path, api='v2', params=None, data=None):
        response = json.loads(self.delete(path, api=api, params=params, data=data).content)
        return response

    @staticmethod
    def print_data(response, verbose=False):
        if response['status']=='success':
            if verbose:
                pprint.pprint (response)
            elif response['http_method']=='GET':
                pprint.pprint (response['results'])
            else:
                print ('OK!')
        else:
            print ('Fail!')
            pprint.pprint (response)



def main():
    un = "admin"
    pw = getpass.getpass()
    proxy = None

    fw = '10.0.1.2:10443'
   
    prefixlists = [
            {"name":"default_only","rule":[{"prefix":"0.0.0.0 0.0.0.0"}]},
            {"name":"dwre_sf_block6","rule":[{"prefix":"10.254.162.0 255.255.255.0","ge":25}]}
          ]

    try:
        t = fortigate_api(fw, un, pw, proxies=proxy)
        t.print_data (t.edit(['cmdb', 'router', 'prefix-list', 'dwre_sf_block6'], data = prefixlists[1]))
        t.print_data (t.show(['cmdb', 'router', 'prefix-list', 'dwre_sf_block6']))
        
    except:
        print ('something went wrong')
        raise

if __name__ == "__main__":
    main()
