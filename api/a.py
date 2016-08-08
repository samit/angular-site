import os
import pprint
from get_sys_info import GetSysStat
b =GetSysStat()
d = b.get_pid()
for id in d:
  a = open("/proc/"+id+"/status").readlines()
  state = ''.join([x for x in a if x.startswith('State')]).strip().split()
  vmrss = ''.join([x for x in a if x.startswith('VmRSS')]).strip().split()
  vmpeak = ''.join([x for x in a if x.startswith('VmPeak')]).strip().split()
  vmhwm =''.join([x for x in a if x.startswith('VmHWM')]).strip().split()
  d_keys = ['State', 'VmRss', 'VmPeak', 'VmHWM']
  d_val = [state, vmrss, vmpeak, vmhwm,]
  pprint.pprint(dict(zip(d_keys,d_val)))


