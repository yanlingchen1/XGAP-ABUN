from glob import glob
from my_io import IO
from fit_frame import FitFrame
from fit_other import FitOther
from fit_annu import FitAnnu
from datetime import datetime

def main():
    # # define date of fitting 
    # current_date = datetime.now()
    # date = current_date.strftime("%y%m%d")
    date = 231107

    ## Some mandatory parameters
    nH_dict = {'SDSSTG3460':0.024, 'SDSSTG9647':0.0201, 'SDSSTG828':0.0303, 'RGH80':0.0131}
    reds_dict = {'SDSSTG3460':0.043, 'SDSSTG9647':0.023, 'SDSSTG828':0.046, 'RGH80':0.037}

    REGNAME = 'R500-01'
    ##  Some basic prefixes
    # ### RGH80 ####
    # srcname1 = ''
    # srcname2 = 'RGH80'
    # root_dir = f"/Users/eusracenorth/Documents/work/XGAP-ABUN/data/RGH80/eckert/0105860101"


    #### IDxxx ####
    for srcnum in ['3460']: # '3460', '9647', '828'
        # srcnum = '3460'
        srcname1 = f'ID{srcnum}'
        srcname2 = f'SDSSTG{srcnum}'
        root_dir = glob(f"/data/yanling/XGAP-ABUN/data/alldata/XGAP/{srcname2}")[0]
    
    ## CAUTIOUS: {nH in spex} = 1e-2*{nH in xspec}
    nH = nH_dict[srcname2] * 1e-2 
    reds = reds_dict[srcname2]

    # # # io issues
    io_instance = IO(date, root_dir, srcname1, srcname2)
    io_instance.make_output_dir()
    io_instance.edit_hduclas3()
    io_instance.xspec2spex()


    #fit_other = FitOther(date, root_dir, srcname1, srcname2, 'bkg', nH, reds)
    #fit_annu = FitAnnu(date, root_dir, srcname1, srcname2, 'bkg', nH, reds)
    #fit_annu.fit_annu('1T')
    #io_instance.tidy_outputs('1T')
    # io_instance.make_output_dir()
    # io_instance.edit_hduclas3()
    # io_instance.xspec2spex()


    # fit_other = FitOther(date, root_dir, srcname1, srcname2, REGNAME, nH, reds)
    #fit_annu = FitAnnu(date, root_dir, srcname1, srcname2, REGNAME, nH, reds)
    # fit_other.fit_oot()
    # fit_annu.fit_annu('1T')
   # fit_annu.fit_annu('GDEM')
    # io_instance.tidy_outputs('1T')
    
if __name__ == "__main__":
    main()






