from get_sys_info import GetSysStat
import operator
import pprint
f =[]
a= GetSysStat()
b =a.get_pid()
#print b
#print "Printing CPUPID"
#pprint.pprint( dict(sorted(c.iteritems(), key=operator.itemgetter(1), reverse=True)[:10]))

print a.per_procs_status()

#d = a.get_disk_usge()
#for q in d:
  #f.append(q)
#print f
#print c 
#c = a.pre_procs_status()
#print c 
#print a. get_pid_cpu_consuming()
#d = a.alert_system()
#print a.get_cpu_stat()
#cpu_wait = d['cpu']['wa']
#swap_si = d['swap']['si']
#swap_so = d['swap']['so']
#si_cnt =0
#so_cnt =0
#for s in  swap_si:
  #if (s >0):
    #si_cnt = si_cnt+1

#for s in swap_so:
  #if(s > 0):
    #so_cnt = so_cnt+1
    
#if(si_cnt > 5 and so_cnt >5):
  #print "Alert The SYstem is Swapping"

  #try:
    #ids = d['cpu']['id']
    #sy_time = d['cpu']['sy']
    #us_time = d['cpu']['us']
    #ctxt = d['system']['cs']
    #intr = d['system']['in']

    #for ct,intrr in ctxt,intr:
      #if(ct > intrr):
        #print "Alert System is doing More ContextSwitching than Actual Work"

    #for x,y in sy_time, us_time:
      #if(x+y > 1):
        #print "Possible CPU bottelneck"

      #if (x > y):
        #print "System is spending less time on real Work (not good)"
      #if(x > 1):
        #print "Your Application is issuing many system calls to the kernal and asking kernal to work"
  #except Excemtion as e:
    #print e

print a.get_uname()
