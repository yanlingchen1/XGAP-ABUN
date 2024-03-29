from atable_allbkg import AtableBKG
from glob import glob
from my_io import IO
import pandas as pd

date = 231115


REGNAME = 'big1_src'

basfile = f'/data/yanling/XGAP-ABUN/codes/XGAP-ABUN/codes/ESAS/get_nh/basics_allsources.csv'
f = pd.read_csv(basfile)
ids = f['ID']
ids = ['SDSSTG1162']
for i, srcnum in enumerate(ids):
    srcnum = srcnum.split('G')[-1] 
    nH = f['nH(1e20cm-2)'][i] * 1e-22
    reds = f['z'][i]

    srcname1 = f'ID{srcnum}'
    srcname2 = f'SDSSTG{srcnum}'
    
    if glob(f"/data/yanling/XGAP-ABUN/data/alldata/XGAP/{srcname2}"):
        root_dir = glob(f"/data/yanling/XGAP-ABUN/data/alldata/XGAP/{srcname2}")[0]
        print(root_dir)
        # # # io issues
        io_instance = IO(date, root_dir, srcname1, srcname2, 'bkg', nH, reds)
        io_instance.make_output_dir()
        #io_instance.check_files()
        io_instance.edit_hduclas3()

        # # # # # smooth bkg back pi
        ab = AtableBKG(date, root_dir, srcname1, srcname2, 'bkg', nH, reds)
        io_instance.edit_hduclas3()
        ab.bkgsmooth()
        ab.gen_qpbmdltxt()


