from glob import glob
from my_io import IO
from fit_other import FitOther
from fit_annu_allbkg import FitAnnu
from datetime import datetime
import pandas as pd
import concurrent.futures

def fit_source(srcnum, nH, reds):
    current_date = datetime.now()
    date = current_date.strftime("%y%m%d")

    REGNAME = 'R500-01'
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

def main():
    basfile = f'/data/yanling/XGAP-ABUN/codes/XGAP-ABUN/codes/ESAS/get_nh/basics_allsources.csv'
    f = pd.read_csv(basfile)

    # Define the number of worker processes (adjust as needed)
    num_workers = 4

    with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
        # Use executor.map to apply the function to each source in parallel
        futures = [executor.submit(fit_source, srcnum, nH, reds) for srcnum, nH, reds in zip(f['ID'], f['nH(1e20cm-2)'] * 1e-22, f['z'])]

        # Wait for all tasks to complete
        concurrent.futures.wait(futures)

if __name__ == "__main__":
    main()
