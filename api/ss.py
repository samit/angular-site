import commands
import pprint
command = ['ss -tp', 'ss -up', 'mpstat -P ALL |cut -f 5', 'vmstat 1 10| tail -n+2', 'sar -d |cut -f 5']
for c in command:
  com_data = commands.getoutput(c)
  fil_data = filter(lambda x:x !='', com_data.split('\n'))
  row_col=map(lambda x:x.strip().split(),fil_data)
  rows,col = row_col[0],row_col[1:]
  parse_data = {k:v for (k,v) in zip(rows,zip(*col))}
  pprint.pprint(parse_data)
