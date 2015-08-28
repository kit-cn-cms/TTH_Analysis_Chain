import sys

inputDataCard=sys.argv[1]
print "doing card ", inputDataCard

SystematicsToRemove=[
    "CMS_scale_j",
    "CSVLF",
    "CSVHFStats1",
    "CSVHFStats2",
    "CSVLFStats2",
  ]

for sys in SystematicsToRemove:
  infile=open(inputDataCard,"r")
  inlines=list(infile)
  infile.close()
  outfile=open(inputDataCard+"_NO_"+sys,"w")
  for l in inlines:
    substrings=l.split("\t")
    #print substrings, sys
    if sys!=substrings[0]:
      outfile.write(l)
  outfile.close()

infile=open(inputDataCard,"r")
inlines=list(infile)
infile.close()
outfile=open(inputDataCard+"_NO_Shapes","w")
for l in inlines:
  substrings=l.split("\t")
  if substrings[0] not in SystematicsToRemove:
    outfile.write(l)
outfile.close()
