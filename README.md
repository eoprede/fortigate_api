## fw_api_test
Main library to interface with the Fortigate API
It's best to use it with Fortigates running code 5.4 and later, as 5.2 lacks lots of API calls.

### Usage:

##### Instantiate object
```
fw = fortigate_api('1.2.3.4:10443', un, pw)
```
Proxy servers are supported as well:
Note that you will need to install socks5 for requests library: http://docs.python-requests.org/en/master/user/advanced/#socks
```
proxy={'https': 'socks5://127.0.0.1:9000'}
fw = fortigate_api('1.2.3.4:10443', un, pw, proxies=proxy)
```
You can enable HTTPS warnings if you are using real certs:
```
fw = fortigate_api('1.2.3.4:10443', un, pw, disable_warnings=False)
```

#### Show parameters of an object
For example, to print all the interfaces:
```
a = fw.show(['cmdb', 'system', 'interface'])
fw.print_data(a)
```
You can print only specific interface:
```
a = fw.show('cmdb/system/interface/port1') # note that you can provide either string or a list for API path
fw.print_data(a)
```
Sometimes it's hard to find the exact API path, so you can display the API schema (beware that it's very large)
```
fw.show(['cmdb', 'system', 'interface'], params={'action':'schema'}))
```
or for all the configurable objects (9M file), you can do
```
fw.show(['cmdb'], params={'action':'schema'}))
```

#### Edit parameters of an object
For example, edit route 1 and display OK if change successful:
```
a = fw.edit(['cmdb', 'router', 'static', '1'], data={"device": "FW_IP_outbound","dst": "0.0.0.0 0.0.0.0","gateway": "10.0.1.1","comment": "Default route for FW outbound"})
fw.print_data(a)
```

#### Remove object
For example, remove DHCP server 1
```
fw.remove(['cmdb', 'system.dhcp', 'server', '1'])
```

#### Create new object
For example, create new firewall rule:
```
policy = {"action": "accept",
            "dstaddr": [{"name": "all"}],
            "dstintf": [{"name": "Ext1"}],
            "name": "Allow_all_in",
            "nat": "disable",
            "policyid": 1,
            "schedule": "always",
            "service": [{"name": "ALL"}],
            "srcaddr": [{"name": "all"}],
            "srcintf": [{"name": "Ext2"}],
            "status": "disable"}
fw.create (['cmdb','firewall','policy'], data=policy)
```

#### Working with VDOMs
By default, you are working with VDOM root, but you can specify any other VDOM with params={'vdom':'WAN'}
For example, previous API call with VDOM would look like this:
```
fw.create (['cmdb','firewall','policy'], params={'vdom':'WAN'}, data=policy)
```

#### Known issues
* Error checking is non-existent. For example, failed authentication would be raised as a JSON exception (as there would be nothing to decode from an API response, as there would be none)
* I have not tested additional actions, like moving FW policies around. Theoretically it should be done with additional values in params, but I haven't tested it.
