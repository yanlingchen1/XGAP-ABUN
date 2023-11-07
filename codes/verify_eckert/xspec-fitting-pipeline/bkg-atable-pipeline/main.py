from atable_allbkg import AtableBKG
from glob import glob
from my_io import IO

date = 231107

## Some mandatory parameters
nH_dict = {'SDSSTG3460':0.024, 'SDSSTG9647':0.0201, 'SDSSTG828':0.0303, 'RGH80':0.0131}
reds_dict = {'SDSSTG3460':0.043, 'SDSSTG9647':0.023, 'SDSSTG828':0.046, 'RGH80':0.037}

###  Some basic prefixes
### RGH80 ####
# srcname1 = ''
# srcname2 = 'RGH80'
# root_dir = f"/Users/eusracenorth/Documents/work/XGAP-ABUN/data/RGH80/eckert/0105860101"
# nH = nH_dict[srcname2]
# reds = reds_dict[srcname2]

#### IDxxx ####
for srcnum in ['828', '9647']: # '3460', '828', '9647'
    srcname1 = f'ID{srcnum}'
    srcname2 = f'SDSSTG{srcnum}'
    root_dir = glob(f"/Users/eusracenorth/Documents/work/XGAP-ABUN/data/{srcname1}/eckert/{srcname1}/*")[0]

    # ######### run program ############
    nH = nH_dict[srcname2]
    reds = reds_dict[srcname2]

    # # # io issues
    # io_instance = IO(date, root_dir, srcname1, srcname2)
    # io_instance.make_output_dir()
    # io_instance.check_files()

    # # # # smooth bkg back pi
    ab = AtableBKG(date, root_dir, srcname1, srcname2, 'bkg', nH, reds)
    # ab.bkgsmooth()
    # ab.gen_qpbmdltxt()


    ## after fit oot and bkg in skybkg region in xspec pipeline
    for i in range(13):
        ab.update_inst_dict(f'reg{i}')
        # ab.bkgsmooth()
        # ab.gen_qpbmdltxt()
        # ab.atable_allbkg()
        ab.qdp2ogip()
        ab.qdp2txt()
