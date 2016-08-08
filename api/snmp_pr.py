#!/usr/bin/env python

values = {}
key_data = None
key_val = None
with open('/proc/net/snmp') as fh:
    for line in fh:
        line = line.strip()
        if not line:
            continue 
        key, val = line.split(': ', 1)
        val = val.split(' ')
        if key_data != key:
            key_data = key
            key_val = val
        else:
          
            val = [ v for v in val ]
            values[key] = dict(zip(key_val, val))


import pprint
pprint.pprint(values)
