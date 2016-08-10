#!/usr/bin/pythin
import os
import subprocess
import commands
import csv
from collections import namedtuple

class GetSysStat():


  def __init__(self):
    self.__init__


  def get_iostat_per_process(self):
    """ Returns the dict data from /proc/$pid/io need sudo access"""
   
    io_list = []
    pid = self.get_pid()
    d_key = ['rchar', 'wchar', 'syscr', 'syscw', 'read_bytes', 'write_bytes', 'cancelled_write_bytes']
    for ids in pid:
      iofile = open("/proc/"+ids+"/io", 'r').readlines()
      rchar = ''.join([line for line in iofile if line.startswith('rchar')]).strip().split()[1]
      wchar = ''.join([line for line in iofile if line.startswith('wchar')]).strip().split()[1]
      syscr = ''.join([line for line in iofile if line.startswith('syscr')]).strip().split()[1]
      syscw = ''.join([line for line in iofile if line.startswith('syscw')]).strip().split()[1]
      read_bytes = ''.join([line for line in iofile if line.startswith('read_bytes')]).strip().split()[1]
      write_bytes = ''.join([line for line in iofile if line.startswith('write_bytes')]).strip().split()[1]
      cancelled_write_bytes = ''.join([line for line in iofile if line.startswith('cancelled_write_bytes')]).strip().split()[1]
      d_val = [rchar, wchar, syscr, syscw, read_bytes, write_bytes, cancelled_write_bytes]
      io_proc = dict(zip(d_key, d_val))
      io_proc['pid']= ids
      io_list.append(io_proc)
    return io_list

  def get_uname(self):
    """ Returns the dict containing os Info """
    key_list = ['sysname', 'nodename', 'release',' version', 'machine']
    val_list = map(lambda x:x, os.uname())
    return dict(zip(key_list, val_list))

  def get_pid(self):
    """ Return the process in list owns by user loginspect"""

    pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]

    return pids

  def get_cpupid(self, pid):
    
    """ Return the cpu usage, memory usage, commands and process id own per Processes"""
    hertz= commands.getoutput("getconf CLK_TCK")    
    uptime = commands.getoutput("cat /proc/uptime").strip().split()[0]
    cpu_pid = []
    ret_cpu  = []
    cpu_id = open("/proc/"+pid+"/stat", 'r').read().strip().split()
    utime=cpu_id[13] # CPU time Spent in user code
    stime=cpu_id[14] #CPU time spent in Kernal COde
    cutime=cpu_id[15] #Waited-for children's CPU time spent in user code (in clock ticks)
    cstime = cpu_id[16] # Waited-for children's CPU time spent in kernel code (in clock ticks)
    starttime=cpu_id[21] #Time when the process started, measured in clock ticks
      
    total_time = float(utime)+float(stime)+float(cstime)+float(cutime)
    seconds = float(uptime) -(float(starttime)/(float(hertz)))
    cpu_usage = 100 * ((total_time/float(hertz))/seconds)
    return cpu_usage

  def get_ctxt(self):
     """ Returns the Context Switching voluntery and non voluntery per Processes return type List"""
     ret_list = []
     d_key = ['pid', 'command', 'vctx', 'nvctx']  
     d_ctx = {}
     for ids in self.get_pid():
       stat_file = open("/proc/"+ids+"/status").readlines()
       vol_ctx = (''.join([x for x in stat_file if x.startswith('voluntary_ctxt_switches')]).split(':')[1].strip())
       nvol_ctx = (''.join([x for x in stat_file if x.startswith('nonvoluntary_ctxt_switches')]).split(':')[1].strip())
       
       cmds = commands.getoutput("cat /proc/"+ids+"/cmdline")
       d_val = [ids, cmds,vol_ctx, nvol_ctx]
       d_ctx = dict(zip(d_key, d_val))
       ret_list.append(d_ctx)
     return ret_list
  
  def get_cpu_affinity(self, pid):
    """ Returns the CPU affinity owns per processes """
    cpu_aff = []
    for ids in self.get_pid():
      c_af=commands.getoutput("taskset -c -p "+ids)
      cpu_aff.append(c_af)
    cpu_aff_pid= dict(zip(cpu_aff,pid))
    return cpu_app_pid


  def parse_command(self, command):
    """ Returns the dict value of commands"""
    com_data = commands.getoutput(command)
    ret_list = []
    fil_data = filter(lambda x:x !='', com_data.split('\n'))
    #row_col=map(lambda x:x.strip().split(),fil_data)
    rows,col = fil_data[0],fil_data[1:]
    rows = rows.split()
    rows[0] = "Time"

    for line in col:
      d_data = dict(zip(rows,col))
      ret_list.append(d_data) 
    return ret_list


  def get_cpu_stat(self):
    """ Returns the out put of sar command in parsed form"""
    command = commands.getoutput(" mpstat -P ALL  |cut -f 5 ")
    return self.parse_command(command)  
   
  def get_sys_mem(self):
    
    """ Read the MemoryFile,CPU file and return the Dict"""
    memfile = open('/proc/meminfo','r').readlines()
    meminfo = {}
    for line in memfile:
      meminfo[line.split(':')[0]] = line.split(':')[1].strip()
    return meminfo


  def get_sys_cpu(self):

    """ Read the CPU file and return the Dict"""
    cpufile = open('/proc/cpuinfo','r').readlines()
    cpuinfo = {}
    for line in cpufile:
      try:
        cpuinfo[line.split(':')[0].strip()] = line.split(':')[1].strip()
      except Exception as e:
        pass
    return cpuinfo


  def read_proc_stat(self):
    """ Read /proc/pid/stat file and retrn dict """
    key_list = ['pid', 'command', 'state', 'PPID', 'Pgrp', 'session', 'tty_nr', 'flags', 'minflt', 'cminflt', 'majflt', 'cmajflt', 'utime', 'stime', 'cutime', 'cstime', 'prioroty', 'nice', 'num_threads', 'itervalues', 'starttime', 'vsize', 'rss', 'rsslim', 'startcode', 'endcode', 'startstack', 'kstkesp', 'signal', 'blocked', 'sigignore', 'sigcach', 'wchan', 'nswap', 'cnswap', 'exit_signal', 'processor', 'rt_prioroty', 'policy', 'elayacct_blkio_ticks', 'guest_time', 'cguest_time']
    pid = self.get_pid()
    proc_list = []
    for ids in pid:
      val = commands.getoutput("cat /proc/"+ids+"/stat").strip().split()
      dict_data = dict(zip(key_list,val))
      proc_list.append(dict_data)
    return proc_list


  def alert_system(self):
    """ Collect the vmstat output for 10 second and based on info print alert"""
    p = commands.getoutput("vmstat 1 10 >vmstat.csv ")
    minor2major = {
    'r': 'procs',
    'b': 'procs',
    'swpd': 'memory',
    'free': 'memory',
    'buff': 'memory',
    'cache': 'memory',
    'inact': 'memory',  
    'active': 'memory', 
    'si': 'swap',
    'so': 'swap',
    'bi': 'io',
    'bo': 'io',
    'in': 'system',
    'cs': 'system',
    'us': 'cpu',
    'sy': 'cpu',
    'id': 'cpu',
    'wa': 'cpu',
    'st': 'cpu'
}
  
    minors = []
    content = dict([(h, {}) for h in set(minor2major.values())])
    vm_file = commands.getoutput("vmstat 1 10 > vmstat.csv")  
    reader=csv.reader(open("vmstat.csv"), delimiter=' ', skipinitialspace=True)
    for row in reader:
      if reader.line_num == 1:
        pass
      elif reader.line_num == 2:
        minors = row
        for h in row:
          content[minor2major[h]][h] = []
      elif row[0] != minors[0] and row[0] != minor2major[minors[0]]:
        for i, v in enumerate(row):
          content[minor2major[minors[i]]][minors[i]].append(int(v))
    return content
 
            


  def get_mem_perproc(self):
    """ Read the /proc/pid/statm file and returns the memory usage """

    d_list = []
    f_list = []
    d_key = ['tot_prog_size','res_set_size','share_page','txt_code','data_stack','lib','dirty_pages']
    pid = self.get_pid()
    for ids in pid:
      f_list  = commands.getoutput("cat /proc/"+ids+"/statm").strip().split()
      cmds = commands.getoutput("cat /proc/"+ids+"/cmdline")
      tot_prog_size = float(f_list[0])*4
      res_set_size = float(f_list[1])*4
      share_page = f_list[2]
      txt_code = float(f_list[3])*4
      data_stack = f_list[4]
      lib = float(f_list[5])*4
      dirty_pages = f_list[6]
      d_val = [tot_prog_size,res_set_size,share_page,txt_code,data_stack,lib,dirty_pages]
      d_statm = dict(zip(d_key,d_val))
      d_statm['pid'] = ids
      d_statm['cmd'] = cmds
      #data = "PID="+id+"\nProcess command = "+cmds+"\nToatal Program Size: = "+str(tot_prog_size)+"\nResident Set Size:="+str(res_set_size)+"\nShare Page:="+str(share_page)+"\nText Code:="+str(txt_code)+"\nData Stack:="+str(data_stack)+"\nLibrary:="+str(lib)+"\nDirty Pages:="+str(dirty_pages)+"\n"
      d_list.append(d_statm)
    
    return d_list


  def get_pid_cpu_consuming(self):
    """ Returns the list of  process consuming CPU """
    pids = self.get_pid()
    d_key = ['pid', 'command', 'cpuused', 'state']
    process_list= []
    for ids in pids:
      procs_com = commands.getoutput("cat /proc/"+ids+"/status| grep State| awk '{print $2}'")
      if procs_com =='D':
        pid = ids
        cmd = commands.getoutput("cat /proc/"+ids+"/cmdline")
        cpuused = self.get_cpupid(ids)
        state = procs_com
        d_val = [pid,cmd,cpuused,state]
        d_consm = dict(zip(d_key, d_val))
        process_list.append(d_consm)
    return process_list

  def get_proc_stat(self):   
    """ Read /proc/stat file and provides necessary information"""
    f = open("/proc/stat").readlines()
    ctxt = ''.join([x for x in f if x.startswith('ctxt')]).split()[1]
    btime = ''.join([x for x in f if x.startswith('btime')]).split()[1]
    process = ''.join([x for x in f if x.startswith('process')]).split()[1]
    process_run = ''.join([x for x in f if x.startswith('procs_running')]).split()[1]
    procs_blocked = ''.join([x for x in f if x.startswith('procs_blocked')]).split()[1]
    d_keys = ['ctxt', 'btime', 'process', 'process_run', 'process_blocked']
    d_val = [ctxt, btime,process, process_run,procs_blocked]
    return [(dict(zip(d_keys,d_val)))]

  def per_procs_status(self):
    """Read /proc/pid/status and returns list of dict_data """
    lpid = []
    d_keys = ['State', 'VmRss', 'VmPeak', 'VmHWM', 'VmSwap','PID', 'CPUused', 'Command']
    pids = self.get_pid()
    for ids in pids:
      try: 
        status = open("/proc/"+ids+"/status").readlines()
        command = open("/proc/"+ids+"/cmdline").read()
        state = ''.join([x for x in status if x.startswith('State')]).strip().split()[1]
        vmrss = ''.join([x for x in status if x.startswith('VmRSS')]).strip().split()[1]
        vmpeak = ''.join([x for x in status if x.startswith('VmPeak')]).strip().split()[1]
        vmhwm =''.join([x for x in status if x.startswith('VmHWM')]).strip().split()[1]
        vmswp =''.join([x for x in status if x.startswith('VmSwap')]).strip().split()[1]
        cpuused = self.get_cpupid(str(ids))
        d_val = [state, vmrss, vmpeak, vmhwm,vmswp,ids,cpuused,command]
        d_data = dict(zip(d_keys, d_val))
        lpid.append(d_data)
 
      except Exception as e:
        pass
    return lpid


  def get_interface(self,file_name):
    self.file_name = file_name
    self.columnLine = self.file_name[1]
    self._, self.receiveCols , self.transmitCols = self.columnLine.split("|")
    self.receiveCols = map(lambda a:"recv_"+a, self.receiveCols.split())
    self.transmitCols = map(lambda a:"trans_"+a, self.transmitCols.split())

    self.cols = self.receiveCols+self.transmitCols

    self.faces = {}
    for line in self.file_name[2:]:
      if line.find(":") < 0: continue
      self.face, self.data = line.split(":")
      self.faceData = dict(zip(self.cols, self.data.split()))
      self.faces[self.face] = self.faceData
    return self.faces


  def get_disk_usge(self):
    """ Returns dict data for df command"""
    dlist = []
    df = subprocess.Popen(["df"], stdout=subprocess.PIPE)
    output =df.communicate()[0].split('\n')
    key,val = output[0], output[1:]
    dkey = key.split()
    for v in  val:
      dval = v.split()
      dlist.append(dict(zip(dkey,dval)))
    dlist.pop()
    return dlist
   

  def get_net_stat_summary(self,filename):
    """ Returns the Dict Data for netstat summary """
    values = {}
    key_data = None
    key_val = None
    with open(filename) as netfile:
      for line in netfile:
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


    return values


  def read_procstat(self):
    """Read /proc/stat file and returns the data in dict """
    p_file = open('/proc/stat','r').readlines()
    ret_list = []
    cpu_list = [core for core in p_file if core.startswith('cpu')]
    key_data = ['CPU', 'user', 'nice', 'system', 'idle', 'iowait', 'irq', 'softirq']
    for c in cpu_list:
      val = c.split()
      dict_data = dict(zip(key_data,val))
      ret_list.append(dict_data)
    return ret_list
    p_file.close()


  def get_cpuused_per_core(self):
    """ Read /proc/stat file and computes cpu used percentage"""
    proc_stat = self.read_procstat()
    cpu_list = ['CPU', 'used','idle']
    ret_list = []
    for line in proc_stat:
      cpu  = line.pop('CPU')
      #cpu_list.append(cpu)
      
      tot_cpu_time = sum(map(float,line.values()))
      #print tot_cpu_time
      tot_cpu_idle = float(line['idle'])+float(line['iowait'])
      total_cpu_usage_since_boot = tot_cpu_time - tot_cpu_idle
      tot_cpu_per = (total_cpu_usage_since_boot/tot_cpu_time)*100
      d_val = [cpu, tot_cpu_per, tot_cpu_idle]
      d_data = dict(zip(cpu_list,d_val))
      ret_list.append(d_data)
    return ret_list

      
  def get_vmstat(self):
    """ Returns the output of vmstat for last 10 seconds """
    vm_list = []
    vm = commands.getoutput("vmstat 1 10 | tail -n+2")
    fil_data = filter(lambda x:x!='', vm.split('\n'))
    row, col = fil_data[0].split(), fil_data[1:]
    for line in col:
      d_data = dict(zip(row,line.split()))
      vm_list.append(d_data)

    return vm_list

  def get_mpstat(self):
    """Returns the output of mpstat """
    mp_list = []
    mpst = commands.getoutput('mpstat -P ALL |cut -f 5')
    fil_data = filter(lambda x:x!='', mpst.split('\n'))
    col =fil_data[1:]
    row = ['Time','PM','CPU','usr','nice','sys','iowait','irq', 'soft','steal','guest','gnice','idle']

    
    
    for c in col:
      c_data=c.split()
      d_data = dict(zip(row, c_data))
      mp_list.append(d_data)

    return mp_list


  def parse_sar_mem(self, command,rows):
    """ Parse sar command for memory usage report and Paging Stat"""
    sar_list = []
    mem_usg = commands.getoutput(command)
    fil_data = filter(lambda x:x!='', mem_usg.split('\n'))
    col =fil_data[1:]
    avg = col.pop()
    for c in col:
      try:
        col_data = c.split()
        col_data.pop(1)
        d_data = dict(zip(rows, col_data))
        sar_list.append(d_data)
      except Exception as e:
        pass
    return sar_list


