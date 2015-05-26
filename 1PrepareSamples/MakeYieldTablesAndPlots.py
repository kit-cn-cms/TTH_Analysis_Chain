import ROOT
from array import array
import Categorization
import sys
from datetime import date
from subprocess import call
from subprocess import check_output


DoDebugMode=False


if not len(sys.argv)==4 :
  print "usage:"
  print "MakeYieldTablesAndPlotsFromTrees.py ANALYSIS_LOG|DIRECTORY_FOR_INPUT_TREES OUTPUT_DIRECTORY CATEGORY_DEFINITION"
  exit(0)

cwd=sys.path[0]
print cwd
logOrPath = sys.argv[1]
outPath=sys.argv[2]
CatDefFile=sys.argv[3]
hasLog=False
logfile=""
if ".txt" in logOrPath:
  logfile=logOrPath
  hasLog=True
else:
  indir=check_output(["dir","-1",logOrPath]).splitlines()
  for f in indir:
    if "AnalysisLog.txt" in f:
       hasLog=True
       print "found AnalysisLog.txt in input directory"
       break
  if hasLog==True:
    logfile=logOrPath+"/AnalysisLog.txt"
  else:
    hasLog=False 
    print "did not find AnalysisLog.txt"
    print "will us every Tree in input directory"

loglines=[]
if hasLog==True:
  log=open(logfile,"r")
  loglines=list(log)
  log.close()

#call(["mkdir",outPath+"/AnalysisConfigs"])
#newCatDefFileName=outPath+"/AnalysisConfigs/"+CatDefFile.rsplit("/",1)[1]
#call(["cp",CatDefFile,outPath+"/AnalysisConfigs/."])

#find the samples and their trees
inTrees=[]
if hasLog==True:
  firstIndex=0
  for l in loglines:
    if "Trees slimmend" in l:
      firstIndex=loglines.index(l)
  for l in loglines[firstIndex:]:
    if "root" in l:
      buff=l.rsplit("\n",1)[0]
      inTrees.append(buff)
else:
  indir=check_output(["dir","-1",logOrPath]).splitlines()
  for f in indir:
    if ".root" in f:
      inTrees.append(logOrPath+"/"+f)

print "input Trees ",inTrees, "\n"


print "setting up Categorization of the events"
Categorizer=Categorization.Categorizer(CatDefFile,outPath,DoDebugMode)

if hasLog==False:
  for tree in inTrees:
    Categorizer.OnlyGetYieldsFast(tree)
else:
  Categorizer.ReadCategoryYieldsFromLogLines(loglines)

print "done\n"
#create tables with yields
print "Creating yield tables"
Categorizer.MakeYieldTables()
#create plots
print "making Yields plot"
Categorizer.MakeYieldPlots()
