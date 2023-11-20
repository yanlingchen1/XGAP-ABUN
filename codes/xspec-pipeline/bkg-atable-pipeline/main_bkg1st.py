from atable_allbkg import AtableBKG
from glob import glob
from my_io import IO

date = 231115

## Some mandatory parameters
nH_dict = {'SDSSTG3460':0.024, 'SDSSTG9647':0.0201, 'SDSSTG828':0.0303, 'RGH80':0.0131}
reds_dict = {'SDSSTG3460':0.043, 'SDSSTG9647':0.023, 'SDSSTG828':0.046, 'RGH80':0.037}

REGNAME = 'R500-01'
# ##  Some basic prefixes


#### IDxxx ####
datadir = '/data/yanling/XGAP-ABUN/data/alldata/XGAP'
srcnums = [name.split('/')[-1].split('G')[-1] for name in glob(f'{datadir}/SDSSTG*')]

for srcnum in srcnums: 
    srcname1 = f'ID{srcnum}'
    srcname2 = f'SDSSTG{srcnum}'
    root_dir = glob(f"/{srcname2}")[0]

    # ######### run program ############
    nH = nH_dict[srcname2]
    reds = reds_dict[srcname2]

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


