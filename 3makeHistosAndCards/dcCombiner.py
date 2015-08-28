
#datacards to be combined
infiles=[#"datacard_HCSVSingleGenerousV2.txt",
         "output/datacard_43_KITOPT.txt",
         "output/datacard_44_KITOPT.txt",
         "output/datacard_53_KITOPT.txt",
         "output/datacard_54_KITOPT.txt",
         "output/datacard_62_KITOPT.txt",
         "output/datacard_63_KITOPT.txt",
         "output/datacard_64_KITOPT.txt",
]
          
# path to resulting datacard
outfile=open("output/datacard_Combined_KITOPT_All.txt","w")

# you have to specify the number of samples and systematics here
nSys=17
nSamples=6

#-------------------------------------------------------
# acutally do the stuff

filehandles=[]
lineheader=[]
lines=[]

for inf in infiles:
  filehandles.append(open(inf,"r"))
#print filehandles 

for file in filehandles:
  lines.append(list(file))
  file.close()

newlines=[]
buffline=lines[0][0].split(" ",2)
print buffline
nchannels=int(buffline[1])
for i in range(1,len(infiles)):
  buff=lines[i][0].split(" ",2)
  nchannels+=int(buff[1])
buffline[1]=str(nchannels)
newlines.append(buffline[0]+" "+buffline[1]+" "+buffline[2])

newlines.append(lines[0][1])
newlines.append(lines[0][2])
newlines.append(lines[0][3])
#bin
buffline=lines[0][4].rstrip("\n")
print buffline
for i in range(1,len(infiles)):
  buff=lines[i][4].split("\t",1)
  print buff
  buffline+="\t"+buff[1].rstrip("\n")
buffline+="\n"
newlines.append(buffline)

#observation
buffline=lines[0][5].rstrip("\n")
print buffline
for i in range(1,len(infiles)):
  buff=lines[i][5].split("\t",1)
  print buff
  buffline+="\t"+buff[1].rstrip("\n")
buffline+="\n"
newlines.append(buffline)

#shapes
for i in range(0,len(infiles)):
  newlines.append(lines[i][6])
  buff=lines[i][6].split("\t",3)
  buff2 = lines[i][7].split("\t",3)
  buffline=buff2[0]+"\t"+buff2[1]+"\t"+buff[2]+"\t"+buff2[3]+"\n"
  newlines.append(buffline)

newlines.append(lines[0][8])

for k in range(4):
  buffline=lines[0][k+9].rstrip("\n")
  print buffline
  for i in range(1,len(infiles)):
    buff=lines[i][k+9].split("\t",1)
    print buff
    buffline+="\t"+buff[1].rstrip("\n")
  buffline+="\n"
  newlines.append(buffline)

newlines.append(lines[0][13])

for k in range(nSys):
  buffline=lines[0][k+14].rstrip("\n")
  print buffline
  for i in range(1,len(infiles)):
    buff=lines[i][k+14].split("\t",2)
    print buff
    buffline+="\t"+buff[2].rstrip("\n")
  buffline+="\n"
  newlines.append(buffline)

print "do stat shapes"

for i in range(len(infiles)):
  for k in range(14+nSys, len(lines[i])):
    buffline=lines[i][k].rstrip("\n")
    print buffline
    buff=buffline.split("\t",2)
    print buff
    buff2=buff[0]+"\t"+buff[1]+"\t"
    for j in range(len(infiles)):
      if j==i:
        buff2+=buff[2]
      else:
        for l in range(nSamples):
          buff2+="-\t"
    buff2+="\n"
    newlines.append(buff2)
    
    
    
print newlines

for lines in newlines:
  outfile.write(lines)
  
outfile.close()
print "datacards combined"
#lines.append(list(filehandles[0]))
#lines.append(list(filehandles[1]))
#print int(lines[0][5].split("\t",1))
