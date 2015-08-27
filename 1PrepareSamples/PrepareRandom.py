import ROOT
from array import array
import Categorization
import sys
from datetime import date
from subprocess import call
from subprocess import check_output


DoDebugMode=False

if len(sys.argv)!=4:
  print "usage:"
  print "PrepareSamples.py ANALYSIS_LOG|DIRECTORY_WITH_SLIM_TREES DIRECTORY_FOR_PREPARED_TREES CATEGORY_DEFINITION"
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

call(["mkdir",outPath+"/AnalysisConfigs"])
newCatDefFileName=outPath+"/AnalysisConfigs/"+CatDefFile.rsplit("/",1)[1]
call(["cp",CatDefFile,outPath+"/AnalysisConfigs/."])

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

loglines.append("\n------------------------------------------------------------------\n")
loglines.append("\nAnalysis Path\n")
loglines.append(outPath)
loglines.append("\n")
loglines.append("Category Definitions in\n")
loglines.append(newCatDefFileName)
loglines.append("\n")
loglines.append("Categorized on "+str(date.today())+"\n")
loglines.append("\n")


##first split the ttbar sample in different flavors
print "\n identifying the ttbar trees"
ttbarSampleTrees=[]
nonttbarSampleTrees=[]
for i, tree in enumerate(inTrees):
  if "ttbar" in tree and not "_l_" in tree and not "_bb_" in tree and not "_b_" in tree and not "_cc_" in tree and not "_2b_" in tree:
    ttbarSampleTrees.append(tree)
  else:
    nonttbarSampleTrees.append(tree)
#print ttbarSampleTrees
inTrees=nonttbarSampleTrees


for ttbarSample in ttbarSampleTrees:
  flavSamples=Categorizer.SplitTTbarFlavor(ttbarSample)
  #print flavSamples
  inTrees+=flavSamples


print "done with flavor splitting\n"
print "splitting in categories"
#loop over input samples an split them into the categories
for tree in inTrees:
  Categorizer.SplitInCategoriesRandom(tree)


#make MCData.root
print "creating MCData.root files"
Categorizer.CreateMCData()
Categorizer.ReAddTheTTbarTrees()

#create tables with yields
print "Trees are done"
print "\n ---------------------------------------------------"
#print "Creating yield tables"
#Categorizer.MakeYieldTables()
#create plots
#print "making Yields plot"
#Categorizer.MakeYieldPlots()
##wirte log
#print "Writig AnalysisLog"
#Categorizer.AppendStuffToLogLines(loglines)
#outLog=open(outPath+"/AnalysisConfigs/"+logfile.rsplit("/",1)[1],"w")
#for l in loglines:
  #outLog.write(l)
#outLog.close()

#pack and copy software
#call(["tar","-a","-cf",outPath+"/AnalysisConfigs/AnalysisSoftware.tar.gz",cwd.rsplit("/",1)[0]])