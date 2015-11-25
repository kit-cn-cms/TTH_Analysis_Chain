#set up everything here



OutputDirectoryForPreparedTrees="/nfs/dust/cms/user/kelmorab/AnalysisNov10/PreparedTrees/"
#CategoryDefinitionFile="/afs/desy.de/user/k/kelmorab/NewChain/TTH_Analysis_Chain/GreedyDBoostedCategories.txt"
Categories=[
  ["43","(N_LooseLeptons==1 && N_TightLeptons==1 && N_Jets==4 && N_BTagsM==3 && !(BoostedTopHiggs_TopHadCandidate_TopMVAOutput > -0.6850 && BoostedTopHiggs_HiggsCandidate_HiggsTag >= 0.8132))"],
  ["44","(N_LooseLeptons==1 && N_TightLeptons==1 && N_Jets==4 && N_BTagsM==4 && !(BoostedTopHiggs_TopHadCandidate_TopMVAOutput > -0.6850 && BoostedTopHiggs_HiggsCandidate_HiggsTag >= 0.8132))"],
  ["53","(N_LooseLeptons==1 && N_TightLeptons==1 && N_Jets==5 && N_BTagsM==3 && !(BoostedTopHiggs_TopHadCandidate_TopMVAOutput > -0.6850 && BoostedTopHiggs_HiggsCandidate_HiggsTag >= 0.8132))"],
  ["54","(N_LooseLeptons==1 && N_TightLeptons==1 && N_Jets==5 && N_BTagsM>=4 && !(BoostedTopHiggs_TopHadCandidate_TopMVAOutput > -0.6850 && BoostedTopHiggs_HiggsCandidate_HiggsTag >= 0.8132))"],
  ["62","(N_LooseLeptons==1 && N_TightLeptons==1 && N_Jets>=6 && N_BTagsM==2 && !(BoostedTopHiggs_TopHadCandidate_TopMVAOutput > -0.6850 && BoostedTopHiggs_HiggsCandidate_HiggsTag >= 0.8132))"],
  ["63","(N_LooseLeptons==1 && N_TightLeptons==1 && N_Jets>=6 && N_BTagsM==3 && !(BoostedTopHiggs_TopHadCandidate_TopMVAOutput > -0.6850 && BoostedTopHiggs_HiggsCandidate_HiggsTag >= 0.8132))"],
  ["64","(N_LooseLeptons==1 && N_TightLeptons==1 && N_Jets>=6 && N_BTagsM>=4 && !(BoostedTopHiggs_TopHadCandidate_TopMVAOutput > -0.6850 && BoostedTopHiggs_HiggsCandidate_HiggsTag >= 0.8132))"],
  ["DB","(N_LooseLeptons==1 && N_TightLeptons==1 && BoostedTopHiggs_TopHadCandidate_TopMVAOutput > -0.6850 && BoostedTopHiggs_HiggsCandidate_HiggsTag >= 0.8132)"],

]

SystematicTreeNames=["nominal"]


MCinputDirectory="/nfs/dust/cms/user/hmildner/trees1122/"
#List of MCSamples
# ["ProcessName", [List of input folders], SplitMode="None" or "EvenOdd" , BOOL UseFlavorSplitting, RateSystematics=[["lumi",1.025],[], ShapeSystematics=[["lumi",1.025],[]]
MCSamples=[
	["ttH",["ttHbb","ttHnonbb"],"EvenOdd","False",[["lumi",1.025],["pdf",1.03]],[]],
	["ttbar",["ttbar"],"EvenOdd","True",[["lumi",1.025],["pdf",1.03]],[]],
        ]

DATAinputDirectory="/nfs/dust/cms/user/hmildner/trees1122/"
# ["Data", [List of input folders]]
DataSamples=[
	["Data",["mu_reminiaod"]]
	]

     

