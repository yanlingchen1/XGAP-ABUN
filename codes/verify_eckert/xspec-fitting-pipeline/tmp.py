from fit_other import FitOther
from glob import glob

date = 231019

# Some basic prefixes
srcnum = '9647'
srcname1 = f'ID{srcnum}'
srcname2 = f'SDSSTG{srcnum}'

## ID9647
nH = 0.0201
reds = 0.023
root_dir = glob(f"/Users/eusracenorth/Documents/work/XGAP-ABUN/data/{srcname1}/eckert/{srcname1}/*")[0]

# # io issues
fit_other = FitOther(date, root_dir, srcname1, srcname2, 'reg5', nH, reds) 
fit_other.update_inst_dict('reg0')
