import commands, pprint
command = 'ss -tp'
l = []
d = {}
com_data = commands.getoutput(command)
fil_data = filter(lambda x:x !='', com_data.split('\n'))
row_col=map(lambda x:x.strip().split(),fil_data)
rows,col = row_col[0],row_col[1:]
#rows[0] = "Time"
#parse_data = {k:v for (k,v) in zip(rows,zip(*col))}

row  = ['state', 'recvq', 'sendq', 'locad', 'remad', 'addm']
for c in col:
  st =  c[0]
  rq =c[1].strip()
  sq= c[2].strip()
  lad= c[3].strip()
  rad = c[4].strip()
  adm = c[5].strip()
  val  = [st,sq,rq,lad,rad,adm]
  d [row] = [v for v in val ] 
  l.append(d)

print l

