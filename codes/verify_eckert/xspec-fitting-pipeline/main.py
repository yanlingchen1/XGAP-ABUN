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

    ## Some mandatory parameters
    nH_dict = {'SDSSTG3460':0.024, 'SDSSTG9647':0.0201, 'SDSSTG828':0.0303, 'RGH80':0.0131}
    reds_dict = {'SDSSTG3460':0.043, 'SDSSTG9647':0.023, 'SDSSTG828':0.046, 'RGH80':0.037}

    ###  Some basic prefixes
    # ### RGH80 ####
    # srcname1 = ''
    # srcname2 = 'RGH80'
    # root_dir = f"/Users/eusracenorth/Documents/work/XGAP-ABUN/data/RGH80/eckert/0105860101"
    # nH = nH_dict[srcname2]
    # reds = reds_dict[srcname2]

    #### IDxxx ####
    for srcnum in ['3460']: # , '9647', '828'
        srcname1 = f'ID{srcnum}'
        srcname2 = f'SDSSTG{srcnum}'
        root_dir = glob(f"/Users/eusracenorth/Documents/work/XGAP-ABUN/data/{srcname1}/eckert/{srcname1}/*")[0]

        nH = nH_dict[srcname2]
        reds = reds_dict[srcname2]

    # # io issues
    io_instance = IO(date, root_dir, srcname1, srcname2)
    # io_instance.make_output_dir()
    # io_instance.check_files()
    
    # ## fit the spectrums
    fit_other = FitOther(date, root_dir, srcname1, srcname2, 'bkg', nH, reds) 
    # fit_other.fit_oot()
    # fit_other.fit_qpb_pn()
    # fit_other.fit_bkg()
    # io_instance.tidy_bkgpar()

    # fit_annu = FitAnnu(date, root_dir, srcname1, srcname2, 'reg0', nH, reds) 
    # for i in range(13):
    #     fit_other.update_inst_dict(f'reg{i}')
        # fit_annu.update_inst_dict(f'reg{i}')
    #     fit_other.fit_oot()

    # fit_other.fit_qpb_mos(1)
    # fit_other.fit_qpb_mos(2)
    # print(fit_other.get_backscal())
    #     fit_annu.fit_1T()
        # fit_annu.fit_2T_fixT2()
        # fit_annu.fit_gadem()


    # # #### for GADEM model ####
    # bigkeys = ['T', 'Tsig', 'Z', 'n']
    # resonable_vrange = {'T':[0,5] , 'Tsig':[0,10], 'Z':[0,2] ,'n':[0,1e-2]}
    # io_instance.tidy_outputs('_GADEM', bigkeys = bigkeys, reson_vrange = resonable_vrange)

    # # #### for 2T model ####
    # bigkeys = ['T', 'Z', 'n', 'n2']
    # resonable_vrange = {'T':[0,5] , 'Z':[0,2] ,'n':[0,1e-2], 'n2':[0,1e-2] }
    # io_instance.tidy_outputs('_2T_fixT2', bigkeys = bigkeys, reson_vrange = resonable_vrange)

    #### for 1T model ####
    # io_instance.tidy_outputs('')
    # fit_annu.refit_1T_Z_uc()
    # io_instance.tidy_outputs_2nd('', 'refit_Z_uc')


if __name__ == "__main__":
    main()






