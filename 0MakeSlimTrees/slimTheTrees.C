#include "TreeHeader.h"

void slimTheTrees(string sampleName="", string inSample="", string OutSample=""){
  
   // define selections -------------------------------------------------
  string Dr_Lep_TopJet    = "sqrt(pow(Eta_TopJet-Eta_PrimaryLepton,2)+pow(min(TMath::Abs(Phi_TopJet-Phi_PrimaryLepton),(atan(1.0)*8)-(TMath::Abs(Phi_TopJet-Phi_PrimaryLepton))),2))";
  string Dr_Lep_HiggsJet  = "sqrt(pow(Eta_HiggsJet-Eta_PrimaryLepton,2)+pow(min(TMath::Abs(Phi_HiggsJet-Phi_PrimaryLepton),(atan(1.0)*8)-(TMath::Abs(Phi_HiggsJet-Phi_PrimaryLepton))),2))";
  string Deta_TopCand_HiggsCand_TopLikelihood = "TMath::Abs(Eta_HiggsCandidate_TopLikelihood - Eta_TopHadCandidate_TopLikelihood)";
  
  string Selection="";

  AddSample(sampleName,inSample,"MVATree",Selection);
  AddBin("all","all","");

      
TFile *file0 = TFile::Open(inSample.c_str(),"READ");
  TTree* Mytree = (TTree*) file0->Get("MVATree");
  int nBranches = Mytree->GetNbranches();
  TString BranchName;
  TString BranchTitle;
  TObjArray* BranchList = Mytree->GetListOfBranches();

for(int i=0; i<nBranches; i++){
   BranchName =(TString) BranchList->At(i)->GetName();
   BranchTitle = (TString)BranchList->At(i)->GetTitle();
   if( BranchName.Contains("BoostedTop") || BranchName.Contains("BoostedHiggs") || BranchName.Contains("Evt") || BranchName.Contains("Weight") || BranchName.Contains("N_") || BranchName.Contains("TaggedJet_")){
        TString varSize="";
        if(BranchTitle.Contains("[")){
          int a,b;
          a=BranchTitle.First("[");
          b=BranchTitle.First("]");
          int c=b-a;
          varSize = BranchTitle(a+1,c-1);
//           std::cout<<BranchName<<"  Array Variable with size "<<varSize<<std::endl;
          }
        TString varType="";
        varType=BranchTitle[BranchTitle.Length()-1];
//         std::cout<<BranchName<<"  Variable with type "<<varType<<std::endl;
        AddVar((char*)BranchName.Data(),(char*)varType.Data(),(char*)varSize.Data(),(char*)BranchName.Data() );          
     }
}
  
  
  
  
//  additional variables -----------------------------------------------------
  AddVar("GenHiggs_Pt","F","","GenHiggs_Pt" );
  AddVar("GenHiggs_Phi","F","","GenHiggs_Phi" );
  AddVar("GenHiggs_Eta","F","","GenHiggs_Eta" );
  AddVar("GenTopHad_Pt","F","N_GenTopHad","GenTopHad_Pt" );
  AddVar("GenTopHad_Phi","F","N_GenTopHad","GenTopHad_Phi" );
  AddVar("GenTopHad_Eta","F","N_GenTopHad","GenTopHad_Eta" );
  AddVar("Jet_Pt","F","N_Jets","Jet_Pt" );
  AddVar("Jet_Eta","F","N_Jets","Jet_Eta" );
  AddVar("Jet_Phi","F","N_Jets","Jet_Phi" );
  AddVar("Jet_Phi","F","N_Jets","Jet_Phi" );
  AddVar("Jet_Phi","F","N_Jets","Jet_Phi" );

  AddVar("CSV","F","N_Jets","CSV");
  AddVar("CSV2","F","","CSV[2]" );
  AddVar("CSV3","F","","CSV[3]" );
  
  AddVar("CSV_B_TopHadCandidate_DB","F","","max(BoostedTopHiggs_TopHadCandidate_B_CSV, -1.1)" );
  AddVar("CSV_B_TopHadCandidate_SBT","F","","max(BoostedTop_TopHadCandidate_B_CSV, -1.1)" );
  AddVar("CSV_B_TopHadCandidate_SBH","F","","max(BoostedHiggs_TopHadCandidate_B_CSV, -1.1)" );

/*  AddVar("Detamax_Lepton_Jet2","F","","Detamax_Lepton_Jet[2]");*/
//   AddVar("Sqrt_Deta_THC_Deta_TLC","F","","TMath::Sqrt(Deta_TopHadCandidate_HiggsCandidate_TopLikelihood*Deta_TopLepCandidate_HiggsCandidate_TopLikelihood)");
//   AddVar("Sqrt_Deta_THC_Deta_TLC","F","","TMath::Sqrt(Deta_TopHadCandidate_HiggsCandidate_TopLikelihood*Deta_TopLepCandidate_HiggsCandidate_TopLikelihood)");


  AddVar("MaxDeta_Jet_AveEtaJet","F","","Max$(TMath::Abs(Jet_Eta-Sum$(Jet_Eta)/Length$(Jet_Eta)))" );
  AddVar("Subjetiness21_HiggsCandidate_DB","F","","BoostedTopHiggs_HiggsCandidate_Subjetiness2/BoostedTopHiggs_HiggsCandidate_Subjetiness1" );
  AddVar("Subjetiness32_HiggsCandidate_DB","F","","BoostedTopHiggs_HiggsCandidate_Subjetiness3/BoostedTopHiggs_HiggsCandidate_Subjetiness2" );
  AddVar("Subjetiness31_HiggsCandidate_DB","F","","BoostedTopHiggs_HiggsCandidate_Subjetiness3/BoostedTopHiggs_HiggsCandidate_Subjetiness1" );

  AddVar("Subjetiness21_HiggsCandidate_SBH","F","","BoostedHiggs_HiggsCandidate_Subjetiness2/BoostedHiggs_HiggsCandidate_Subjetiness1" );
  AddVar("Subjetiness32_HiggsCandidate_SBH","F","","BoostedHiggs_HiggsCandidate_Subjetiness3/BoostedHiggs_HiggsCandidate_Subjetiness2" );
  AddVar("Subjetiness31_HiggsCandidate_SBH","F","","BoostedHiggs_HiggsCandidate_Subjetiness3/BoostedHiggs_HiggsCandidate_Subjetiness1" );
  
  AddVar("PtTaggedOverJetE","F","","Sum$(TaggedJet_Pt)/Sum$(Jet_E)" );
  AddVar("MaxAbsEta_TaggedJet","F","","Max$(TMath::Abs(TaggedJet_Eta))" );
  AddVar("MaxAbsEta_Jet","F","","Max$(TMath::Abs(Jet_Eta))" );

  AddVar("Jet_Pt2","F","","Jet_Pt[1]");
  AddVar("Jet_Pt1","F","","Jet_Pt[0]");
  AddVar("Jet_Pt3","F","","Jet_Pt[2]");
  AddVar("Jet_Pt4","F","","Jet_Pt[3]");
  
 
  // end add variables -------------------------------------------------
  
  bool flatTrees = false;
  bool appendVariables = false;
  
  SetOutFileDir(OutSample);
  
  FillAllTrees(flatTrees,appendVariables);
}
