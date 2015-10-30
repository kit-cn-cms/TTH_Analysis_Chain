from trainer import Trainer
from evaluaterRun2 import Evaluater
from evaluaterRun2 import Systematic
from evaluaterRun2 import Sample
from subprocess import call
from SampleScaleGetter import *

import sys
import json

print len(sys.argv)
if len(sys.argv)<6 or len(sys.argv)>6:
  print "usage:"
  print "python TrainAndEval.py CATEGORY NAME FINALBDTCONFIG_FILE INPUTPATH [test | train]"
  print "\n"
  print "CATEGORY = for example 43 or 62 or DB or so "
  print "NAME = name of outputfiles "
  print "FINALBDTCONFIG_FILE = BDT config file e.g. see example files "
  print "INPUTPATH = path to input trees prepared in ../1PrepareSamples. Has to contain directories called Category_*/* "
  print "[test | train] = do limit on test or trainings samples "
  print "\n output is out in ./output/"
  exit(0)
  
category=sys.argv[1]
name=sys.argv[2]
FinalBDTConfig=sys.argv[3]
TestOrTrainSwitch=sys.argv[5]
if TestOrTrainSwitch=="train":
  doTestonTrain=True
else:
  doTestonTrain=False

AnaPath=sys.argv[4]
SubBDTConfig="NONE"

print category
print name
print FinalBDTConfig
print SubBDTConfig

f = open("output/TrainAndEval_"+name+".txt","w")

evaluationPath=AnaPath+"/Category_"+category+"/Even/"
trainingPath=AnaPath+"/Category_"+category+"/Odd/"


if doTestonTrain:
  print "!!!!!!!!!!DOING EVALUATION ON TRAINING SAMPLE!!!!!!!!"

variablesFinal=[]

## these lines are used for a sub BDT chained before the final BDT, for example for ttbb
#if SubBDTConfig=="NONE":
  #SubBDTConfig="SubBDT_Config_Default.txt"
  #variablesSub=['H3', 'MaxAbsEta_Jet', 'Deta_TopHadCandidate_HiggsCandidate_TopLikelihood', 'M2_HiggsCandidate_TopLikelihood', 'M_2TaggedJetsAverage', 'Subjetiness21_HiggsCandidate_TopLikelihood']
  #ntrees_SBDT, shrinkage_SBDT, baggingfraction_SBDT, nCuts_SBDT, maxDepth_SBDT = 100, 0.01, 0.6, 10, 2
  #buffername="output/SubBDT_Config_"+category+"_"+name+".txt"
  #call(['cp', './SubBDT_Config_Default.txt',buffername])
#SBDTConfigFile=open(SubBDTConfig,"r")
#SBDTConfigList=list(SBDTConfigFile)
##splitlist=SBDTConfigList[0].split(" ")
#for line in SBDTConfigList:
   #if "variables" in line:
     #line=line.split("=",1)
     #print line
     #variablesSub=json.loads(line[1])
     #print variablesSub
   #if "BDTOptions" in line:
     #line=line.split("=",1)
     #print line
     #SubBDTOptions=json.loads(line[1])
     #print SubBDTOptions
#buffername="output/SubBDT_Config_"+category+"_"+name+".txt"
#call(['cp', './'+SubBDTConfig,buffername])

FBDTConfigFile=open(FinalBDTConfig,"r")
FBDTConfigList=list(FBDTConfigFile)
#splitlist=FBDTConfigList[0].split(" ")
for line in FBDTConfigList:
   if "variables" in line:
     line=line.split("=",1)
     #print line
     line=line[1].strip().replace("\'","\"")
     print type(line), line
     variablesFinalbuffer=json.loads(line)
     #print variablesFinal
   if "BDTOptions" in line:
     line=line.split("=",1)
     print line
     FinalBDTOptions=line[1]
     print FinalBDTOptions
buffername="output/FinalBDT_Config_"+category+"_"+name+".txt"
call(['cp', './'+FinalBDTConfig,buffername])

f.write("TrainingsPath: "+trainingPath+"\n")
f.write("EvalPath: "+evaluationPath+"\n\n")

for var in variablesFinalbuffer:
  variablesFinal.append(str(var))

#print type(variablesFinal), variablesFinal, variablesFinal[2], type(variablesFinal[2])
#print variablesFinal[2], type(variablesFinal[2]), str(variablesFinal[2]), type(str(variablesFinal[2]))

## these lines are used for a sub BDT chained before the final BDT, for example for ttbb
#f.write("SubBDT Variables:\n")
#f.write(str(variablesSub)+"\n")

f.write("FinalBDT Variables:\n")
f.write(str(variablesFinal)+"\n\n")

## these lines are used for a sub BDT chained before the final BDT, for example for ttbb
#print "Training SubBDT"
#trainerSub=Trainer(trainingPath+"tth_nominal.root",trainingPath+"tbar_nominal.root",SubBDTOptions,variablesSub,[],False,"weights/weights_Sub.xml")
#trainerSub.useTransformations(False)
#trainerSub.setWeightExpression("Weight_XS")
##trainerSub.run(variablesSub, 2000,0.001,0.5, 40,2)
#trainerSub.run(variablesSub,SubBDTOptions)
#f.write("SubBDT Parameters:\n")
#f.write(SubBDTOptions+"\n\n")
#samplesTrainingSub=[Sample("tth",trainingPath+"tth_nominal.root",-1,1.),Sample("ttbar_nominal",trainingPath+"Training_ttbar_bb.root",.5,1.),Sample("ttbar_b",trainingPath+"Training_ttbar_b.root",.5,1.),Sample("ttbar_cc",trainingPath+"Training_ttbar_cc.root",.5,1.),Sample("ttbar_light",trainingPath+"Training_ttbar_l.root",.5,1.),Sample("ttbar",trainingPath+"Training_ttbar.root",.1,1.)]
#print "Writing SubBDT output"
#weightfileSub=trainerSub.weightfile
#evaluaterSub=Evaluater(weightfileSub,variablesSub,samplesTrainingSub,[],[])
#evaluaterSub.WriteBDTVars("","_SubBDT","Sub")

print "Training Final BDT"
trainerFinal=Trainer(trainingPath+"tth_nominal.root",trainingPath+"ttbar_nominal.root",evaluationPath+"tth_nominal.root",evaluationPath+"ttbar_nominal.root",FinalBDTOptions,variablesFinal,[],False,"weights/weights_Final_"+category+"_"+name+".xml")
trainerFinal.useTransformations(False)
trainerFinal.setWeightExpression("Weight_XS")
trainerFinal.run(variablesFinal,FinalBDTOptions)

f.write("FinalBDT Parameters:\n")
f.write(FinalBDTOptions+"\n\n")
f.close()

samplesTrainingFinal=[Sample("tth",trainingPath+"tth_nominal.root",-1,1.),Sample("ttbar_light",trainingPath+"ttbar_l_nominal.root",.1,1.),Sample("ttbar_b",trainingPath+"ttbar_b_nominal.root",.5,1.),Sample("ttbar_bb",trainingPath+"ttbar_bb_nominal.root",.5,1.),Sample("ttbar_2b",trainingPath+"ttbar_2b_nominal.root",.5,1.),Sample("ttbar_cc",trainingPath+"ttbar_cc_nominal.root",.5,1.),Sample("ttbar",trainingPath+"ttbar_nominal.root",.1,1.),Sample("SingleT",trainingPath+"SingleT_nominal.root",0.031,1.),Sample("DiBoson",trainingPath+"DiBoson_nominal.root",0.07,1.),Sample("ttW",trainingPath+"ttW_nominal.root",0.139,1.),Sample("ttZ",trainingPath+"ttZ_nominal.root",0.124,1.)]
dataTrain=Sample("data",trainingPath+"MCData.root",-1,1.)

print "Writing FinalBDT output"
weightfileFinal=trainerFinal.weightfile
evaluaterFinal=Evaluater(weightfileFinal,variablesFinal,samplesTrainingFinal,[],[])
evaluaterFinal.WriteBDTVars("","_FinalBDT","Final")

## plot scripts deprecated
#print "plotting BDTTraining"
#command = "PlotBDTTraining.C+(\"" + trainingPath + "\",\"" + name + "\",\"BDTTraining\")"
##call(['root', '-b','-q','PlotBDTTraining.C+(trainingPath,name,"BDTTraining")'])
#call(['root', '-b','-q',command])
#plotname = "output/BDTTraining_"+name+".pdf"
#rootname = "output/BDTTraining_"+name+".root"
#call(['cp', './BDTTraining.pdf',plotname])
#call(['cp', './BDTTraining.root',rootname])
#call(['root', '-b','-q','PlotTraining.C+'])
#plotname = "output/PlotTraining_"+name+".pdf"
#call(['cp', './PlotTraining.pdf',plotname])

## these lines are used for a sub BDT chained before the final BDT, for example for ttbb
# evaulate the other sample 
#samplesEvalSub=[Sample("tth",evaluationPath+"tth.root",-1,1.),Sample("ttbar_bb",evaluationPath+"ttbar_bb.root",.5,1.),Sample("ttbar_b",evaluationPath+"ttbar_b.root",.5,1.),Sample("ttbar_cc",evaluationPath+"ttbar_cc.root",.5,1.),Sample("ttbar_light",evaluationPath+"ttbar_l.root",.1,1.),Sample("ttbar",evaluationPath+"ttbar.root",.1,1.),Sample("SingleT",evaluationPath+"SingleT.root",.0,1.),Sample("WJets",evaluationPath+"WJets.root",.0,1.),Sample("ZJets",evaluationPath+"ZJets.root",.0,1.),Sample("DiBoson",evaluationPath+"DiBoson.root",.0,1.)]
#print "Writing SubBDT output to Evaluation Samples"
#weightfileEvalSub=trainerSub.weightfile
#evaluaterEvalSub=Evaluater(weightfileSub,variablesSub,samplesEvalSub,[],[])
#evaluaterEvalSub.WriteEvalBDTVars("","_SubBDT","Sub")

#dname=evaluationPath+"MCData.root"
#sname=evaluationPath+"tth_SubBDT.root"
#bname=evaluationPath+"ttbar_SubBDT.root"
#bname2=evaluationPath+"SingleT_SubBDT.root"
#bname3=evaluationPath+"DiBoson_SubBDT.root"
#bname4=evaluationPath+"WJets_SubBDT.root"
#bname5=evaluationPath+"ZJets_SubBDT.root"

#call(['rm', '-f', dname])
#call(['hadd','-f2',dname,sname,bname,bname2,bname3,bname4,bname5])
print "doing eval samples"

if doTestonTrain:
  print "!!!!!!!!!!DOING EVALUATION ON TRAINING SAMPLE!!!!!!!!"
  bufferpath=evaluationPath
  evaluationPath=trainingPath
  trainingPath=bufferpath
  print trainingPath
  print evaluationPath
  print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"

samplesTrainingForScales=[Sample("tth",trainingPath+"tth_nominal.root",-1,1.),Sample("ttbar_light",trainingPath+"ttbar_l_nominal.root",.1,1.),Sample("ttbar_b",trainingPath+"ttbar_b_nominal.root",.618,1.),Sample("ttbar_bb",trainingPath+"ttbar_bb_nominal.root",.618,1.),Sample("ttbar_2b",trainingPath+"ttbar_2b_nominal.root",.618,1.),Sample("ttbar_cc",trainingPath+"ttbar_cc_nominal.root",.618,1.),Sample("SingleT",trainingPath+"SingleT_nominal.root",0.031,1.),Sample("DiBoson",trainingPath+"DiBoson_nominal.root",0.07,1.),Sample("ttW",trainingPath+"ttW_nominal.root",0.139,1.),Sample("ttZ",trainingPath+"ttZ_nominal.root",0.124,1.)]
dataTrainForScales=Sample("data",trainingPath+"MCData.root",-1,1.)

samplesTest=[Sample("tth",evaluationPath+"tth_nominal.root",0.097,1.),Sample("ttbar_light",evaluationPath+"ttbar_l_nominal.root",-1,1.),Sample("ttbar_b",evaluationPath+"ttbar_b_nominal.root",0.618,1.),Sample("ttbar_bb",evaluationPath+"ttbar_bb_nominal.root",0.618,1.),Sample("ttbar_2b",evaluationPath+"ttbar_2b_nominal.root",0.618,1.),Sample("ttbar_cc",evaluationPath+"ttbar_cc_nominal.root",0.618,1.),Sample("SingleT",evaluationPath+"SingleT_nominal.root",0.031,1.),Sample("DiBoson",evaluationPath+"DiBoson_nominal.root",0.07,1.),Sample("ttW",evaluationPath+"ttW_nominal.root",0.139,1.),Sample("ttZ",evaluationPath+"ttZ_nominal.root",0.124,1.)]
dataTest=Sample("data",evaluationPath+"MCData.root",-1,1.)

samplesEval=GetSampleScales(samplesTrainingForScales,samplesTest)
#data=GetSampleScales([dataTrainForScales],[dataTest])
#data=data[0]
data=dataTest

systematics=[
             Systematic("CMS_scale_j","CMS_scale_jUp","_JESUP","","CMS_scale_jDown","_JESDOWN",""),
             Systematic("CMS_res_r","CMS_res_rUp","_JERUP","","CMS_res_rDown","_JERDOWN",""),
             Systematic("CSVLF","CSVLFUp","","Weight_CSVLFup","CSVLFDown","","Weight_CSVLFdown"),
             Systematic("CSVHF","CSVHFUp","","Weight_CSVHFup","CSVHFDown","","Weight_CSVHFdown"),
             Systematic("CSVHFStats1","CSVHFStats1Up","","Weight_CSVHFStats1up","CSVHFStats1Down","","Weight_CSVHFStats1down"),
             Systematic("CSVLFStats1","CSVLFStats1Up","","Weight_CSVLFStats1up","CSVLFStats1Down","","Weight_CSVLFStats1down"),
             Systematic("CSVHFStats2","CSVHFStats2Up","","Weight_CSVHFStats2up","CSVHFStats2Down","","Weight_CSVHFStats2down"),
             Systematic("CSVLFStats2","CSVLFStats2Up","","Weight_CSVLFStats2up","CSVLFStats2Down","","Weight_CSVLFStats2down"),
             Systematic("CSVCErr1","CSVCErr1Up","","Weight_CSVCErr1up","CSVCErr1Down","","Weight_CSVCErr1down"),
             Systematic("CSVCErr2","CSVCErr2Up","","Weight_CSVCErr2up","CSVCErr2Down","","Weight_CSVCErr2down"),
             #Systematic("Q2Scale_ttbar_bb","Q2Scale_ttbar_bbUp","","Weight_Q2up","Q2Scale_ttbar_bbDown","","Weight_Q2down"),
             #Systematic("Q2Scale_ttbar_b","Q2Scale_ttbar_bUp","","Weight_Q2up","Q2Scale_ttbar_bDown","","Weight_Q2down"),
             #Systematic("Q2Scale_ttbar_cc","Q2Scale_ttbar_ccUp","","Weight_Q2up","Q2Scale_ttbar_ccDown","","Weight_Q2down"),
             #Systematic("Q2Scale_ttbar_0p","Q2Scale_ttbar_0pUp","","Weight_Q2up","Q2Scale_ttbar_0pDown","","Weight_Q2down"),
             #Systematic("Q2Scale_ttbar_1p","Q2Scale_ttbar_1pUp","","Weight_Q2up","Q2Scale_ttbar_1pDown","","Weight_Q2down"),
             #Systematic("Q2Scale_ttbar_2p","Q2Scale_ttbar_2pUp","","Weight_Q2up","Q2Scale_ttbar_2pDown","","Weight_Q2down"),
             #Systematic("Q2Scale_ttbar_less","Q2Scale_ttbar_lessUp","","Weight_Q2up","Q2Scale_ttbar_lessDown","","Weight_Q2down")
             #Systematic("Q2Scale","Q2ScaleUp","","Weight_Q2up","Q2ScaleDown","","Weight_Q2down")
]


                  
weightfileEval=trainerFinal.weightfile
print "Evaluation and Limit Calculation"
evaluaterEval=Evaluater(weightfileEval,variablesFinal,samplesEval,data,systematics)
evaluaterEval.run(category,name)


## plotting deprecated
#call(['root', '-b','-q','PlotLimits.C+'])
#limitname = "output/EvalOutput_"+name+".pdf"
#call(['cp','Limits.pdf',limitname])
#print "plotting BDTEval"
#nBins, minX, maxX = evaluaterEval.GetHistoConfig(category)
#command = "PlotBDTEval.C+(\"" + evaluationPath + "\",\"" + name + "\",\"BDTEval\","+str(nBins)+","+str(minX)+","+str(maxX)+")"
#call(['root', '-b','-q',command])
#plotname = "output/BDTEval_"+name+".pdf"
#rootname = "output/BDTEval_"+name+".root"
#call(['cp', './BDTEval.pdf',plotname])
#call(['cp', './BDTEval.root',rootname])
