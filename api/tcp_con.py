#!/usr/bin/python
import os, socket,struct
from collections import namedtuple
import commands
import glob, re
def get_con_stat(filename):
  tcp_list = []
  pid_list = []
  fname = open(filename, 'r').readlines()
  net_file = [line.strip('\\ \n \\') for line in fname if line!='']
  #net = (net[i] for i in xrange(0, len(net_file), 12))
  for net in net_file[1:]:
    local_address= net.split(':')[1:]
    #print net
    lpra = ''.join(local_address[1]).split(' ')
    l_port = lpra[0]
    rem_ad = lpra[1]
    loc_ad = local_address[0]
    print loc_ad
    #print l_port
    rqsq = ''.join(local_address[2]).split(' ')
    rxtx = ''.join(local_address[3]).split(' ')
    rxque = str(int(rxtx[0],16))
    tm = rxtx[1]
    tmret = ''.join(local_address[4]).split()
    tm_when=tmret[0]
    retrnsmt= tmret[1]
    uid= tmret[2]
    timeout=tmret[3]
    inode = tmret[4]
    for item in glob.glob('/proc/[0-9]*/fd/[0-9]*'):
      try:
        if re.search(inode,os.readlink(item)): 
          pd = item.split('/')[2]
          cmd = commands.getoutput('cat /proc/'+pd+'/cmdline')
          pid_list.append(cmd)
      except:
        pass
    #print pid_list
    sock_ref_count =''.join(tmret[5])
    loc_sock_mem = ''.join(tmret[6])
    rettout= ''.join(tmret[7])
    del_ack_ctrl = ''.join(tmret[8])
    ackquick = ''.join(tmret[9])
    s_cog_win = ''.join(tmret[10])
    sl_st_sz = ''.join(tmret[11])
    #print sock_ref_count+' '+loc_sock_mem+' '+rettout+' '+ackquick+' '+del_ack_ctrl+' '+s_cog_win+' '+sl_st_sz
    #print uid+timeout+inode
    r_port = rqsq[0]
    status_st = rqsq[1]
    tx_queue = rqsq[2]
    rem_port = str(int(r_port,16))
    tx_queue = str(int(tx_queue,16))
    if(loc_ad == None and rem_ad ==None):continue
    l_ad = str(int(loc_ad,16))
    l_port = str(int(l_port,16))
    try:
      lad =  socket.inet_ntoa(struct.pack('!L', int(l_ad))).split('.')
      rad = socket.inet_ntoa(struct.pack('!L', int(rem_ad)))
      lad = '.'.join(lad[::-1])
    except Exception as e:
      pass
  #print pid_list
  #print "Printing CPAM info"
  #print sock_ref_count+' '+loc_sock_mem+' '+rettout+' '+ackquick+' '+del_ack_ctrl+' '+s_cog_win+' '+sl_st_sz
def main():
  filename= '/proc/net/tcp'
  get = get_con_stat(filename)
  

if __name__=='__main__':
  main()
