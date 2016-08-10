# -*- coding: UTF-8 -*-
from get_sys_info import GetSysStat
import operator
import pprint
import json 
import time
import commands
def process_page():
  
  f =[]
  a= GetSysStat()
  b =a.get_pid()
  dd= a.get_disk_usge()
  #pprint.pprint(dd)
  mpstat = a.get_mpstat()
  proc_stat = a.get_proc_stat()
  #pprint.pprint(proc_stat)
  sar_row = [ 'Time' ,'kbmemfree', 'kbmemused' , 'memused' ,'kbbuffers' , 'kbcached',  'kbcommit',   'commit',  'kbactive',   'kbinact', 'kbdirty']
  sar_mem = a.parse_sar_mem('sar -r 2 5|cut -f 5', sar_row)
  sar_page_row = [ 'Time',  'pgpgin', 'pgpgout',   'fault'  ,'majflt' , 'pgfree', 'pgscank' ,'pgscand' ,'pgsteal',  'vmeff']
  sar_page =a.parse_sar_mem('sar -B 2 5|cut -f 5', sar_page_row)
  pidrow =['Time', 'UID', 'PID', 'usr', 'system' , 'guest',  'CPUper', 'CPU',  'Command']
  pdstat = a.parse_sar_mem('pidstat -u|cut -f 5', pidrow) 
  #pprint.pprint(pdstat)
  c = a.per_procs_status()
  tten = {}
  cp = []
  cpuinfo = a.get_sys_cpu()
  mempie = a.get_sys_mem()
  for ids in b:
    cpupid = a.get_cpupid(ids)
    tten[ids] = cpupid
    cp.append(tten)
  #print cp
  for i in cp:
    topten = dict(sorted(i.iteritems(), key=operator.itemgetter(1), reverse=True)[:10])
  
  io=a. get_iostat_per_process()
  cons = a.get_pid_cpu_consuming()
  statm = a.get_mem_perproc()
  filename = ["/proc/net/netstat", "/proc/net/snmp"]
  for files in filename:
    net  = a.get_net_stat_summary(files)
    f.append(net)
  #pprint.pprint(net)
  cpucore = a.read_procstat()
  cpuper = a.get_cpuused_per_core()

  with open("../pages/services/mempage.json", 'w') as sarpage:
    json.dump(sar_page, sarpage)
    sarpage.close()
  with open("../pages/services/disk_usage.json", 'w') as diskpage:
    json.dump(dd, diskpage)
    diskpage.close()
  with open("../pages/services/mempie.json", 'w') as mempiepage:
    json.dump(mempie, mempiepage)
    mempiepage.close()

  with open("../pages/services/pidstat.json", 'w') as pidpage:
    json.dump(pdstat, pidpage)
    pidpage.close()


  with open("../pages/services/memusage.json", 'w') as memusg:
    json.dump(sar_mem, memusg)
    memusg.close()
  with open("../pages/services/cpuper.json", 'w') as percpu:
    json.dump(cpuper, percpu)
    percpu.close()
  with open("../pages/services/cpuinfo.json", 'w') as cpinfo:
    json.dump(cpuinfo, cpinfo)
    cpinfo.close()
  with open("../pages/services/topten.json", 'w') as topcpu:
    json.dump(topten,topcpu)
    percpu.close()

  with open("../pages/services/mpstat.json", 'w') as mpst:
    json.dump(mpstat, mpst)
    mpst.close()



  with open("../pages/services/netsnmp.json", 'w') as netsnmp:
    json.dump(f, netsnmp) 
    netsnmp.close()
  with open("../pages/services/procs_stat.json", 'w') as psfile:
    json.dump(proc_stat, psfile)
    psfile.close()

  
  with open("../pages/services/cpucore.json", 'w') as core:
    json.dump(cpucore, core)
    core.close()
  
  with open("../pages/services/statm.json", 'w') as mfile:
    json.dump(statm, mfile)
    mfile.close()
 
  ctxt =  a.get_ctxt()
  with open("../pages/services/page_process.json", 'w') as outfile:
    json.dump(c, outfile)
    outfile.close()
  with open("../pages/services/io_per_process.json",'w') as iopage:
    json.dump(io, iopage)
    iopage.close()
  pro_maj_min = a. read_proc_stat()
  with open("../pages/services/pro_maj_min.json", 'w') as majmin:
    json.dump(pro_maj_min, majmin)
    majmin.close()
  with open("../pages/services/ctxt.json", 'w') as ctxfile:
    json.dump(ctxt,ctxfile)
    ctxfile.close()
  mpst = a.parse_command("mpstat -P ALL | cut -f 5")
  vmstat  = a.get_vmstat()
  com_data = commands.getoutput("ss -atp")
  fil_data = filter(lambda x:x !='', com_data.split('\n'))
  row_col=map(lambda x:x.strip().split(),fil_data)
  rows,col = row_col[0],row_col[1:]
  ptcp = []
  row  = ['state', 'recvq', 'sendq', 'locad', 'remad', 'addm']
  for c in col:
    d = dict(zip(row,c))
    ptcp.append(d)


  with open("../pages/services/vmstat.json", 'w') as vmst:
    json.dump(vmstat, vmst)
    vmst.close()

  
  with open("../pages/services/io_con.json", 'w') as iocons:
    json.dump(cons, iocons)
    iocons.close()
  with open("../pages/services/tcpcon.json", 'w') as tcpcon:
    json.dump(ptcp, tcpcon)
    tcpcon.close()
def main():
  #while True: 
  process_page()
  #time.sleep(1)  
    

if __name__ =='__main__':
  main()


