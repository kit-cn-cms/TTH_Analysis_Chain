import ROOT
from array import array
from subprocess import call
import time as timer
import sys

datacard= sys.argv[1]
currentPath = sys.path[0]

minmu=0.0
maxmu=7.0
nSteps=350
nToysBatch=500
nIterations=6
nJobs=175

stepsPerJob=nSteps/nJobs

deltamu=maxmu-minmu
stepsize=deltamu/float(nSteps)

currentmu=minmu
seed=200

runfile=open("runAll.sh","w")
runfile.write("#!/bin/bash\n")

for job in range(nJobs):
  point=minmu+job*stepsize
  jobfile=open("ToyMC"+str(job)+".sh" ,"w")
  jobfile.write("#!/bin/bash\n")
  jobfile.write(". /etc/profile.d/modules.sh\n")
  jobfile.write("module use -a /afs/desy.de/group/cms/modulefiles/\n")
  jobfile.write("module load cmssw/slc6_amd64_gcc491\n")
  jobfile.write("export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch/\n")
  jobfile.write("export SCRAM_ARCH=slc6_amd64_gcc491\n")
  jobfile.write("source $VO_CMS_SW_DIR/cmsset_default.sh\n")
  jobfile.write("cd /afs/desy.de/user/k/kelmorab/CMSSW_7_4_6_patch6/src\n")
  jobfile.write("eval `scram runtime -sh`\n")
  jobfile.write("cd "+currentPath+"/\n")
  
  for step in range(stepsPerJob):
    currentmu+=stepsize
    seed+=1
    #jobfile.write("/afs/desy.de/user/k/kelmorab/CMSSW_7_4_6_patch6/bin/slc6_amd64_gcc491/combine "+datacard+" -M HybridNew  --frequentist --testStat LHC --clsAcc 0 -T "+str(nToysBatch)+" -i "+str(nIterations)+" -s "+str(seed)+" --singlePoint "+str(currentmu)+" --saveToys --saveHybridResult\n")
    jobfile.write("/afs/desy.de/user/k/kelmorab/CMSSW_7_4_6_patch6/bin/slc6_amd64_gcc491/combine "+datacard+" -M HybridNew  --generateExternalMeasurements 1 --generateNuisances 0 --testStat LHC --clsAcc 0 -T "+str(nToysBatch)+" -i "+str(nIterations)+" -s "+str(seed)+" --singlePoint "+str(currentmu)+" --fullBToys  --saveToys --saveHybridResult\n")
    print "wrote job ", str(job), "with point ", str(currentmu)
  jobfile.close()


for job in range(nJobs):
  runfile.write("qsub -l h=bird* -hard -l os=sld6 -l h_vmem=2000M -l s_vmem=2000M -l cvmfs -cwd -S /bin/bash -o "+currentPath+"/logs/\$JOB_NAME.o\$JOB_ID -e logs/\$JOB_NAME.e\$JOB_ID -q 'default.q' ToyMC"+str(job)+".sh\n")

runfile.close()

# after all jobs are finished do
# hadd the single output files to mygrid.root
# combine datacard_Combined_ThesisSTD.txt -M HybridNew --testStat LHC  --generateExternalMeasurements 1 --generateNuisances 0 --grid=mygrid.root  --expectedFromGrid 0.5
# for median prefit expected

