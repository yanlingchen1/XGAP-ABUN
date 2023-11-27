from glob import glob
from my_io import IO
from fit_frame import FitFrame
from fit_other import FitOther
from fit_annu import FitAnnu
from datetime import datetime
import pandas as pd





def main():
    date = 231115
    
    spex_set1 = ['SDSSTG8050','SDSSTG10842','SDSSTG885','SDSSTG1011','SDSSTG4654']
    spex_set2 = ['SDSSTG1695','SDSSTG15641','SDSSTG3128'
    ,'SDSSTG12349','SDSSTG16150']
    spex_set3 = ['SDSSTG3460','SDSSTG9771','SDSSTG10094'
    ,'SDSSTG5742','SDSSTG6058','SDSSTG1162']
    spex_set4 = ['SDSSTG15354','SDSSTG2424'
    ,'SDSSTG46701','SDSSTG35976','SDSSTG9399','SDSSTG4436']
    spex_set5 = ['SDSSTG9647'
    ,'SDSSTG4936','SDSSTG828','SDSSTG15776','SDSSTG9370','SDSSTG21128']
    spex_set6 = ['SDSSTG1398','SDSSTG40241','SDSSTG11844','SDSSTG4047','SDSSTG3513'
    ,'SDSSTG16393']

    REGNAME = 'R500-01'
    # ##  Some basic prefixes
    basfile = f'/data/yanling/XGAP-ABUN/codes/XGAP-ABUN/codes/ESAS/get_nh/basics_allsources.csv'
    f = pd.read_csv(basfile)


    # ids = f['ID']
    ids = spex_set1
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
            io_instance.make_output_dir()
            io_instance.edit_hduclas3()
            io_instance.xspec2spex()


            fit_other = FitOther(date, root_dir, srcname1, srcname2, REGNAME, nH, reds)
            fit_annu = FitAnnu(date, root_dir, srcname1, srcname2, REGNAME, nH, reds)
            fit_other.fit_oot()
            fit_annu.fit_annu('1T')
            fit_annu.fit_annu('GDEM')
            # io_instance.tidy_outputs('1T')
            
if __name__ == "__main__":
    main()






