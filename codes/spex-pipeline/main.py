from glob import glob
from my_io import IO
from fit_frame import FitFrame
from fit_other import FitOther
from fit_annu import FitAnnu
from datetime import datetime
import pandas as pd





def main():
    date = 231115

    REGNAME = 'R500-01'
    # ##  Some basic prefixes
    basfile = f'/data/yanling/XGAP-ABUN/codes/XGAP-ABUN/codes/ESAS/get_nh/basics_allsources.csv'
    f = pd.read_csv(basfile)
    #spex_set = ['SDSSTG10159', 'SDSSTG39344', 'SDSSTG16386']
    ids = f['ID']
    #ids =spex_set
    for i, srcnum in enumerate(ids): 
        srcnum = srcnum.split('G')[-1]
        nH = f['nH(1e20cm-2)'][i] * 1e-24
        reds = f['z'][i]

        srcname1 = f'ID{srcnum}'
        srcname2 = f'SDSSTG{srcnum}'
        if glob(f"/data/yanling/XGAP-ABUN/data/alldata/XGAP/{srcname2}"):
            root_dir = glob(f"/data/yanling/XGAP-ABUN/data/alldata/XGAP/{srcname2}")[0]
            # # # io issues
            io_instance = IO(date, root_dir, srcname1, srcname2)
            #io_instance.make_output_dir()
            #io_instance.edit_hduclas3()
            #io_instance.xspec2spex()


            fit_other = FitOther(date, root_dir, srcname1, srcname2, REGNAME, nH, reds)
            fit_annu = FitAnnu(date, root_dir, srcname1, srcname2, REGNAME, nH, reds)
            #fit_other.fit_oot()
            #fit_annu.fit_annu('1T')
            #fit_annu.fit_annu('GDEM')
            #fit_annu.fit_annu('GDEM-logT')
            io_instance.tidy_outputs('GDEM', bigkeys = ['n', 'T', 'Tsig', 'Z'], reson_vrange = {'T':[0,5] , 'Z':[0,2] , 'Tsig':[0,5], 'n':[0,1e7]}) 
if __name__ == "__main__":
    main()







