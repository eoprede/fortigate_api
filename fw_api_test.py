#!/usr/bin/env python

import pprint
import requests
import getpass


class fortigate_api:

    _secure=True

    def __init__(self, ip, un, pw, verify=False, proxies=None, disable_warnings=True, secure=True):
        if disable_warnings:
            requests.packages.urllib3.disable_warnings()
        unpw = {'username':un,'secretkey':pw}
        self._secure=secure
        self.verify = verify
        self.ip = ip
        self.proxies=proxies
        if self._secure:
            http='https://'
        else:
            http='http://'
        auth = requests.post(http+self.ip+'/logincheck', data=unpw, verify=self.verify, proxies=self.proxies)
        self.cookies = auth.cookies
        for cookie in self.cookies:
            if cookie.name == "ccsrftoken":
                csrftoken = cookie.value[1:-1]  # token stored as a list
                self.header = {"X-CSRFTOKEN": csrftoken}

    def __enter__(self):
        return self

    def __del__(self):
        if self._secure:
            http='https://'
        else:
            http='http://'
        try:
            requests.post(http+self.ip+'/logout', verify=self.verify, cookies=self.cookies, proxies=self.proxies)
        except AttributeError:
            print ("Looks like connection to "+self.ip+" has never been established")



    def __exit__(self, *args):
        pass

    def get(self, path, api='v2', params=None):
        if isinstance(path, list):
            path = '/'.join(path) + '/'
        if self._secure:
            http='https://'
        else:
            http='http://'
        return requests.get(http+self.ip+'/api/'+api+'/'+path, cookies=self.cookies, verify=self.verify, proxies=self.proxies, params=params)

    def put(self, path, api='v2', params=None, data=None):
        if isinstance(path, list):
            path = '/'.join(path) + '/'
        if self._secure:
            http='https://'
        else:
            http='http://'
        return requests.put(http+self.ip+'/api/'+api+'/'+path, headers=self.header,cookies=self.cookies,
                            verify=self.verify, proxies=self.proxies, params=params, json={'json': data})

    def post(self, path, api='v2', params=None, data=None, files=None):
        if isinstance(path, list):
            path = '/'.join(path) + '/'
        if self._secure:
            http='https://'
        else:
            http='http://'
        return requests.post(http+self.ip+'/api/'+api+'/'+path, headers=self.header,cookies=self.cookies,
                            verify=self.verify, proxies=self.proxies, params=params, json={'json': data},
                            files=files)

    def delete(self, path, api='v2', params=None, data=None):
        if isinstance(path, list):
            path = '/'.join(path) + '/'
        if self._secure:
            http='https://'
        else:
            http='http://'
        return requests.delete(http+self.ip+'/api/'+api+'/'+path, headers=self.header,cookies=self.cookies,
                            verify=self.verify, proxies=self.proxies, params=params, json={'json': data})

    def show(self, path, api='v2', params=None):
        response = self.get(path, api=api, params=params)
        return response.json()

    def edit(self, path, api='v2', params=None, data=None):
        response = self.put(path, api=api, params=params, data=data)
        return response.json()

    def create(self, path, api='v2', params=None, data=None, files=None):
        response = self.post(path, api=api, params=params, data=data, files=files)
        return response.json()

    def remove(self, path, api='v2', params=None, data=None):
        response = self.delete(path, api=api, params=params, data=data)
        return response.json()

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
    #proxy={'http': 'socks5://127.0.0.1:9000'}
    proxy = None

    fw = '192.168.3.19'

    intf = {
              "name": "testagg",
              "vdom": "root",
              "allowaccess": "ping",
              "ip": "1.1.1.1 255.255.255.0",
              "role": "lan",
              "type": "aggregate",
              "member": [
                {
                    "interface-name": "port6"
                },
                {
                    "interface-name": "port7"
                }
              ]
            }

    try:
        t = fortigate_api(fw, un, pw, proxies=proxy)
        t.print_data (t.show('cmdb/system/interface'))
        t.print_data (t.create('cmdb/system/interface', data=intf))

    except:
        print ('something went wrong')
        raise

if __name__ == "__main__":
    main()
