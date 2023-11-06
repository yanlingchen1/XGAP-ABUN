"""
This class load qpb only using backgrnd command in xspec
which is not correct since W-STAT xspec is not sure to be correct. 

"""

from my_io import IO
from fit_frame import FitFrame
import re
from astropy.io import fits
import numpy as np
import os
from glob import glob
import pandas as pd

class FitAnnu(FitFrame):
    def fit_annu(self, mdl):
        # Alter the inputs in sample_annu.xcm
        with open(f'{self.pipeline_path}/sample_models/annu_qpb/annu_{mdl}.xcm') as f:
            lines = f.read()

        #### MDL #####
        lines = lines.replace('MDL', mdl)
        #### general ####
        lines = self.add_gen_par(lines)
        #### oot ####
        lines = self.add_oot_xcm(lines)
        #### backscal ####
        lines = self.add_backscal(lines)
        #### skybkg ####
        lines = self.add_gen_bkgpar(lines)

        with open(f'{self.savepath}/bins/annu_{self.regname}_{mdl}_qp.xcm', 'w') as newf:
            newf.write(f'{lines}\n')

        # Begin fitting
        os.chdir(self.savepath)
        os.system(f'''
xspec<<EOT
@bins/annu_{self.regname}.xcm
EOT''')

        os.system(f'''ps2pdf annu_{self.regname}_{mdl}_qp.ps
rm annu_{self.regname}_{mdl}_qp.ps
mv annu_{self.regname}_{mdl}_qp.pdf figs
mv annu_{self.regname}_{mdl}_qp.pco dats
mv annu_{self.regname}_{mdl}_qp.qdp dats 
mv annu_{self.regname}_chain1000_{mdl}_qp.out logs''')
        print(f'annu fitting for {self.regname} has finished!')


    def refit_1T_Z_uc(self):
        """
        Read the 1st fitting para
        if the Z is unconstrained, refit the data by fix z to 0.3
        
        """
        os.chdir(self.savepath)
        # load the 1st para csv
        df = pd.read_csv(f'{self.savepath}/csvs/{self.srcname2}_annuli_mypar.csv')
        for new_regname in df['reg'][df['Z-status'] == 'u']:
            print(new_regname)
            # renew the regname
            self.update_inst_dict(new_regname)
            self.bkg_dict = self.load_bkgpar()
            print(self.regname)
            #### begin fitting ####
            replace_text = f'''
new 12 1
new 15 1e-4
new 14 {self.reds}
new 13 0.3
free 13,14
thaw 12,15
            '''
            # Alter the inputs in sample_data.xcm
            fit_text, sav_text = self.gen_text('')
            self.replace_lines(fit_text, replace_text, '#### icm ####', '### fit ###')
            newfit_text = self.edit_run_xcm('sample_data.xcm', 'refit_Z_uc')
            replace_text = f'''err 12,15'''
            newfit_text = re.sub(r'err\s+12,13,15', replace_text, newfit_text)
            # Begin fitting
            os.chdir(self.savepath)
            os.system(newfit_text)
            os.system(sav_text)

    


    if __name__ == "__main__":
        from fit_annu import FitAnnu
        date = 231019

        # Some basic prefixes
        srcnum = '9647'
        srcname1 = f'ID{srcnum}'
        srcname2 = f'SDSSTG{srcnum}'

        ## ID9647
        nH = 0.0201
        reds = 0.023
        rannu_dir = glob(f"/Users/eusracenorth/Documents/work/XGAP-ABUN/data/{srcname1}/eckert/{srcname1}/*")[0]

        # # io issues
        io_instance = IO(date, rannu_dir, srcname1, srcname2)

        fit_annu = FitAnnu(date, rannu_dir, srcname1, srcname2, 'reg5', nH, reds) 
        fit_annu.edit_run_xcm('sample_data_2T.xcm', '2T')

    