from glob import glob
import numpy as np
import re

savepath = '/Users/eusracenorth/Documents/work/XGAP-ABUN/data/ID828/eckert/ID828/0904720501/fit_231019'

def sort_files(flist):
    pattern = r'_reg(\d+)'
    idxlst = []
    for file_name in flist:
        match = re.search(pattern, file_name)
        number = match.group(1)
        idxlst.append(int(number))
    print(idxlst)
    print(np.sort(idxlst))
    return np.argsort(idxlst)

files = glob(f'{savepath}/logs/annu_reg*_freepar.log')
files = np.array(files)[sort_files(files)]
# print(files)
# for file in files:
#     with open(file) as f:
#         lines = f.readlines()[11:14]
#         for i, line in enumerate(lines):
#                 value = line.split('+/-')[0].split()[-1]
#                 print(value)