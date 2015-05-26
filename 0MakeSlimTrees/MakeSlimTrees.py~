from subprocess import call
import sys
from datetime import date

print len(sys.argv)
if not (len(sys.argv)==3 or len(sys.argv)==4):
  print "usage:"
  print "MakeSlimTrees.py PATH_TO_MOTHER_TREES TARGET_PATH_TO_SLIMMED_TREES [ANALYSIS_LOG]"
  exit(0)

inPath=sys.argv[1]
outPath=sys.argv[2]
logfile=""
if len(sys.argv)==4:
  logfile=sys.argv[3]

print inPath
print outPath

if logfile!="":
  log=open(logfile,"r")
else:
  log=open(inPath+"/AnalysisLog.txt","r")
  
loglines=list(log)
log.close()

#find the samples and their trees
firstIndex=0
for l in loglines:
  if "hadded" in l:
    firstIndex=loglines.index(l)
#print firstIndex

inTrees=[]
for l in loglines[firstIndex:]:
  if "root" in l:
    buff = l.rsplit("/",1)[1]
    #print buff
    buff=buff.rsplit("\n",1)[0]
    print buff
    inTrees.append(buff)

print inTrees

loglines.append("\n------------------------------------------------------------------\n")
loglines.append("MotherTrees "+str(inPath)+"\n")
loglines.append("Trees slimmend on "+str(date.today())+"\n\n")
#slim the Trees
for t in inTrees:
  sn=t.replace(".root","")
  command = "slimTheTrees.C+(\""+sn+"\",\""+inPath+"/"+t+"\",\""+outPath+"/"+"\")"
  call(["root","-b","-q",command])
  loglines.append(outPath+"/"+t+"\n")
  #exit(0)

newlog=open(outPath+"/AnalysisLog.txt","w")
for l in loglines:
  newlog.write(l)
newlog.close()

print "all Trees slimmed and written to "+outPath