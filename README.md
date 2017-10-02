# NSO Query Tool

> Code Name Hubble

Enables SQL Like Queries into the NSO cDB

Sample usage:

```python
from nso_query_tool import NsoServer, NsoQuery

server = NsoServer('server', "user", "pass")
select= ['name', 'port', 'address']
_from= [{"device-group":"device_group_name"}, {"device":"box"}]
where= ["port='22'"]
query = NsoQuery(server, _from= _from, select= select, where= where)
for row in query.results:
    print row
print query.results.length()
```

Sample output:
```
{u'address': u'box', u'name': u'box', u'port': u'22'}
{u'address': u'box2', u'name': u'box3', u'port': u'22'}
{u'address': u'box3', u'name': u'box3', u'port': u'22'}
3
[Finished in 1.936s]
```

Another usage is filtering & selecting based on navigation.
This is most usage will happen (inside the configuration):

```python
from nso_query_tool import NsoServer, NsoQuery

server = NsoServer('server', "user", "pass")
select= ['name',"config/ios:ip/http/server"]
_from= ["*"]
where= ["config/ios:ip/http/server='true'"]
query = NsoQuery(server, _from= _from, select= select, where= where)
for item in query.results:
    print item
print query.results.length()
```

This will return every device in the network that has `ip http server` configured

Another example of filtering and specific device-groups.


```python
from nso_query_tool import NsoServer, NsoQuery

server = NsoServer('server', "user", "pass")
select = ['name', "config/ios:ip/http/server", "platform/model", "platform/version"]
  _from = [{"device-group":"group_name"}, {"device":"box"}]
  where = ["config/ios:tacacs/timeout='3'", "and", "config/ios:cdp/run ='true'"]
  query = NsoQuery(server, _from=_from, select=select, where=where)
  for item in query.results:
      print item
  print query.results.length()
```
