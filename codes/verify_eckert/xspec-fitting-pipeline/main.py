from glob import glob
from my_io import IO
from fit_other import FitOther
from fit_annu import FitAnnu
from datetime import datetime

def main():
    # # define date of fitting 
    # current_date = datetime.now()
    # date = current_date.strftime("%y%m%d")
    date = 231019

    ####  Some basic prefixes
    ### RGH80 ####
    srcname1 = ''
    srcname2 = 'RGH80'
    root_dir = f"/Users/eusracenorth/Documents/work/XGAP-ABUN/data/RGH80/eckert/0105860101"

    # #### IDxxx ####
    # srcnum = '9647'
    # srcname1 = f'ID{srcnum}'
    # srcname2 = f'SDSSTG{srcnum}'
    # root_dir = glob(f"/Users/eusracenorth/Documents/work/XGAP-ABUN/data/{srcname1}/eckert/{srcname1}/*")[0]

    ### Some mandatory parameters
    # ## ID3460
    # nH = 0.024
    # reds = 0.043

    # ## ID9647
    # nH = 0.0201
    # reds = 0.023

    # ## ID828
    # nH = 0.0303
    # reds = 0.046

    ## RGH80
    nH = 0.0131
    reds = 0.037

    # # io issues
    io_instance = IO(date, root_dir, srcname1, srcname2)
    # io_instance.make_output_dir()
    # io_instance.check_files()

    # ## fit the spectrums
    # fit_other = FitOther(date, root_dir, srcname1, srcname2, 'bkg', nH, reds) 
    # fit_other.fit_oot()
    # fit_other.fit_qpb_pn()
    # fit_other.fit_bkg()
    # io_instance.tidy_bkgpar()

    fit_annu = FitAnnu(date, root_dir, srcname1, srcname2, 'reg0', nH, reds) 
    for i in range(13):
    #     fit_other.update_inst_dict(f'reg{i}')
        fit_annu.update_inst_dict(f'reg{i}')
    #     fit_other.fit_oot()
    #     fit_annu.fit_1T()
        fit_annu.fit_2T()

    #### for 2T model ####
    bigkeys = ['T', 'Z', 'n', 'T2', 'n2'], 
    resonable_vrange = {'T':[0,5] , 'Z':[0,2] ,'n':[0,1e-2], 'T2':[0,5] , 'n2':[0,1e-2] }
    io_instance.tidy_outputs('2T', bigkeys = bigkeys, reson_vrange = resonable_vrange)

    # fit_annu.refit_1T_Z_uc()
    # io_instance.tidy_outputs_2nd()


if __name__ == "__main__":
    main()






