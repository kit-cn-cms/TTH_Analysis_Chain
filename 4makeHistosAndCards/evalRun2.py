from evaluaterRun2 import LJWriter
from evaluaterRun2 import Systematic
from evaluaterRun2 import Sample
from subprocess import call
from SampleScaleGetter import *
import sys

cat=sys.argv[1]
nameAna=sys.argv[2]
AnaPath=sys.argv[3]


evaluationPath=AnaPath+"/Category_"+category+"/Even/"
trainPath=AnaPath+"/Category_"+category+"/Odd/"

samplesTrain=[Sample("tthbb",trainPath+"tthbb_nominal.root",0.125,1.),Sample("ttbar_light",trainPath+"ttbar_l_nominal.root",-1,1.),Sample("ttbar_b",trainPath+"ttbar_b_nominal.root",0.5,1.),Sample("ttbar_bb",trainPath+"ttbar_bb_nominal.root",0.5,1.),Sample("ttbar_2b",trainPath+"ttbar_2b_nominal.root",0.5,1.),Sample("ttbar_cc",trainPath+"ttbar_cc_nominal.root",0.5,1.)]
dataTrain=Sample("data",trainPath+"MCData.root",-1,1.)

samplesTest=[Sample("tthbb",evaluationPath+"tthbb_nominal.root",0.133,1.),Sample("ttbar_light",evaluationPath+"ttbar_l_nominal.root",-1,1.),Sample("ttbar_b",evaluationPath+"ttbar_b_nominal.root",0.618,1.),Sample("ttbar_bb",evaluationPath+"ttbar_bb_nominal.root",0.618,1.),Sample("ttbar_2b",evaluationPath+"ttbar_2b_nominal.root",0.618,1.),Sample("ttbar_cc",evaluationPath+"ttbar_cc_nominal.root",0.618,1.)]
dataTest=Sample("data",evaluationPath+"MCData.root",-1,1.)
#data=Sample("data",evaluationPath+"tthbb_lj_"+name+"_nominal.root",-1,1.)

#print samplesTest
samplesEval=GetSampleScales(samplesTrain,samplesTest)
#print samplesEval
data=GetSampleScales([dataTrain],[dataTest])
data=data[0]
#print data
#exit(0)

systematics=[
             Systematic("CMS_scale_j","CMS_scale_jUp","_JESUP","","CMS_scale_jDown","_JESDOWN",""),
             Systematic("CSVLF","CSVLFUp","","Weight_CSVLFup","CSVLFDown","","Weight_CSVLFdown"),
             #Systematic("CSVHF","CSVHFUp","","Weight_CSVHFup","CSVHFDown","","Weight_CSVHFdown"),
             Systematic("CSVHFStats1","CSVHFStats1Up","","Weight_CSVHFStats1up","CSVHFStats1Down","","Weight_CSVHFStats1down"),
             #Systematic("CSVLFStats1","CSVLFStats1Up","","Weight_CSVLFStats1up","CSVLFStats1Down","","Weight_CSVLFStats1down"),
             Systematic("CSVHFStats2","CSVHFStats2Up","","Weight_CSVHFStats2up","CSVHFStats2Down","","Weight_CSVHFStats2down"),
             Systematic("CSVLFStats2","CSVLFStats2Up","","Weight_CSVLFStats2up","CSVLFStats2Down","","Weight_CSVLFStats2down"),
             #Systematic("CSVCErr1","CSVCErr1Up","","Weight_CSVCErr1up","CSVCErr1Down","","Weight_CSVCErr1down"),
             #Systematic("CSVCErr2","CSVCErr2Up","","Weight_CSVCErr2up","CSVCErr2Down","","Weight_CSVCErr2down"),
             
             #Systematic("Q2Scale_ttbar_bb","Q2Scale_ttbar_bbUp","","Weight_Q2up","Q2Scale_ttbar_bbDown","","Weight_Q2down"),
             #Systematic("Q2Scale_ttbar_b","Q2Scale_ttbar_bUp","","Weight_Q2up","Q2Scale_ttbar_bDown","","Weight_Q2down"),
             #Systematic("Q2Scale_ttbar_cc","Q2Scale_ttbar_ccUp","","Weight_Q2up","Q2Scale_ttbar_ccDown","","Weight_Q2down"),
             #Systematic("Q2Scale_ttbar_0p","Q2Scale_ttbar_0pUp","","Weight_Q2up","Q2Scale_ttbar_0pDown","","Weight_Q2down"),
             #Systematic("Q2Scale_ttbar_1p","Q2Scale_ttbar_1pUp","","Weight_Q2up","Q2Scale_ttbar_1pDown","","Weight_Q2down"),
             #Systematic("Q2Scale_ttbar_2p","Q2Scale_ttbar_2pUp","","Weight_Q2up","Q2Scale_ttbar_2pDown","","Weight_Q2down"),
             #Systematic("Q2Scale_ttbar_less","Q2Scale_ttbar_lessUp","","Weight_Q2up","Q2Scale_ttbar_lessDown","","Weight_Q2down")
             #Systematic("Q2Scale","Q2ScaleUp","","Weight_Q2up","Q2ScaleDown","","Weight_Q2down")
]

LJWriter=LJWriter(samplesEval,data,systematics)
LJWriter.runLJ(cat,nameAna)

#call(['root', '-b','-q','PlotLimits.C+'])
#limitname = "output/EvalOutput_"+name+".pdf"
#call(['cp','Limits.pdf',limitname])

