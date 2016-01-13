#set up everything here



OutputDirectoryForPreparedTrees="/nfs/dust/cms/user/kelmorab/MEMstudies/PreparedTrees/"
#CategoryDefinitionFile="/afs/desy.de/user/k/kelmorab/NewChain/TTH_Analysis_Chain/GreedyDBoostedCategories.txt"
#Categories=[
  #["43","(N_LooseLeptons==1 && N_TightLeptons==1 && N_Jets==4 && N_BTagsM==3 && !(BoostedTopHiggs_TopHadCandidate_TopMVAOutput > -0.1650 && BoostedTopHiggs_HiggsCandidate_HiggsTag >= 0.9425))"],
  #["44","(N_LooseLeptons==1 && N_TightLeptons==1 && N_Jets==4 && N_BTagsM==4 && !(BoostedTopHiggs_TopHadCandidate_TopMVAOutput > -0.1650 && BoostedTopHiggs_HiggsCandidate_HiggsTag >= 0.9425))"],
  #["53","(N_LooseLeptons==1 && N_TightLeptons==1 && N_Jets==5 && N_BTagsM==3 && !(BoostedTopHiggs_TopHadCandidate_TopMVAOutput > -0.1650 && BoostedTopHiggs_HiggsCandidate_HiggsTag >= 0.9425))"],
  #["54","(N_LooseLeptons==1 && N_TightLeptons==1 && N_Jets==5 && N_BTagsM>=4 && !(BoostedTopHiggs_TopHadCandidate_TopMVAOutput > -0.1650 && BoostedTopHiggs_HiggsCandidate_HiggsTag >= 0.9425))"],
  #["62","(N_LooseLeptons==1 && N_TightLeptons==1 && N_Jets>=6 && N_BTagsM==2 && !(BoostedTopHiggs_TopHadCandidate_TopMVAOutput > -0.1650 && BoostedTopHiggs_HiggsCandidate_HiggsTag >= 0.9425))"],
  #["63","(N_LooseLeptons==1 && N_TightLeptons==1 && N_Jets>=6 && N_BTagsM==3 && !(BoostedTopHiggs_TopHadCandidate_TopMVAOutput > -0.1650 && BoostedTopHiggs_HiggsCandidate_HiggsTag >= 0.9425))"],
  #["64","(N_LooseLeptons==1 && N_TightLeptons==1 && N_Jets>=6 && N_BTagsM>=4 && !(BoostedTopHiggs_TopHadCandidate_TopMVAOutput > -0.1650 && BoostedTopHiggs_HiggsCandidate_HiggsTag >= 0.9425))"],
  #["DB","(N_LooseLeptons==1 && N_TightLeptons==1 && BoostedTopHiggs_TopHadCandidate_TopMVAOutput > -0.1650 && BoostedTopHiggs_HiggsCandidate_HiggsTag >= 0.9425)"],

#]

Categories=[
  #["43","(N_LooseLeptons==1 && N_TightLeptons==1 && N_Jets==4 && N_BTagsM==3)"],
  #["44","(N_LooseLeptons==1 && N_TightLeptons==1 && N_Jets==4 && N_BTagsM==4)"],
  #["53","(N_LooseLeptons==1 && N_TightLeptons==1 && N_Jets==5 && N_BTagsM==3)"],
  #["54","(N_LooseLeptons==1 && N_TightLeptons==1 && N_Jets==5 && N_BTagsM>=4)"],
  #["62","(N_LooseLeptons==1 && N_TightLeptons==1 && N_Jets>=6 && N_BTagsM==2)"],
  #["63","(N_LooseLeptons==1 && N_TightLeptons==1 && N_Jets>=6 && N_BTagsM==3)"],
  ["64","(N_LooseLeptons==1 && N_TightLeptons==1 && N_Jets>=6 && N_BTagsM>=4)"],
]

SystematicTreeNames=["nominal"]


MCinputDirectory="/nfs/dust/cms/user/kelmorab/MEMstudies/newTrees/"
#List of MCSamples
# ["ProcessName", [List of input folders], SplitMode="None" or "EvenOdd" , BOOL UseFlavorSplitting, RateSystematics=[["lumi",1.025],[], ShapeSystematics=[["lumi",1.025],[]]
MCSamples=[
	["ttH",["ttHbb"],"EvenOdd","False",[["lumi",1.025],["pdf",1.03]],[]],
	["ttbar",["ttbar"],"EvenOdd","True",[["lumi",1.025],["pdf",1.03]],[]],
	#["SingleT",["st_tchan","stbar_tchan","st_schan","stbar_tWchan","st_tWchan"],"EvenOdd","False",[["lumi",1.025],["pdf",1.03]],[]],
	#["WJets",["Wjets"],"EvenOdd","False",[["lumi",1.025],["pdf",1.03]],[]],
	#["ZJets",["Zjets_m10to50","Zjets_m50toInf"],"EvenOdd","False",[["lumi",1.025],["pdf",1.03]],[]],
	#["QCD",["QCD-HT-700-1000","QCD-HT-500-700","QCD-HT-300-500","QCD-HT-2000-inf","QCD-HT-200-300","QCD-HT-1500-2000","QCD-HT-1000-1500","QCD-HT-100-200"],"EvenOdd","False",[["lumi",1.025],["pdf",1.03]],[]],
	#["DiBoson",["WW","ZZ","WZ"],"EvenOdd","False",[["lumi",1.025],["pdf",1.03]],[]],
	#["ttZ",["ttZ_hadr"],"EvenOdd","False",[["lumi",1.025],["pdf",1.03]],[]],
	#["ttW",["ttW_lept","ttW_hadr"],"EvenOdd","False",[["lumi",1.025],["pdf",1.03]],[]],

]

DATAinputDirectory="/nfs/dust/cms/user/hmildner/trees1122/"
# ["Data", [List of input folders]]
DataSamples=[
	["Data",["mu_reminiaod"]]
	]

     

