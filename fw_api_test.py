import pprint
import json
import requests
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
        requests.post('https://'+self.ip+'/logout', cookies=self.cookies, verify=self.verify, proxies=self.proxies)

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

    def post(self, path, api='v2', params=None, data=None):
        if isinstance(path, list):
            path = '/'.join(path) + '/'
        return requests.post('https://'+self.ip+'/api/'+api+'/'+path, headers=self.header,cookies=self.cookies, 
                            verify=self.verify, proxies=self.proxies, params=params, json={'json': data})

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

    def create(self, path, api='v2', params=None, data=None):
        response = json.loads(self.post(path, api=api, params=params, data=data).content)
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
    
    '''un = "admin"
    pw = getpass.getpass()

    try:
        t = fortigate_api('1.2.3.4:10443', un, pw)
        t.print_data (t.show(['cmdb', 'system', 'interface', 'port5']))
        t.print_data (t.edit(['cmdb', 'system', 'interface', 'port5'], data={'ip': '1.1.1.1 255.255.255.255','status': 'down'}), verbose=True)
        t.print_data (t.show(['cmdb', 'system', 'interface', 'port5']))
        t.print_data (t.edit(['cmdb', 'report', 'setting'], params={'vdom':'WAN'}, data={'fortiview': 'disable','pdf-report': 'disable'}))
    except:
        print ('something went wrong')
        raise'''
 


if __name__ == "__main__":
    main()
