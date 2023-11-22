#!/usr/bin/python
#****************************************************************#
# ScriptName: dnsclient.py
# Author: $SHTERM_REAL_USER@alibaba-inc.com
# Create Date: 2019-05-20 19:53
# Modify Author: $SHTERM_REAL_USER@alibaba-inc.com
# Modify Date: 2019-06-05 11:11
# Function:
#***************************************************************#
import urllib,json,sys

if sys.argv.__len__() == 3 or sys.argv.__len__() == 5:
        command = sys.argv[1]
else:

        print ("usage: python dnsclient.py <queryrrs|addzone|delzone> <zone>\r\n       python dnsclient.py <addrr|delrr> <doamin> <zone> <ip>")
        exit(1)
dnsmng="172.19.59.190:80"
#zone = sys.argv[2]

if command == "queryrrs":
        zone = sys.argv[2]
        api = "http://"+dnsmng+"/zone/queryrrs"
        jstr = {'name': zone}
        body = json.dumps(jstr).encode('utf-8')
else:
        if command == "delzone":
                zone = sys.argv[2]
                api = "http://"+dnsmng+"/zone/delzone"
                jstr = {'name': zone}
                body = json.dumps(jstr).encode('utf-8')
        else:
                if command == "addzone":
                        zone=sys.argv[2]
                        api="http://"+dnsmng+"/zone/addzone"
                        jstr={  "name": zone,
                                "defaultTTL": 600,
                                "description": zone+"zone",
                                "type": "hosted",
                                "soa": {
                                        "mname": "master."+zone,
                                        "rname": "hostmaster."+zone,
                                        "serial": 1,
                                        "refresh": 3600,
                                        "retry": 1800,
                                        "expire": 604800,
                                        "minimumTTL": 60
                                        },
                                        "nsRRs": [{
                                        "name": zone+".",
                                        "type": "NS",
                                        "ttl": 60,
                                        "value": "ns1."+zone+"."
                                        }],
                                        "glueRRs": [{
                                        "name": "ns1."+zone+".",
                                        "type": "A",
                                        "ttl": 60,
                                        "value": "1.1.1.1"
                                        }]
                        }
                        body = json.dumps(jstr).encode('utf-8')
                else:
                        if command == "addrr":
                                domain = sys.argv[2]
                                zone = sys.argv[3]
                                ip = sys.argv[4]
                                api = "http://"+dnsmng+"/rr/addrr"
                                jstr = {
                                        "name": domain+".",
                                        "zone": zone+".",
                                        "value": ip,
                                        "ttl": 60,
                                        "type": "A"
                                        }
                                body=json.dumps(jstr).encode('utf-8')
                        else:
                                if command == "delrr":
                                        domain = sys.argv[2]
                                        zone = sys.argv[3]
                                        ip = sys.argv[4]
                                        api = "http://"+dnsmng+"/rr/delrr"
                                        jstr = {
                                        "name": domain+".",
                                        "zone": zone+".",
                                        "value": ip,
                                        "ttl": 60,
                                        "type": "A"
                                        }
                                        body=json.dumps(jstr).encode('utf-8')
                                else:
                                        print ("usage: python dnsclient.py <queryrrs|addzone|delzone> <zone>\r\n       python dnsclient.py <addrr|delrr> <doamin> <zone> <ip>")
                                        exit(1)
req = urllib.Request(url=api,data=body)
try:
        res = urllib.urlopen(req)
#except urllib.HTTPError,e:
#       print e.read()
#       exit(1)
except urllib.HTTPError as e:
        print (e.read())
        print ("catched errors and exited")
        exit(1)
resc=res.read()
res_json=json.loads(resc)
if command == "queryrrs":
        if res_json['success'] == True:
                pout = res_json['data']
                for x in pout:
                        if x['type'] == "A":
                                print (x['name'],x['value'])
else:
    print ('success:',res_json['success']),