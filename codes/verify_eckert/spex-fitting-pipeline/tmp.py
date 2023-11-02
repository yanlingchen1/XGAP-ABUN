from my_io import IO
from glob import glob

date = 231019

# # Some basic prefixes
# srcnum = '9647'
# srcname1 = f'ID{srcnum}'
# srcname2 = f'SDSSTG{srcnum}'
# root_dir = glob(f"/Users/eusracenorth/Documents/work/XGAP-ABUN/data/{srcname1}/eckert/{srcname1}/*")[0]
# io_instance = IO(date, root_dir, srcname1, srcname2)

## RGH80
srcname = f'RGH80'
root_dir = glob(f"/Users/eusracenorth/Documents/work/XGAP-ABUN/data/{srcname}/eckert/*")[0]
io_instance = IO(date, root_dir, '', srcname)

# # io issues
# io_instance.edit_hduclas3()
io_instance.xspec2spex()
