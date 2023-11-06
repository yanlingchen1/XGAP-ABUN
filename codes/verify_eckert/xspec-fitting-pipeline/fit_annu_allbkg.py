from my_io import IO
from fit_frame import FitFrame
import re
from astropy.io import fits
import numpy as np
import os
from glob import glob
import pandas as pd

class FitAnnu_qpb(FitFrame):
    def fit_annu(self, mdl):
        # Alter the inputs in sample_annu.xcm
        with open(f'{self.pipeline_path}/sample_models/annu_qpb/annu_{mdl}.xcm') as f:
            lines = f.read()

        #### MDL #####
        lines = lines.replace('MDL', mdl)
        #### general ####
        lines = self.add_gen_par(lines)
        #### annu ####
        lines = self.add_annu_xcm(lines)
        #### backscal ####
        lines = self.add_backscal(lines)
        #### skybkg ####
        lines = self.add_gen_bkgpar(lines)

        with open(f'{self.savepath}/bins/annu_{self.regname}.xcm', 'w') as newf:
            newf.write(f'{lines}\n')

        # Begin fitting
        os.chdir(self.savepath)
        os.system(f'''
xspec<<EOT
@bins/annu_{self.regname}.xcm
EOT''')

        os.system(f'''ps2pdf annu_{self.regname}_{mdl}.ps
rm annu_{self.regname}_{mdl}.ps
mv annu_{self.regname}_{mdl}.pdf figs
mv annu_{self.regname}_{mdl}.pco dats
mv annu_{self.regname}_{mdl}.qdp dats 
mv annu_{self.regname}_chain1000_{mdl}.out logs''')
        print(f'annu fitting for {self.regname} has finished!')



    