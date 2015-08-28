# TTH_Analysis_Chain
This is the long analysis chain created for developement and is very WIP
It goes from n-tuple Trees -> BDT optimization -> BDT Training -> Limits

If your trees already contain the BDT output you can follow the Ohio way here: https://twiki.cern.ch/twiki/bin/viewauth/CMS/BoostedAnalyzer#Calculate_limits_for_baseline_an

Instructions:

#### -1)
To begin with you need some trees.  
You can use https://github.com/cms-ttH/BoostedTTH to produce these.  
Hadd the output trees accroding to their sample.   
They should follow some some naming conventions like tth_nominal.root or ttbar_JESUP.root or so.  
Put them all into one directory.  

To get the limits you can do the following steps  

#### 0) 
You can use 0MakeSlimTrees to slim the trees down, allowing for a speed increase in the following steps.   

#### 1)
Use 1PrepareSamples to split the trees into categories and ttbar trees into flavor specific sub trees.  
This sets up the structure needed in the Training and Limit steps.  

Run  
"python -b PrepareSamples.py DIRECTORY_WITH_SLIM_TREES DIRECTORY_FOR_PREPARED_TREES CATEGORY_DEFINITION"  
DIRECTORY_WITH_SLIM_TREES = directory containing the input trees. You should follow the above mentioned naming   convention, see e.g. /1PrepareSamples/CatFormats.py  
DIRECTORY_FOR_PREPARED_TREES = empty directory for output  
CATEGORY_DEFINITION = a file defining the categories.   
  
I already prepared 3 categorizations:  
"LJcategories.txt" = usual L+J categories  
"GreedyDBoostedCategories.txt" = puts overlapping events in the double boosted category  
"GenerousDBoostedCategories.txt" = puts overlapping events in the L+J categories  

#### 2) 
At this point you can find a BDT configuration  
- Play around with TMVA  
- or use https://github.com/kit-cn-cms/mva-training  
- or https://github.com/kit-cn-cms/ParticleSwarmOptimization  

#### 3)  
Here you train the BDTs, create output histograms, create datacards and calculate the limits.  
This is all done with either:  
/4makeHistosAndCards/evalRun2.py if the trees already contain the BDT output (or use https://twiki.cern.ch/twiki/bin/viewauth/CMS/BoostedAnalyzer#Calculate_limits_for_baseline_an)  
  
but usually thats not the case and then you do     
"cd /4makeHistosAndCards/"  
"python -b TrainAndEval.py CATEGORY NAME FINALBDTCONFIG_FILE INPUTPATH [test | train]"  
  
where   
CATEGORY = for example 43 or 62 or DB or so  
NAME = name of outputfiles  
FINALBDTCONFIG_FILE = a file containing the BDT config e.g. see example files  
INPUTPATH = path to input trees prepared in ../1PrepareSamples.  
[test | train] = do limit on test or trainings samples , default is testing sample  

this will give you a datacard, histograms and a Limit result file in the /4makeHistosAndCards/output directory  
You can recalculate the limit with  
"combine -M Asymptotic --minosAlgo stepping datacard.txt --run="blind" "  
or any other combine option  

Different categories can be combined with   
"dcCombiner.py"  
But the script is not very clever and you have to specify the number of samples and systematics in the script  

You can also convert the created histograms to be compatible with the Ohio way (see above) via "ConvertHistosToNova.py"  

#### 4)
Here a tool to calculate a ProfileLikelihood Limit with lots of toys will be provided.  
It can parallelize toy creation on the batch system.  
It already exists and will be updated soon(TM).  


