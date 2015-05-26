#helper functions to write a table

def write_syst(file,value):
    file.write(value[0]+' &')
    for val in value[1:-1]:
      file.write(val+" &")
    file.write(value[-1])
    file.write('\\\\ \n')

def write_foot(file):
    file.write('\\hline\n')
    file.write('\end{tabular}\n')
    file.write('\\end{center}\n')

def write_head(file,columns):
    #print columns
    file.write('\\begin{center}\n')
    file.write('\\begin{tabular}{l')
    for entry in columns[1:]:
        file.write('c')
    file.write('}\n')
    file.write('\\hline\n')
    for entry in columns[:-1]:
        file.write(entry+' &')
    file.write(columns[-1]+' \\\\ \n')
    file.write('\\hline\n')