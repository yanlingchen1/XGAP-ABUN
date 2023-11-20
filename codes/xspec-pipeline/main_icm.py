from glob import glob
from my_io import IO
from fit_other import FitOther
from fit_annu_allbkg import FitAnnu
from datetime import datetime

def main():
    # # define date of fitting 
    # current_date = datetime.now()
    # date = current_date.strftime("%y%m%d")
    date = 231115

    ## Some mandatory parameters
    nH_dict = {'SDSSTG3460':0.024, 'SDSSTG9647':0.0201, 'SDSSTG828':0.0303, 'RGH80':0.0131}
    reds_dict = {'SDSSTG3460':0.043, 'SDSSTG9647':0.023, 'SDSSTG828':0.046, 'RGH80':0.037}


    REGNAME = 'R500-01'
    # ##  Some basic prefixes

    #### IDxxx ####
    for srcnum in ['3460']: # '3460', '9647', '828'
        srcname1 = f'ID{srcnum}'
        srcname2 = f'SDSSTG{srcnum}'
        root_dir = glob(f"/data/yanling/XGAP-ABUN/data/alldata/XGAP/{srcname2}")[0]
        nH = nH_dict[srcname2]
        reds = reds_dict[srcname2]

        # # io issues
        io_instance = IO(date, root_dir, srcname1, srcname2)
        fit_other = FitOther(date, root_dir, srcname1, srcname2, REGNAME, nH, reds) 
#        fit_other.grp_spec()
#        fit_other.edit_headers()
#        io_instance.make_output_dir()
        # io_instance.check_files()
        
        
        # # ## fit the sky bkg, after fit the qpb in bkgatablepiipeline
        fit_other = FitOther(date, root_dir, srcname1, srcname2, 'bkg', nH, reds)
        #fit_other.grp_spec()
        #fit_other.edit_headers()
        #fit_other.fit_oot()
        #fit_other.fit_bkg()
        #io_instance.tidy_bkgpar()

       # fit source 
        fit_other.update_inst_dict(REGNAME)
        #fit_other.fit_oot()
        #### allbkg, 1T ####
        fit_annu = FitAnnu(date, root_dir, srcname1, srcname2, REGNAME, nH, reds)

        # fit_annu.update_inst_dict(REGNAME)
        fit_annu.fit_annu('1T')
        fit_annu.fit_annu('GDEM')

        # io_instance.tidy_outputs('1T')

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

    # #### allbkg, 1T ####
    # fit_annu.fit_annu('1T')

if __name__ == "__main__":
    main()






