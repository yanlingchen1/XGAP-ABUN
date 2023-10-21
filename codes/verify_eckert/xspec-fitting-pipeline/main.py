from glob import glob
from my_io import IO
from fit_spec import FitSpec
from datetime import datetime

def main():
    # Define the root directory where data are
    root_dir = glob("/Users/eusracenorth/Documents/work/XGAP-ABUN/data/ID828/eckert/ID828/*")[0]
    
    # # define date of fitting 
    # current_date = datetime.now()
    # date = current_date.strftime("%y%m%d")
    date = 231019

    # Some basic prefixes
    srcnum = '828'
    srcname1 = f'ID{srcnum}'
    srcname2 = f'SDSSTG{srcnum}'

    # # io issues
    io_instance = IO(date, root_dir, srcname1, srcname2)
    # io_instance.make_output_dir()
    # io_instance.check_files()

    ## fit the spectrums
    fit_pipeline = FitSpec(date, root_dir, srcname1, srcname2, 'bkg', 0.0303, 0.046) # last two: nH and reds
    # fit_pipeline.fit_oot()
    # fit_pipeline.fit_qpb_pn()
    # fit_pipeline.fit_bkg(0.0303)
    # io_instance.tidy_bkgpar()


    for i in range(13):
        fit_pipeline.update_inst_dict(f'reg{i}')
        fit_pipeline.fit_oot()
        fit_pipeline.fit_data()

if __name__ == "__main__":
    main()






