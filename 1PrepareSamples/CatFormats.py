#for formatting the output plots and tables    
import ROOT

#doesnt fit in table 
##catnames=[["43","4 jets + 3 b-tags"],["44","4 jets +4 b-tags"],["53","5 jets + 3 b-tags"],["54","5 jets + $\\geq$ 4 b-tags"],["62","$\\geq$ 6 jets + 2 b-tags"],["63","$\\geq$ 6 jets + 3 b-tags"],["64","$\\geq$ 6 jets + $\\geq$ 4 b-tags"],["DB","boosted Higgs + boosted Top"],["SBT","boosted Top + $\\geq$ 3 b-tags"],["SBH","boosted Higgs + $\\geq$ 3 b-tags"]]


catnames=[["42","4j2t"],["43","4j3t"],["44","4j4t"],["52","5j2t"],["53","5j3t"],["54","5j$\\geq$4t"],["62","$\\geq$6j2t"],["63","$\\geq$6j3t"],["64","$\\geq$6j$\\geq$4t"],["DB","boosted"],["SBT","boostedTop+$\\geq$3t"],["SBH","boostedHiggs+$\\geq$2t"]]

sampleNames=[ ["tth","$\\rm t\\bar{t}H$"],["ttH","$\\rm t\\bar{t}H$"],["TTH","$\\rm t\\bar{t}H$"],["tthbb","$\\rm t\\bar{t}H b\\bar{b}$"],["ttHbb","$\\rm t\\bar{t}H b\\bar{b}$"], ["tthnonbb","$\\rm t\\bar{t}H non b\\bar{b}$"],["ttHnonbb","$\\rm t\\bar{t}H non b\\bar{b}$"], ["ttbar","t\\bar{t}"], ["ttbar_l","$\\rm t\\bar{t}+lf$"] , ["ttbar_bb","$\\rm t\\bar{t}+b\\bar{b}$"], ["ttbar_b","$\\rm t\\bar{t}+b$"], ["ttbar_2b","$\\rm t\\bar{t}+2b$"],["ttbar_cc","$\\rm t\\bar{t}+c\\bar{c}$"], ["ttW","$\\rm t\\bar{t}+W$"], ["ttZ","$\\rm t\\bar{t}+Z$"], ["SingleT","single t"], ["WJets","W+jets"], ["ZJets","Z+jets"], ["DiBoson","diboson"],["data","Data"]]

#sampleOrder=["tth","ttH","TTH","ttHbb","tthbb","ttHnonbb","tthnonbb","ttbar","ttbar_l","ttbar_b","ttbar_bb","ttbar_2b","ttbar_cc","ttW","ttZ","SingleT","singlet","WJets","ZJets","Wjets","Zjets","DiBoson","Diboson","diboson","data","DATA","Data"]

sampleOrder=["tth","ttH","TTH","ttHbb","tthbb","ttHnonbb","tthnonbb","ttbar","ttbar_l","ttbar_cc","SingleT","singlet","WJets","ZJets","Wjets","Zjets","ttW","ttZ","DiBoson","Diboson","diboson","ttbar_b","ttbar_2b","ttbar_bb","data","DATA","Data"]


#catOrder=["42","43","44","52","53","54","62","63","64","DB"]
catOrder=["42","52","62","43","53","63","44","54","64","DB"]

sampleColors=[ ["ttH",ROOT.kBlue], ["ttHbb",ROOT.kBlue], ["ttHnonbb",ROOT.kYellow], ["ttbar",ROOT.kRed], ["ttbar_l",ROOT.kRed-7] , ["ttbar_bb",ROOT.kRed+3], ["ttbar_b",ROOT.kRed-2], ["ttbar_2b",ROOT.kRed-5], ["ttbar_cc",ROOT.kRed-3], ["ttW",ROOT.kGray], ["ttZ",ROOT.kGray+2], ["SingleT",ROOT.kPink], ["WJets",ROOT.kBlue-7], ["ZJets",ROOT.kBlue-9], ["DiBoson",ROOT.kBlue-4],["data",ROOT.kBlack]]

TLatexSampleNames=[ ["ttH","$\\rm t\\bar{t}H$"],["ttbar","t\bar{t}"], ["ttbar_l","$\\rm t\\bar{t}+lf$"] , ["ttbar_bb","$\\rm t\\bar{t}+b\\bar{b}$"], ["ttbar_b","$\\rm t\\bar{t}+b$"],["ttbar_2b","$\\rm t\\bar{t}+2b$"], ["ttbar_cc","$\\rm t\\bar{t}+c\\bar{c}$"], ["ttW","$\\rm t\\bar{t}+W$"], ["ttZ","$\\rm t\\bar{t}+Z$"], ["SingleT","Single t"], ["WJets","W+jets"], ["ZJets","Z+jets"], ["DiBoson","Diboson"],["data","Data"]]
