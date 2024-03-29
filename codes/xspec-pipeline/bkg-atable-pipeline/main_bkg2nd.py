from atable_allbkg import AtableBKG
from glob import glob
from my_io import IO
import pandas as pd

date = 231115

## Some mandatory parameters
REGNAME = 'big1-src'

basfile = f'/data/yanling/XGAP-ABUN/codes/XGAP-ABUN/codes/ESAS/get_nh/basics_allsources.csv'
f = pd.read_csv(basfile)
ids = f['ID'][2:]
ids = ['SDSSTG828']
for i, srcnum in enumerate(ids): 
    srcnum = srcnum.split('G')[-1]
    nH = f['nH(1e20cm-2)'][i]
    reds = f['z'][i]

    srcname1 = f'ID{srcnum}'
    srcname2 = f'SDSSTG{srcnum}'
    if glob(f"/data/yanling/XGAP-ABUN/data/alldata/XGAP/{srcname2}"):
        root_dir = glob(f"/data/yanling/XGAP-ABUN/data/alldata/XGAP/{srcname2}")[0]
    

        ## after fit oot and bkg in skybkg region in xspec pipeline
        ab = AtableBKG(date, root_dir, srcname1, srcname2, REGNAME, nH, reds)
        ab.bkgsmooth()
        ab.gen_qpbmdltxt()
        ab.atable_allbkg()
        ab.qdp2ogip()
        ab.qdp2txt()
