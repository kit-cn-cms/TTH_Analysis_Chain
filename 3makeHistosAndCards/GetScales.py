from trainer import Trainer
from evaluaterRun2 import Evaluater
from evaluaterRun2 import Systematic
from evaluaterRun2 import Sample
from subprocess import call
from SampleScaleGetter import *

import sys
import json

category=sys.argv[1]
AnaPath=sys.argv[2]

evaluationPath=AnaPath+"/Category_"+category+"/Even/"
trainingPath=AnaPath+"/Category_"+category+"/Odd/"

samplesTrainingForScales=[Sample("tth",trainingPath+"tth_nominal.root",-1,1.),Sample("ttbar_light",trainingPath+"ttbar_l_nominal.root",.1,1.),Sample("ttbar_b",trainingPath+"ttbar_b_nominal.root",.618,1.),Sample("ttbar_bb",trainingPath+"ttbar_bb_nominal.root",.618,1.),Sample("ttbar_2b",trainingPath+"ttbar_2b_nominal.root",.618,1.),Sample("ttbar_cc",trainingPath+"ttbar_cc_nominal.root",.618,1.),Sample("SingleT",trainingPath+"SingleT_nominal.root",0.031,1.),Sample("DiBoson",trainingPath+"DiBoson_nominal.root",0.07,1.),Sample("ttW",trainingPath+"ttW_nominal.root",0.139,1.),Sample("ttZ",trainingPath+"ttZ_nominal.root",0.124,1.),Sample("ZJets",trainingPath+"ZJets_nominal.root",0.1,1.)]
dataTrainForScales=Sample("data",trainingPath+"MCData.root",-1,1.)

samplesTest=[Sample("tth",evaluationPath+"tth_nominal.root",0.097,1.),Sample("ttbar_light",evaluationPath+"ttbar_l_nominal.root",-1,1.),Sample("ttbar_b",evaluationPath+"ttbar_b_nominal.root",0.618,1.),Sample("ttbar_bb",evaluationPath+"ttbar_bb_nominal.root",0.618,1.),Sample("ttbar_2b",evaluationPath+"ttbar_2b_nominal.root",0.618,1.),Sample("ttbar_cc",evaluationPath+"ttbar_cc_nominal.root",0.618,1.),Sample("SingleT",evaluationPath+"SingleT_nominal.root",0.031,1.),Sample("DiBoson",evaluationPath+"DiBoson_nominal.root",0.07,1.),Sample("ttW",evaluationPath+"ttW_nominal.root",0.139,1.),Sample("ttZ",evaluationPath+"ttZ_nominal.root",0.124,1.),Sample("ZJets",evaluationPath+"ZJets_nominal.root",0.1,1.)]
dataTest=Sample("data",evaluationPath+"MCData.root",-1,1.)


samplesEval=GetSampleScales(samplesTrainingForScales,samplesTest)
#data=GetSampleScales([dataTrainForScales],[dataTest])
#data=data[0]
