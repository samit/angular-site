import subprocess
import os
import csv
def main():
  p = subprocess.Popen("vmstat 1 10", stdout=subprocess.PIPE ,  stderr=subprocess.PIPE , shell=True)
  out = str(p.stdout.read())
  #file_vmstat =  open("vmstat.txt", "rw+")
  #file_vmstat.write(out)
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
  #print "\nThe minor headers read from the file"
  print content
  #print "\nThe CPU user process stats"
  #print content['cpu']['us']
  #print "\nMinimum free memory in the data set"
  #print min(content['memory']['free'])
  #print "\nMaximum IO, either input or output"
  #print max([max(l) for l in content['io'].values()])
  #print content
if __name__ =="__main__":
  main()

