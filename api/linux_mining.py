#!/usr/bin/pyhton
import os 
import sys
import pprint
import commands
from collections import namedtuple
class LinuxMining():
  def get_cpu_stat(self, cpufile):
    self.cpufile = cpufile
    self.cpuinfo = {}
    for line in cpufile:
      try:
        self.cpuinfo[line.split(":")[0].strip('\t')]=line.split(":")[1].strip()
      except Exception as e:
        pass
    return self.cpuinfo



  def get_memory_stats(self,mem_file):
    self.meminfo = {}
    self.mem_file = mem_file
    for line in mem_file:
      self.meminfo[line.split(':')[0]] = line.split(':')[1].strip()

    return self.meminfo

  def get_iostat_per_process(self, pid):
     """ Returns the dict data from /proc/$pid/io need sudo access"""
     io_proc = {}
     pid = self.get_pid()
     for ids in pid:
       with open("/proc/"+ids+"/io") as iofile:
         io_porc[iofile.split(':')[0]] = iofile.split[":"][1].strip()
    return io_proc


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


  def proc_stat(self):
    self. si_cnt=0
    self.so_cnt=0
    self.core_list = ['CPU', 'user', 'nice', 'system', 'idle', 'iowait', 'irq', 'softirq']
    self.load_avg = commands.getoutput("uptime|awk '{print $8 $9 $10}'").split(',')
    self.last_five_load_avg = self.load_avg[0]
    self.get_stat = open("/proc/stat", "r").readlines()
    self.cpu =''.join( [cpu for cpu in self.get_stat if cpu.startswith('cpu')]).split('\n')
    #self.no_of_cpu = commands.getoutput("lscpu |grep 'CPU(s)'|awk '{print $2}'").split()[0]
    self.core=self.cpu[1:-1]
    self.no_of_cpu = len(self.core)
    print "Prining length"+str(self.no_of_cpu)
      
    if (self.last_five_load_avg > self.no_of_cpu):
      print "Alert Saturation level exceeded load avrage is "+self.last_five_load_avg 
      self.cpu_swp = {}
      self.cpu_wait =commands.getoutput("vmstat 1 10| awk '{print $16}'").split('\n')[1:]   
      self.swap_si = commands.getoutput("vmstat 1 10| awk '{print $7}'").split('\n')[1:]
      self.swap_so = commands.getoutput("vmstat 1 10| awk '{print $8}'").split('\n')[1:]
      self.cpu_swp['cpu_wait']=self.cpu_wait
      self.cpu_swp['swap_si']=self.swap_si
      self.cpu_swp['swap_so']=self.swap_so
      #return self.cpu_swp
      for s in self.swap_si:
        if (s>0):
          self.si_cnt = self.si_cnt+1

      for so in self.swap_so:
        if(so>0):
          self.so_cnt = self.so_cnt+1
      

      if (self.so_cnt>5 and self.si_cnt>5):
        print "Alert the system is swapping!"
    try:
      self.ids = commands.getoutput("vmstat 1 10| awk '{print $15}'").split('\n')[2:]
      self.sy_time = commands.getoutput("vmstat 1 10| awk '{print $14}'").split('\n')[2:]
      self.us_time = commands.getoutput("vmstat 1 10| awk '{print $13}'").split('\n')[2:]
      self.ctx = commands.getoutput("vmstat 1 10| awk '{print $12}'").split('\n')[2:]
      self.intr = commands.getoutput("vmstat 1 10| awk '{print $11}'").split('\n')[2:]
      for ct,inr in (self.ctx, self.sy_time):
        if(ct >inr):
          print "System is doing more context switching than actual work."
 
      for x,y in (self.sy_time,self.us_time):
        if (x+y >1):
          print "possible CPU bottleneck"
        if (x>y):
          print "System is spending less time on real work (not good)"
        if(x>1):
          print "Your application is issuing many system calls to the kernel and asking the kernel to work"
          
    except Exception as e:
      pass
    self.ctxt = ''.join( [cpu for cpu in self.get_stat if cpu.startswith('ctxt')]).split()[1]
    self.btime = ''.join( [cpu for cpu in self.get_stat if cpu.startswith('btime')]).split()[1]
    self.process = ''.join( [cpu for cpu in self.get_stat if cpu.startswith('processes')]).split()[1]
    self.procs_run = ''.join( [cpu for cpu in self.get_stat if cpu.startswith('procs_running')]).split()[1]
    self.procs_blocked=''.join( [cpu for cpu in self.get_stat if cpu.startswith('procs_blocked')]).split()[1]

    print "The total number of context switches across all CPUs: "+''.join(self.ctxt)+'\n'
    print "The time at which the system booted, in seconds since the Unix epoch :"+''.join(self.btime)+'\n'
    print "number of processes and threads created, which includes those created by calls to the fork() and clone() system calls:"+''.join(self.process)+'\n'
    print "The number of processes currently running on CPUs:"+''.join(self.procs_run)+'\n'
    print "The number of processes currently blocked, waiting for I/O to complete:"+''.join(self.procs_blocked)+'\n'
    for c_data in self.core:
      self.d_data = {}
      try:
        self.cpu_info = dict(zip(self.core_list, '\n'.join(c_data.strip('\n').split('\n')).split()))
      except:
        pass
    self.cpu_info["cpu_swap"]=self.cpu_swp
    return self.cpu_info
    self.per_util = commands.getoutput("iostat -x 5 > io.txt")
    self.util = commands.getoutput("tail -n+5| awk'{print $ 14}'").strip('\n').split()
    for u in self.util[1:]:
      if(float(u)==100.0):
        print "The device is being hit hard"
       
  def get_pid_cpuusage(self):
    self.per_cpu = {}
    lpid = []
    lcmd=[]
    self.pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]
    for id in self.pids:
      self.pid_cpu = commands.getoutput("ps -p"+id+" "+"-o %cpu").strip('\n').split()[1]
      self.cmds = commands.getoutput("cat /proc/"+id+"/cmdline").strip('\n')
      lpid.append(self.pid_cpu)
      lcmd.append(self.cmds)     
      try:
        if(pid):
          self.per_cpu = dict(zip(lpid, lcmd))
      except:
        pass
    return  self.per_cpu
  def get_disk_usge(self):
    self.DiskUsage = namedtuple('DiskUsage',  ' device mounts fstype total used free percent')
    self.disk_info =namedtuple('partition', 'device mountpoint fstype') 
    self.f = open('/etc/mtab', 'r')
    self.dlist = []
    for line in self.f:
      if line.startswith('none'):continue
      self.device = line.split()[0]
      self.mountpoint = line.split()[1]
      self.fstype = line.split()[2]
      self.dtuple = self.disk_info(self.device, self.mountpoint, self.fstype)
      self.dlist.append(self.dtuple)
     
    for  item in self.dlist:
      st = os.statvfs(item.mountpoint)
      free = st.f_bavail * st.f_frsize
      total = st.f_blocks * st.f_frsize
      used = (st.f_blocks - st.f_bfree) * st.f_frsize
      try:
        percent =  (float(used) / total) * 100
      except ZeroDivisionError:
        percent = 0
      print  self.DiskUsage(item.device,item.mountpoint, item.fstype,total, used, free, round(percent, 1))

