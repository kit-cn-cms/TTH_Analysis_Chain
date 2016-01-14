import ROOT
from array import array
import Categorization
import sys
from datetime import date
from subprocess import call
from subprocess import check_output


DoDebugMode=False

CatDefFile="/nfs/dust/cms/user/kelmorab/limitstudies0111/pyroot-plotscripts/forLimit/1PrepareSamples/ljetscategories.txt"
#insamples=["/nfs/dust/cms/user/kelmorab/treesMEM/ttHbb","/nfs/dust/cms/user/kelmorab/treesMEM/ttHnonbb","/nfs/dust/cms/user/kelmorab/treesMEM/ttbar"]
insamples=["/nfs/dust/cms/user/kelmorab/treesMEM/ttHbb","/nfs/dust/cms/user/kelmorab/treesMEM/ttHnonbb","/nfs/dust/cms/user/kelmorab/treesMEM/ttbar"]
intreenames=["ttHbb_*_nominal_Tree.root","ttHnonbb_*_nominal_Tree.root","ttbar_*_nominal_Tree.root"]
outPath="/nfs/dust/cms/user/kelmorab/treesMEM/output"
weight="Weight*2.54*2*(Evt_Odd==0)"


print "setting up Categorization of the events"
Categorizer=Categorization.Categorizer(CatDefFile,outPath,DoDebugMode)

for sample,treename in zip(insamples,intreenames):
  Categorizer.OnlyGetYieldsFastChain(sample,treename,weight)

print "done\n"
#create tables with yields
print "Creating yield tables"
Categorizer.MakeYieldTables()
#create plots
print "making Yields plot"
Categorizer.MakeYieldPlots()
