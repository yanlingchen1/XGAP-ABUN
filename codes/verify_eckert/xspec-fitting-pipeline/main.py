from glob import glob
from my_io import IO
from fit_spec import FitSpec
from datetime import datetime

def main():
    
    
    # # define date of fitting 
    # current_date = datetime.now()
    # date = current_date.strftime("%y%m%d")
    date = 231019

    # Some basic prefixes
    srcnum = '3460'
    srcname1 = f'ID{srcnum}'
    srcname2 = f'SDSSTG{srcnum}'

    # Define the root directory where data are
    root_dir = glob(f"/Users/eusracenorth/Documents/work/XGAP-ABUN/data/{srcname1}/eckert/{srcname1}/*")[0]

    # # io issues
    io_instance = IO(date, root_dir, srcname1, srcname2)
    # io_instance.make_output_dir()
    # io_instance.check_files()

    ## fit the spectrums
    fit_pipeline = FitSpec(date, root_dir, srcname1, srcname2, 'bkg', 0.024, 0.043) # last two: nH and reds
    fit_pipeline.fit_oot()
    fit_pipeline.fit_qpb_pn()
    fit_pipeline.fit_bkg()
    io_instance.tidy_bkgpar()


    for i in range(13):
        fit_pipeline.update_inst_dict(f'reg{i}')
        fit_pipeline.fit_oot()
        fit_pipeline.fit_data()

if __name__ == "__main__":
    main()






