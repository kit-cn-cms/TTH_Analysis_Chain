import ROOT
import sys

ROOT.gDirectory.cd('PyROOT:/')

catNames=[
  ["43","ljets_j4_t3"],
  ["44","ljets_j4_t4"],
  ["53","ljets_j5_t3"],
  ["54","ljets_j5_tge4"],
  ["62","ljets_jge6_t2"],
  ["63","ljets_jge6_t3"],
  ["64","ljets_jge6_tge4"],
]

samples=[
  ["tthbb","ttH125"],
  ["ttbar_bb","ttbarPlusBBbar"],
  ["ttbar_cc","ttbarPlusCCbar"],
  ["ttbar_light","ttbarOther"],
  ["ttbar_2b","ttbarPlus2B"],
  ["ttbar_b","ttbarPlusB"],
  ["data","data"],
  ]

systs=[
  ["nominal",""],
  ["CSVLF","CMS_ttH_CSVLF"],
  ["CSVHF","CMS_ttH_CSVHF"],
  ["CSVHFStats1","CMS_ttH_CSVHFStats1"],
  ["CSVHFStats2","CMS_ttH_CSVHFStats2"],
  ["CSVLFStats1","CMS_ttH_CSVLFStats1"],
  ["CSVLFStats2","CMS_ttH_CSVLFStats2"],
  ["CMS_scale_j","CMS_scale_j"],
  ["obs","obs"],
  ]



histofile=sys.argv[2]
cat=sys.argv[1]

for c in catNames:
  if cat==c[0]:
    cat=c[1]

histos=[]
infile=ROOT.TFile(histofile,"READ")
keys=infile.GetListOfKeys()

print keys, len(keys)
for k in keys:
  print "--------------"
  print k.GetName()
  hnameOld=k.GetName()
  h=infile.Get(hnameOld)
  #print h.GetName()
  if "data" in hnameOld:
    hnameOld="output_nominal_data"
# hnamelist=hnameOld.rsplit("_",1)
  sNameNew=""
  sysNameNew=""
  discNameNew="BDT"
  for s in samples:
    if s[0] in hnameOld and (hnameOld.find(s[0])+len(s[0]))==len(hnameOld):
      sNameOld=s[0]
      sNameNew=s[1]
#  print sNameOld, " -> ", sNameNew
  hnameOld=hnameOld.replace("output_","")
  hnameOld=hnameOld.replace("_"+sNameOld,"")
#  print hnameOld
  for s in systs:
    if s[0] == hnameOld:
      sysNameOld=s[0]
      sysNameNew=s[1]
    elif s[0]+"Up" == hnameOld:
      sysNameOld=s[0]+"Up"
      sysNameNew=s[1]+"Up"
    elif s[0]+"Down" == hnameOld:
      sysNameOld=s[0]+"Down"
      sysNameNew=s[1]+"Down"
#  print sysNameOld, " -> ", sysNameNew
  hnameNew=sNameNew+"_"+discNameNew+"_"+cat
  if sysNameNew!="":
    hnameNew+="_"+sysNameNew
  print " => ",hnameNew
#  h.SetDirectory(0)
  if "data" in hnameNew:
    hnameNew="data_obs"+"_"+"BDT"+"_"+cat
  histoNew=h.Clone(hnameNew)
  histoNew.SetDirectory(0)
  histoNew.SetName(hnameNew)
  histoNew.SetTitle(hnameNew)
  histos.append(histoNew)
  
infile.Close()

outfileName=histofile.replace(".root","_NOVA.root")
#print outfileName
#print histos
#print len(histos)
outfile=ROOT.TFile(outfileName,"RECREATE")
for h in histos:
  h.Write()
newkeyslist=outfile.GetListOfKeys()
#print len(newkeyslist)
outfile.Close()




