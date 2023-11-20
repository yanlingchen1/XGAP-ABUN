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
        if glob(f"/data/yanling/XGAP-ABUN/data/alldata/XGAP/{srcname2}"):
            root_dir = glob(f"/data/yanling/XGAP-ABUN/data/alldata/XGAP/{srcname2}")[0]


            # # io issues
            io_instance = IO(date, root_dir, srcname1, srcname2)
            fit_other = FitOther(date, root_dir, srcname1, srcname2, REGNAME, nH, reds) 
            fit_other.grp_spec()
            fit_other.edit_headers()
            io_instance.make_output_dir()
            # io_instance.check_files()
            
            
            # # ## fit the sky bkg, after fit the qpb in bkgatablepiipeline
            fit_other = FitOther(date, root_dir, srcname1, srcname2, 'bkg', nH, reds)
            fit_other.grp_spec()
            fit_other.fit_oot()
            fit_other.fit_bkg()
            io_instance.tidy_bkgpar()


if __name__ == "__main__":
    main()







