import ROOT
from array import array
from subprocess import call
import TableHelper
import CatFormats
import json


class Categorizer:
  def __init__(self, CatDefinition,outPath,debug=False):
    self.categories=[]
    self.categoryPaths=[]
    self.categoryPathsEven=[]
    self.categoryPathsOdd=[]
    self.categoryYields=[]
    self.outPath=outPath
    self.categoryTrees=[]
    self.categoryTreesEven=[]
    self.categoryTreesOdd=[]
    self.debugMaxEntries=20000
    self.debugFlag=debug
    if self.debugFlag:
      print "debugging mode"

    infile=open(CatDefinition,"r")
    inlist=list(infile)
    infile.close()
    line = inlist[0].split(" ")
    for p in line[1:]:
      if "\n" in p:
        p=p.split("\n")[0]
      self.categories.append([p])
    for l in inlist[1:]:
      l=l.split("\n")[0]
      l=l.split(" ")
      for c in self.categories:
        if l[0]==c[0]:
          c.append([l[1],l[2],float(l[3])])
    print "found Categories", self.categories, "\n"
    for cat in self.categories:
     call(["mkdir",outPath+"/Category_"+cat[0]])
     call(["mkdir",outPath+"/Category_"+cat[0]+"/Even"])
     call(["mkdir",outPath+"/Category_"+cat[0]+"/Odd"])
     self.categoryPaths.append([cat[0],outPath+"/Category_"+cat[0]])
     self.categoryPathsEven.append([cat[0],outPath+"/Category_"+cat[0]+"/Even"])
     self.categoryPathsOdd.append([cat[0],outPath+"/Category_"+cat[0]+"/Odd"])
     self.categoryYields.append([cat[0]])
     self.categoryTrees.append([cat[0]])
     self.categoryTreesEven.append([cat[0]])
     self.categoryTreesOdd.append([cat[0]])

    #print self.categoryPaths


  def GetCategory(self,N_Jets, N_BTagsM, BoostedTop_N_BTagsM_Clean_ak5Jets, BoostedHiggs_N_BTagsM_Clean_ak5Jets, Jet_Pt3, BoostedTopHiggs_TopHadCandidate_TopMVAOutput, BoostedTopHiggs_HiggsCandidate_HiggsTag, BoostedHiggs_HiggsCandidate_HiggsTag):
    CatResult=[]
    FinalResult=[]
    # check each category
    for cat in self.categories:
      passed=True
      for cut in cat[1:]:
        if "Greed" in cut[0]:
          continue
        val=cut[2]
        #print cat[0], cut[0], eval(cut[0]), val
        if cut[1]=="==":
          passed = ( eval(cut[0])==val) and passed
        elif cut[1]==">=":
          passed = ( eval(cut[0])>=val) and passed
        elif cut[1]==">":
          passed = ( eval(cut[0])>val) and passed
        elif cut[1]=="<=":
          passed = ( eval(cut[0])<=val) and passed
          #print "<="        
        elif cut[1]=="<":
          passed = ( eval(cut[0])<val) and passed
        else:
          passed == False
        #print passed
      if passed==True:
        CatResult.append(cat[0])
        #print "event passed cuts for category "+str(cat[0])
   # print "Event is in Category ", CatResult
    if len(CatResult)==0:
    #  print "no fitting category found"
      FinalResult.append("NONE")
    if len(CatResult)==1:
      FinalResult.append(CatResult[0])
    if len(CatResult)>1:
     # print "multiple fitting categories, looking at greediness"
      for cat in self.categories:
        if cat[0] in CatResult:
          otherCats=CatResult[:]
          otherCats.remove(cat[0])
      #    print otherCats
          for cut in cat[1:]:
            for oc in otherCats:
              if "Greed" in cut[0] and oc in cut[0]:
                if cut[1]=="==":
                  if cut[2]==1:
                    FinalResult.append(oc)
                  else:
                    FinalResult.append(cat[0])
                else:
                  print "something is wrong"
    if len(FinalResult)!=1:
      print "could not resolve where to put the event"
    else:
      return FinalResult[0]
      
#a=Categorizer("/storage/a/karimel/13TeV/Analysis1/categories.txt","/storage/a/karimel/13TeV/Analysis1","")
#print a.GetCategory(4,2,2,2,40.0,0.0,0.3,0.9)

#method for splitting in Cats
# for testing
#better use SplitInCategoriesEvenOdd() further down
  def SplitInCategories(self,inPath):
    outTrees=[]
    inTreeName=inPath.rsplit("/",1)[1]
    #print samplename
    print "splitting ", inPath
    samplename=inTreeName.rsplit("_",1)[0]
    #print samplename
      
    oldfile = ROOT.TFile( inPath )
    oldtree = oldfile.Get( "MVATree" )
    nentries =oldtree.GetEntries()
      
    for catPath in self.categoryPaths:
      tf=ROOT.TFile(catPath[1]+"/"+inTreeName,"recreate")
      tree=oldtree.CloneTree(0)
      outTrees.append([catPath[0],[tf,tree]])
      for cat in self.categoryTrees:
        if cat[0]==catPath[0]:
          cat.append(catPath[1]+"/"+inTreeName)
    #print outTrees
    #print self.categoryPaths

    njets=array('i',[0])
    nbtagsM=array('i',[0])
    BoostedTopHiggs_TopHadCandidate_TopMVAOutput=array('f',[0])
    BoostedTopHiggs_HiggsCandidate_HiggsTag=array('f',[0])
    BoostedHiggs_HiggsCandidate_HiggsTag=array('f',[0])
    BoostedHiggs_N_BTagsM_Clean_ak5Jets=array('i',[0])
    BoostedTop_N_BTagsM_Clean_ak5Jets=array('i',[0])
    weight=array('f',[0])
    ptjet=array('f',[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    
    oldtree.SetBranchAddress( "N_Jets", njets )
    oldtree.SetBranchAddress( "N_BTagsM", nbtagsM )
    oldtree.SetBranchAddress( "Jet_Pt",ptjet)
    oldtree.SetBranchAddress( "BoostedTopHiggs_TopHadCandidate_TopMVAOutput",BoostedTopHiggs_TopHadCandidate_TopMVAOutput)
    oldtree.SetBranchAddress( "BoostedTopHiggs_HiggsCandidate_HiggsTag",BoostedTopHiggs_HiggsCandidate_HiggsTag)
    oldtree.SetBranchAddress( "BoostedHiggs_HiggsCandidate_HiggsTag",BoostedHiggs_HiggsCandidate_HiggsTag)
    oldtree.SetBranchAddress( "BoostedHiggs_N_BTagsM_Clean_ak5Jets",BoostedHiggs_N_BTagsM_Clean_ak5Jets)
    oldtree.SetBranchAddress( "BoostedTop_N_BTagsM_Clean_ak5Jets",BoostedTop_N_BTagsM_Clean_ak5Jets)
    oldtree.SetBranchAddress( "Weight",weight)
    
    if "JESUP" not in inTreeName and "JESDOWN" not in inTreeName:
      for cat in self.categoryYields:
        cat.append([samplename,0.0])
    #print self.categoryYields
    
    if self.debugFlag==True:
      nentries=self.debugMaxEntries
    for i in range(nentries):
      if i>0 and i%100000==0:
            print "at entry "+str(i)
      oldtree.GetEntry( i )
      resCat=self.GetCategory(njets[0],nbtagsM[0],BoostedTop_N_BTagsM_Clean_ak5Jets[0],BoostedHiggs_N_BTagsM_Clean_ak5Jets[0],ptjet[3],BoostedTopHiggs_TopHadCandidate_TopMVAOutput[0],BoostedTopHiggs_HiggsCandidate_HiggsTag[0],BoostedHiggs_HiggsCandidate_HiggsTag[0])
      
      for cat in outTrees:
        if resCat==cat[0]:
          cat[1][1].Fill()
                
      if "JESUP" not in inTreeName and "JESDOWN" not in inTreeName:
        for cat in self.categoryYields:
          if resCat==cat[0]:
            for s in cat[1:]:
              if samplename==s[0]:
                s[1]+=weight[0]
    
    for cat in outTrees:
      cat[1][1].AutoSave()
      cat[1][0].Close()
    oldfile.Close()
    print "done splitting", inPath
    #print self.categoryYields


#method for splitting in Cats and even/odd event ID
  def SplitInCategoriesEvenOdd(self,inPath):
    outTreesEven=[]
    outTreesOdd=[]
    outNames=[]
    inTreeName=inPath.rsplit("/",1)[1]
    #print samplename
    print "splitting ", inPath
    samplename=inTreeName.rsplit("_",1)[0]
    #print samplename
      
    oldfile = ROOT.TFile( inPath )
    oldtree = oldfile.Get( "MVATree" )
    nentries =oldtree.GetEntries()
      
    for catPath in self.categoryPathsEven:
      outNames.append(catPath[1]+"/"+inTreeName)
      tf=ROOT.TFile(catPath[1]+"/"+inTreeName,"recreate")
      tree=oldtree.CloneTree(0)
      outTreesEven.append([catPath[0],[tf,tree]])
      for cat in self.categoryTreesEven:
        if cat[0]==catPath[0]:
          cat.append(catPath[1]+"/"+inTreeName)
    for catPath in self.categoryPathsOdd:
      tf=ROOT.TFile(catPath[1]+"/"+inTreeName,"recreate")
      tree=oldtree.CloneTree(0)
      outTreesOdd.append([catPath[0],[tf,tree]])
      for cat in self.categoryTreesOdd:
        if cat[0]==catPath[0]:
          cat.append(catPath[1]+"/"+inTreeName)
    #print outTrees
    #print self.categoryPaths

    njets=array('i',[0])
    nbtagsM=array('i',[0])
    BoostedTopHiggs_TopHadCandidate_TopMVAOutput=array('f',[0])
    BoostedTopHiggs_HiggsCandidate_HiggsTag=array('f',[0])
    BoostedHiggs_HiggsCandidate_HiggsTag=array('f',[0])
    BoostedHiggs_N_BTagsM_Clean_ak5Jets=array('i',[0])
    BoostedTop_N_BTagsM_Clean_ak5Jets=array('i',[0])
    weight=array('f',[0])
    ptjet=array('f',[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    eventID=array("i",[0])
    
    oldtree.SetBranchAddress( "N_Jets", njets )
    oldtree.SetBranchAddress( "N_BTagsM", nbtagsM )
    oldtree.SetBranchAddress( "Jet_Pt",ptjet)
    oldtree.SetBranchAddress( "BoostedTopHiggs_TopHadCandidate_TopMVAOutput",BoostedTopHiggs_TopHadCandidate_TopMVAOutput)
    oldtree.SetBranchAddress( "BoostedTopHiggs_HiggsCandidate_HiggsTag",BoostedTopHiggs_HiggsCandidate_HiggsTag)
    oldtree.SetBranchAddress( "BoostedHiggs_HiggsCandidate_HiggsTag",BoostedHiggs_HiggsCandidate_HiggsTag)
    oldtree.SetBranchAddress( "BoostedHiggs_N_BTagsM_Clean_ak5Jets",BoostedHiggs_N_BTagsM_Clean_ak5Jets)
    oldtree.SetBranchAddress( "BoostedTop_N_BTagsM_Clean_ak5Jets",BoostedTop_N_BTagsM_Clean_ak5Jets)
    oldtree.SetBranchAddress( "Weight",weight)
    oldtree.SetBranchAddress("Evt_ID",eventID)
    
    if "JESUP" not in inTreeName and "JESDOWN" not in inTreeName:
      for cat in self.categoryYields:
        cat.append([samplename,0.0])
    #print self.categoryYields
    
    if self.debugFlag==True:
      nentries=self.debugMaxEntries    
    for i in range(nentries):
      if i>0 and i%100000==0:
            print "at entry "+str(i)
      oldtree.GetEntry( i )
      resCat=self.GetCategory(njets[0],nbtagsM[0],BoostedTop_N_BTagsM_Clean_ak5Jets[0],BoostedHiggs_N_BTagsM_Clean_ak5Jets[0],ptjet[3],BoostedTopHiggs_TopHadCandidate_TopMVAOutput[0],BoostedTopHiggs_HiggsCandidate_HiggsTag[0],BoostedHiggs_HiggsCandidate_HiggsTag[0])
      
      #ttW and ttZ dont need to be splitted->Fill em in both 
      if (eventID[0]/100)%2==0 or "ttW" in inTreeName or "ttZ" in inTreeName: # even
        for cat in outTreesEven:
          if resCat==cat[0]:
            cat[1][1].Fill()
      if (eventID[0]/100)%2==1 or "ttW" in inTreeName or "ttZ" in inTreeName: # odd
        for cat in outTreesOdd:
          if resCat==cat[0]:
            cat[1][1].Fill()
                            
      if "JESUP" not in inTreeName and "JESDOWN" not in inTreeName:
        for cat in self.categoryYields:
          if resCat==cat[0]:
            for s in cat[1:]:
              if samplename==s[0]:
                s[1]+=weight[0]
    
    for cat in outTreesEven:
      cat[1][1].AutoSave()
      cat[1][0].Close()
    for cat in outTreesOdd:
      cat[1][1].AutoSave()
      cat[1][0].Close()
    oldfile.Close()
    print "done splitting", inPath
    
    print "hadding the even/odd trees together"
    for name in outNames:
      call(["rm","-f",name.replace("/Even","")])
      call(["hadd",name.replace("/Even",""),name.replace("/Even","/Odd"),name])
    print "hadding done"
      
    #print self.categoryYields



# method to split samples according additional jet flavor
  def SplitTTbarFlavor(self,inPath):
    print "splitting ", inPath, " in different flavors"
    outTrees=[["ttbar_l"],["ttbar_bb"],["ttbar_b"],["ttbar_cc"],["ttbar_2b"]]
    
    oldfile = ROOT.TFile( inPath )
    oldtree = oldfile.Get( "MVATree" )
    nentries =oldtree.GetEntries()
 
    outPaths=[]
    for flavor in outTrees:
      tfname=inPath.replace("ttbar",flavor[0])
      tf=ROOT.TFile(tfname,"recreate")
      tree=oldtree.CloneTree(0)
      flavor.append([tf,tree])
      outPaths.append(tfname)
    #print outTrees
    
    TTPlusCC=array('i',[0])
    TTPlusBB=array('i',[0])

    oldtree.SetBranchAddress( "GenEvt_I_TTPlusCC", TTPlusCC )
    oldtree.SetBranchAddress( "GenEvt_I_TTPlusBB", TTPlusBB )
    
    if self.debugFlag==True:
      nentries=self.debugMaxEntries    
    for i in range(nentries):
      if i>0 and i%100000==0:
        print "at entry "+str(i)
      oldtree.GetEntry( i )
      if TTPlusBB[0]==3:
        outTrees[1][1][1].Fill()
      elif TTPlusBB[0]==1:
        outTrees[2][1][1].Fill()
      elif TTPlusCC[0]==1:
        outTrees[3][1][1].Fill()
      elif TTPlusBB[0]==2:
        outTrees[4][1][1].Fill()
      else:
        outTrees[0][1][1].Fill()
    
    for flavor in outTrees:
      flavor[1][1].AutoSave()
      flavor[1][0].Close()
    oldfile.Close()
    print "done with flavor splitting of ", inPath
    return outPaths

#method opens trees and gets event yields without writing new trees
#use only with unsplit ttbar trees
  def OnlyGetYields(self,inPath):
    inTreeName=inPath.rsplit("/",1)[1]
    #print samplename
    print "counting events in ", inPath
    samplename=inTreeName.rsplit("_",1)[0]
    #print samplename
      
    oldfile = ROOT.TFile( inPath )
    oldtree = oldfile.Get( "MVATree" )
#    oldtree.SetBranchStatus("*",0)
    nentries =oldtree.GetEntries()
      
    njets=array('i',[0])
    nbtagsM=array('i',[0])
    BoostedTopHiggs_TopHadCandidate_TopMVAOutput=array('f',[0])
    BoostedTopHiggs_HiggsCandidate_HiggsTag=array('f',[0])
    BoostedHiggs_HiggsCandidate_HiggsTag=array('f',[0])
    BoostedHiggs_N_BTagsM_Clean_ak5Jets=array('i',[0])
    BoostedTop_N_BTagsM_Clean_ak5Jets=array('i',[0])
    weight=array('f',[0])
    ptjet=array('f',[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    eventID=array("i",[0])
    TTPlusCC=array('i',[0])
    TTPlusBB=array('i',[0])
    
#    oldtree.SetBranchStatus("N_Jets",1)
#    oldtree.SetBranchStatus("N_BTagsM",1)
#    oldtree.SetBranchStatus("Jet_Pt",1)
#    oldtree.SetBranchStatus("BoostedTopHiggs_TopHadCandidate_TopMVAOutput",1)
#    oldtree.SetBranchStatus("BoostedTopHiggs_HiggsCandidate_HiggsTag",1)
#    oldtree.SetBranchStatus("BoostedHiggs_HiggsCandidate_HiggsTag",1)
#    oldtree.SetBranchStatus("BoostedHiggs_N_BTagsM_Clean_ak5Jets",1)
#    oldtree.SetBranchStatus("BoostedTop_N_BTagsM_Clean_ak5Jets",1)
#    oldtree.SetBranchStatus("Weight",1)
#    oldtree.SetBranchStatus("Evt_ID",1)
#    oldtree.SetBranchStatus("GenEvt_I_TTPlusCC",1)
#    oldtree.SetBranchStatus("GenEvt_I_TTPlusBB",1)
    
    oldtree.SetBranchAddress( "N_Jets", njets )
    oldtree.SetBranchAddress( "N_BTagsM", nbtagsM )
    oldtree.SetBranchAddress( "Jet_Pt",ptjet)
    oldtree.SetBranchAddress( "BoostedTopHiggs_TopHadCandidate_TopMVAOutput",BoostedTopHiggs_TopHadCandidate_TopMVAOutput)
    oldtree.SetBranchAddress( "BoostedTopHiggs_HiggsCandidate_HiggsTag",BoostedTopHiggs_HiggsCandidate_HiggsTag)
    oldtree.SetBranchAddress( "BoostedHiggs_HiggsCandidate_HiggsTag",BoostedHiggs_HiggsCandidate_HiggsTag)
    oldtree.SetBranchAddress( "BoostedHiggs_N_BTagsM_Clean_ak5Jets",BoostedHiggs_N_BTagsM_Clean_ak5Jets)
    oldtree.SetBranchAddress( "BoostedTop_N_BTagsM_Clean_ak5Jets",BoostedTop_N_BTagsM_Clean_ak5Jets)
    oldtree.SetBranchAddress( "Weight",weight)
    oldtree.SetBranchAddress("Evt_ID",eventID)
    oldtree.SetBranchAddress( "GenEvt_I_TTPlusCC", TTPlusCC )
    oldtree.SetBranchAddress( "GenEvt_I_TTPlusBB", TTPlusBB )
    
    if "JESUP" not in inTreeName and "JESDOWN" not in inTreeName:
      if "ttbar" in inTreeName or "TTbar" in inTreeName:
        for cat in self.categoryYields:
          cat.append([samplename+"_l",0.0])
          cat.append([samplename+"_bb",0.0])
          cat.append([samplename+"_b",0.0])
          cat.append([samplename+"_cc",0.0])
      else:
        for cat in self.categoryYields:
          cat.append([samplename,0.0])
    print self.categoryYields
    
    if self.debugFlag==True:
      nentries=self.debugMaxEntries    
    for i in range(nentries):
      if i>0 and i%100000==0:
            print "at entry "+str(i)
      oldtree.GetEntry( i )
      resCat=self.GetCategory(njets[0],nbtagsM[0],BoostedTop_N_BTagsM_Clean_ak5Jets[0],BoostedHiggs_N_BTagsM_Clean_ak5Jets[0],ptjet[3],BoostedTopHiggs_TopHadCandidate_TopMVAOutput[0],BoostedTopHiggs_HiggsCandidate_HiggsTag[0],BoostedHiggs_HiggsCandidate_HiggsTag[0])
      
      if "ttbar" in inTreeName or "TTbar" in inTreeName:
        if TTPlusBB[0]==3:
          samplename=samplename+"_bb"
        elif TTPlusBB[0]==1:
          samplename=samplename+"_b"
        elif TTPlusCC[0]==1:
          samplename=samplename+"_cc"
        else:
          samplename=samplename+"_l"
      
      if "JESUP" not in inTreeName and "JESDOWN" not in inTreeName:
        for cat in self.categoryYields:
          if resCat==cat[0]:
            for s in cat[1:]:
              if samplename==s[0]:
                s[1]+=weight[0]
    
    oldfile.Close()
    print "done counting", inPath
    
  def OnlyGetYieldsFast(self,inPath):
    
    inTreeName=inPath.rsplit("/",1)[1]
    if "JESUP" in inTreeName or "JESDOWN" in inTreeName:
      return 0
    #print samplename
    print "counting events in ", inPath
    samplename=inTreeName.rsplit("_",1)[0]
    origname=samplename
    #print samplename
      
    oldfile = ROOT.TFile( inPath )
    oldtree = oldfile.Get( "MVATree" )

#    oldtree.SetBranchStatus("*",0)
    nentries =oldtree.GetEntries()
      
#    oldtree.SetBranchStatus("N_Jets",1)
#    oldtree.SetBranchStatus("N_BTagsM",1)
#    oldtree.SetBranchStatus("Jet_Pt",1)
#    oldtree.SetBranchStatus("BoostedTopHiggs_TopHadCandidate_TopMVAOutput",1)
#    oldtree.SetBranchStatus("BoostedTopHiggs_HiggsCandidate_HiggsTag",1)
#    oldtree.SetBranchStatus("BoostedHiggs_HiggsCandidate_HiggsTag",1)
#    oldtree.SetBranchStatus("BoostedHiggs_N_BTagsM_Clean_ak5Jets",1)
#    oldtree.SetBranchStatus("BoostedTop_N_BTagsM_Clean_ak5Jets",1)
#    oldtree.SetBranchStatus("Weight",1)
#    oldtree.SetBranchStatus("Evt_ID",1)
#    oldtree.SetBranchStatus("GenEvt_I_TTPlusCC",1)
#    oldtree.SetBranchStatus("GenEvt_I_TTPlusBB",1)
#    oldtree.SetBranchStatus("Evt_HT",1)

    if "JESUP" not in inTreeName and "JESDOWN" not in inTreeName:
      if "ttbar" in inTreeName or "TTbar" in inTreeName:
        for cat in self.categoryYields:
          cat.append([samplename+"_l",0.0])
          cat.append([samplename+"_bb",0.0])
          cat.append([samplename+"_b",0.0])
          cat.append([samplename+"_cc",0.0])
          cat.append([samplename+"_2b",0.0])
      else:
        for cat in self.categoryYields:
          cat.append([samplename,0.0])
    #print self.categoryYields
    
    for c in self.categoryYields:
      selection="Weight*("
      for cat in self.categories:
        greedyCats=[]
        if c[0]==cat[0]:
          selection+="("
          for cut in cat[1:]:
            if "Greed" in cut[0]:
              for gc in self.categories:
                if gc[0] in cut[0] and "=="==cut[1] and 1==cut[2]:
                  greedyCats.append(gc[0])
                  #print "Greedy ",gc[0]
              continue
            selection+=str(cut[0])+str(cut[1])+str(cut[2])
            selection+=" && "
          selection=selection.rsplit("&&",1)[0]
          #print selection
          selection+=") && "
          #print selection
          for gc in self.categories:
            if gc[0] in greedyCats:
              selection+="!("
              for cut in gc[1:]:
                #print cut
                if "Greed" in cut[0]:
                  continue
                selection+=str(cut[0])+str(cut[1])+str(cut[2])
                selection+=" && "
                #print selection
              selection=selection.rsplit("&&",1)[0]
              #print selection
              selection+=") && "
      selection=selection.rsplit("&&",1)[0]
      selection+=")"
      #print " "
      #print selection
      #print ""
      if "ttbar" in inTreeName or "TTbar" in inTreeName:
        samplename=origname+"_bb"
        selection=selection.rsplit(")",1)[0]
        selection+=" && GenEvt_I_TTPlusBB==3)"
        bufferHisto=ROOT.TH1D("bufferHisto","bufferHisto",1000,oldtree.GetMinimum("Evt_HT")-1.0,oldtree.GetMaximum("Evt_HT")+1.0)
        oldtree.Draw("Evt_HT>>bufferHisto",selection)
        integral=bufferHisto.Integral()
        for s in c[1:]:
          if samplename==s[0]:
            s[1]=integral
            #print samplename, integral
        
        samplename=origname+"_b"
        selection=selection.replace("GenEvt_I_TTPlusBB==3","GenEvt_I_TTPlusBB==1")
        bufferHisto=ROOT.TH1D("bufferHisto","bufferHisto",1000,oldtree.GetMinimum("Evt_HT")-1.0,oldtree.GetMaximum("Evt_HT")+1.0)
        oldtree.Draw("Evt_HT>>bufferHisto",selection)
        integral=bufferHisto.Integral()
        for s in c[1:]:
          if samplename==s[0]:
            s[1]=integral
            #print samplename, integral
        
        samplename=origname+"_cc"
        selection=selection.replace("GenEvt_I_TTPlusBB==1","GenEvt_I_TTPlusCC==1")
        bufferHisto=ROOT.TH1D("bufferHisto","bufferHisto",1000,oldtree.GetMinimum("Evt_HT")-1.0,oldtree.GetMaximum("Evt_HT")+1.0)
        oldtree.Draw("Evt_HT>>bufferHisto",selection)
        integral=bufferHisto.Integral()
        for s in c[1:]:
          if samplename==s[0]:
            s[1]=integral
            #print samplename, integral
            
        samplename=origname+"_l"
        selection=selection.replace("GenEvt_I_TTPlusCC==1","GenEvt_I_TTPlusBB==0 && GenEvt_I_TTPlusCC==0")
        bufferHisto=ROOT.TH1D("bufferHisto","bufferHisto",1000,oldtree.GetMinimum("Evt_HT")-1.0,oldtree.GetMaximum("Evt_HT")+1.0)
        oldtree.Draw("Evt_HT>>bufferHisto",selection)
        integral=bufferHisto.Integral()
        for s in c[1:]:
          if samplename==s[0]:
            s[1]=integral
            #print samplename, integral
        
        samplename=origname+"_2b"
        selection=selection.replace("GenEvt_I_TTPlusBB==0 && GenEvt_I_TTPlusCC==0","GenEvt_I_TTPlusBB==2")
        bufferHisto=ROOT.TH1D("bufferHisto","bufferHisto",1000,oldtree.GetMinimum("Evt_HT")-1.0,oldtree.GetMaximum("Evt_HT")+1.0)
        oldtree.Draw("Evt_HT>>bufferHisto",selection)
        integral=bufferHisto.Integral()
        for s in c[1:]:
          if samplename==s[0]:
            s[1]=integral
            #print samplename, integral
        
      else:
        bufferHisto=ROOT.TH1D("bufferHisto","bufferHisto",1000,oldtree.GetMinimum("Evt_HT")-1.0,oldtree.GetMaximum("Evt_HT")+1.0)
        oldtree.Draw("Evt_HT>>bufferHisto",selection)
        integral=bufferHisto.Integral()
        for s in c[1:]:
          if samplename==s[0]:
            s[1]=integral
            #print "integral ",integral
            
    oldfile.Close()
    print self.categoryYields
    print "done counting\n", inPath
    
#method to add each tree in a category to create MCData.root
  def CreateMCData(self):
    print self.categoryTrees
    print self.categoryTreesEven
    print self.categoryTreesOdd
    if len(self.categoryTrees[0])>1:
      for cat in self.categoryTrees:
        names=[]
        for tree in cat[1:]:
          if "JESUP" not in tree and "JESDOWN" not in tree:
            names.append(tree)
        outname=names[0].rsplit("/",1)[0]+"/MCData.root"
        call(["rm","-f",outname])
        call(["hadd",outname]+names)
    if len(self.categoryTreesEven[0])>1:
      for cat in self.categoryTreesEven:
        names=[]
        for tree in cat[1:]:
          if "JESUP" not in tree and "JESDOWN" not in tree:
            names.append(tree)
        outname=names[0].rsplit("/",1)[0]+"/MCData.root"
        call(["rm","-f",outname])
        call(["hadd",outname]+names)
    if len(self.categoryTreesOdd[0])>1:
      for cat in self.categoryTreesOdd:
        names=[]
        for tree in cat[1:]:
          if "JESUP" not in tree and "JESDOWN" not in tree:
            names.append(tree)
        outname=names[0].rsplit("/",1)[0]+"/MCData.root"
        call(["rm","-f",outname])
        call(["hadd",outname]+names)
    print "\n hadded Trees for MCData files\n"
     
#method to make yield tables for the categories
  def MakeYieldTables(self):
    call(["mkdir",self.outPath+"/Yields"])
    out=open(self.outPath+"/Yields/CategoryYields.tex","w")
    out.write( '\\documentclass{article}\n')
    out.write( '\\begin{document}\n')
    #print self.categoryYields
    
    bkgSums=["Total bkg"]
    data=["Data"]
    #sort the yields in the right sample and category order
    #print CatFormats.sampleOrder
    orderedYields=[]
    orderedYields=sorted(self.categoryYields,key=lambda x: CatFormats.catOrder.index(x[0]))
    self.categoryYields=orderedYields
    orderedYields=[]
    for cat in self.categoryYields:
      cat=cat[:1]+sorted(cat[1:],key=lambda x: CatFormats.sampleOrder.index(x[0]))
      orderedYields.append(cat)
    self.categoryYields=orderedYields
    print self.categoryYields
    #make the table
    headline=[" "]
    for cat in self.categoryYields:
      if len(cat)!=len(self.categoryYields[0]):
        print "SOMETHING Wrong with the categories"
        exit(1)
      foundName=False
      for name in CatFormats.catnames:
        if cat[0]==name[0]:
          foundName=True
          headline.append(name[1])
      if foundName==False:
        headline.append(cat[0])
    TableHelper.write_head(out,headline)
    for i, sample in enumerate(self.categoryYields[0][1:]):
      if sample[0]=="data" or sample[0]=="Data":
        continue
      line=[]
      sampleName=sample[0]
      for sn in CatFormats.sampleNames:
        if sample[0] == sn[0]:
          sampleName=sn[1]
          break
        
      line.append(sampleName)
      #print type(sample[1]), sample[1]
      yld="%0.1f" % sample[1]
      line.append(yld)
      #print self.categoryYields[1:]
      for cat in self.categoryYields[1:]:
        #print type(cat[i+1][1]),cat[i+1]
        yld="%0.1f" % cat[i+1][1]
        line.append(yld)
      TableHelper.write_syst(out,line)
    
    #get bkgSums
    for cat in self.categoryYields:
      bkg=0.0
      for sample in cat[1:]:
        if sample[0]=="data" or sample[0]=="Data" or sample[0]=="tth" or sample[0]=="ttH" or sample[0]=="ttHbb" or sample[0]=="tthbb" :
          continue
        bkg+=sample[1]
      byld="%0.1f" % bkg
      bkgSums.append(byld)
    out.write("\\hline\n")
    TableHelper.write_syst(out,bkgSums)
    out.write("\\hline\n")
    #get Data
    for cat in self.categoryYields:
      dtyld="0"
      for sample in cat[1:]:
        if sample[0]=="data" or sample[0]=="Data":
          dtyld="%0.1f" % sample[1]
      data.append(dtyld)
    TableHelper.write_syst(out,data)
    TableHelper.write_foot(out)
    out.write("\\end{document}\n")
    out.close()
    print "creating table.pdf"
    call(["pdflatex","-interaction","batchmode","-output-directory",self.outPath+"/Yields/",self.outPath+"/Yields/CategoryYields.tex"])
    print "creating table.eps"
    call(["pdftops","-eps",self.outPath+"/Yields/CategoryYields.pdf",self.outPath+"/Yields/CategoryYields.eps"])


# method to create category yield plots
  def MakeYieldPlots(self):
    call(["mkdir",self.outPath+"/Yields"])
    ttHScale=30.0
    #print self.categoryYields
    nCats=len(self.categoryYields)
    hstack=ROOT.THStack("hstack","Yields")
    histos=[]
    canvas=ROOT.TCanvas("canvas","Yields",800,600)
    legend=ROOT.TLegend(0.3,0.78,0.94,0.89)
    legend.SetFillColor(0)
    legend.SetBorderSize(0)
    legend.SetNColumns(3);
    #sort the yields in the right sample and category order
    #print CatFormats.sampleOrder
    orderedYields=[]
    orderedYields=sorted(self.categoryYields,key=lambda x: CatFormats.catOrder.index(x[0]))
    self.categoryYields=orderedYields
    orderedYields=[]
    for cat in self.categoryYields:
      cat=cat[:1]+sorted(cat[1:],key=lambda x: CatFormats.sampleOrder.index(x[0]))
      orderedYields.append(cat)
    self.categoryYields=orderedYields
    print self.categoryYields
    
    for sample in self.categoryYields[0][1:]:
      print sample
      thisHisto=ROOT.TH1F("h"+sample[0],sample[0],nCats,0,nCats)
      for i,cat in enumerate(self.categoryYields):
        print "doing ",cat
        for s in cat[1:]:
          if s[0] == sample[0]:
            print i, s[0]
            thisHisto.SetBinContent(i+1,s[1])
            catName=cat[0]
            for cn in CatFormats.catnames:
              if cat[0] == cn[0]:
                catName=cn[1].replace("\\rm ","").replace("$","").replace("\\","#")
                break
            break
        thisHisto.GetXaxis().SetBinLabel(i+1,catName)
      color=ROOT.kYellow
      for sc in CatFormats.sampleColors:
        if sample[0] == sc[0]:
          color=sc[1]
          #print "this histo has color ",color
          break
      thisHisto.SetLineColor(color)
      thisHisto.SetFillColor(color)
      histos.append([sample[0],thisHisto,"stack"])
    #print "created histos"
    #print histos
    datahisto=""
    tthhisto=""
    for thisHisto in reversed(histos):
      name=thisHisto[0]
      for sn in CatFormats.sampleNames:
        if name==sn[0]:
          name=sn[1].replace("\\rm ","").replace("$","").replace("\\","#")
          break
      integral=thisHisto[1].Integral()
      #print thisHisto[0],integral
      legstring=name+" (%0.1f)" %integral
      if thisHisto[0]=="tth" or thisHisto[0]=="ttH" or thisHisto[0]=="tthbb" or thisHisto[0]=="ttHbb":
        thisHisto[1].Scale(ttHScale)
        print thisHisto[1].GetLineWidth
        thisHisto[1].SetLineWidth(2)
        thisHisto[1].SetFillColor(0)
        tthhisto=thisHisto
        legend.AddEntry(tthhisto[1],legstring+"x30","l")
      elif thisHisto[0]=="data" or thisHisto[0]=="Data":
        thisHisto[1].SetMarkerStyle(2)
        datahisto=thisHisto
        legend.AddEntry(datahisto[1],legstring,"p")
      else:
        thisHisto[1].SetLineColor(ROOT.kBlack)
        hstack.Add(thisHisto[1])
        legend.AddEntry(thisHisto[1],legstring,"f")
      print "done with ", name
    canvas.cd()
    maxVal=hstack.GetMaximum()
    print maxVal
    hstack.SetMaximum(maxVal*3.0)
    canvas.SetLogy(1)
    hstack.Draw()
    tthhisto[1].Draw("SAME")
    if datahisto!="":
      datahisto[1].Draw("SAME")
    legend.Draw()
    canvas.SaveAs(self.outPath+"/Yields/YieldPlot.eps")
    canvas.SaveAs(self.outPath+"/Yields/YieldPlot.root")

  def AppendStuffToLogLines(self,loglines):
    loglines.append("\n")
    loglines.append("Category Trees\n")
    for cat in self.categoryTrees:
      for tree in cat[1:]:
        loglines.append(cat[0]+" "+tree+"\n")
    loglines.append("\n")
    loglines.append("Category Trees Even\n")
    for cat in self.categoryTreesEven:
      for tree in cat[1:]:
        loglines.append(cat[0]+" "+tree+"\n")
    loglines.append("\n")
    loglines.append("Category Trees Odd\n")
    for cat in self.categoryTreesOdd:
      for tree in cat[1:]:
        loglines.append(cat[0]+" "+tree+"\n")
    loglines.append("\n")
    yline=json.dumps(self.categoryYields)
    loglines.append("Yields\n")
    loglines.append("JSONYields "+yline+"\n")
    loglines.append("\n")
    
  def ReadCategoryYieldsFromLogLines(self,loglines):
    yieldline=""
    for line in loglines:
      if "JSONYields" in line:
        yieldline=line.split(" ",1)[1]
        yieldline=yieldline.strip()
        self.categoryYields=json.loads(yieldline)
    print "loaded Yields from AnalysisLog"
    #print type(self.categoryYields)
    #print type(self.categoryYields[0][1][1])
    #print self.categoryYields
      
    
    
