from atable_allbkg import AtableBKG
from glob import glob
from my_io import IO
import pandas as pd
from datetime import datetime
import pandas as pd
import concurrent.futures


def fit_source(srcnum, nH, reds):
    current_date = datetime.now()
    date = current_date.strftime("%y%m%d")

    srcname1 = f'ID{srcnum}'
    srcname2 = f'SDSSTG{srcnum}'
    root_dir = glob(f"/data/yanling/XGAP-ABUN/data/alldata/XGAP/{srcname2}")[0]

    # # # io issues
    io_instance = IO(date, root_dir, srcname1, srcname2, 'bkg', nH, reds)
    io_instance.make_output_dir()
    io_instance.check_files()
    io_instance.edit_hduclas3()

    # # # # # smooth bkg back pi
    ab = AtableBKG(date, root_dir, srcname1, srcname2, 'bkg', nH, reds)
    io_instance.edit_hduclas3()
    ab.bkgsmooth()
    ab.gen_qpbmdltxt()

def main():
    basfile = f'/data/yanling/XGAP-ABUN/codes/XGAP-ABUN/codes/ESAS/get_nh/basics_allsources.csv'
    f = pd.read_csv(basfile)

    # Define the number of worker processes (adjust as needed)
    num_workers = 50

    with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
        # Use executor.map to apply the function to each source in parallel
        futures = [executor.submit(fit_source, srcnum, nH, reds) for srcnum, nH, reds in zip(f['ID'], f['nH(1e20cm-2)'] * 1e-22, f['z'])]

        # Wait for all tasks to complete
        concurrent.futures.wait(futures)

if __name__ == "__main__":
    main()





