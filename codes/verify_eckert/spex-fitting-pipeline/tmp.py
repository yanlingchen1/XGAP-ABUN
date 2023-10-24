from my_io import IO
from glob import glob

date = 231019

# Some basic prefixes
srcnum = '828'
srcname1 = f'ID{srcnum}'
srcname2 = f'SDSSTG{srcnum}'

## ID9647
nH = 0.0201
reds = 0.023
root_dir = glob(f"/Users/eusracenorth/Documents/work/XGAP-ABUN/data/{srcname1}/eckert/{srcname1}/*")[0]

# # io issues
io_instance = IO(date, root_dir, srcname1, srcname2)
io_instance.edit_hduclas3()
