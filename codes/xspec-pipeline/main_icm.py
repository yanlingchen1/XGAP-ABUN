from glob import glob
from my_io import IO
from fit_other import FitOther
from fit_annu_allbkg import FitAnnu
from datetime import datetime
import pandas as pd


def main():
    # # define date of fitting 
    # current_date = datetime.now()
    # date = current_date.strftime("%y%m%d")
    date = 231115

    REGNAME = 'R500-01'
    # ##  Some basic prefixes
    basfile = f'/data/yanling/XGAP-ABUN/codes/XGAP-ABUN/codes/ESAS/get_nh/basics_allsources.csv'
    f = pd.read_csv(basfile)

    for i, srcnum in enumerate(f['ID']): 
        srcnum = srcnum.split('G')[-1]
        nH = f['nH(1e20cm-2)'][i] * 1e-22
        reds = f['z'][i]

        srcname1 = f'ID{srcnum}'
        srcname2 = f'SDSSTG{srcnum}'
        root_dir = glob(f"/data/yanling/XGAP-ABUN/data/alldata/XGAP/{srcname2}")[0]


        # fit source 
        fit_other = FitOther(date, root_dir, srcname1, srcname2, REGNAME, nH, reds)
        fit_other.update_inst_dict(REGNAME)
        fit_other.fit_oot()
        #### allbkg, 1T ####
        fit_annu = FitAnnu(date, root_dir, srcname1, srcname2, REGNAME, nH, reds)
        # fit_annu.update_inst_dict(REGNAME)
        fit_annu.fit_annu('1T')
        fit_annu.fit_annu('GDEM')


if __name__ == "__main__":
    main()






