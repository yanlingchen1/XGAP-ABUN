"""
This class load all_bkg(skybkg+spf+qpb) as a user defined atable model
Which is the right way, and it is the same as spex.

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
        self.bkg_dict = self.load_bkgpar()
        # Alter the inputs in sample_annu.xcm
        with open(f'{self.pipeline_path}/sample_models/annu_allbkg/annu_{mdl}_ab.xcm') as f:
            lines = f.read()

        #### MDL #####
        lines = lines.replace('MDL', mdl)
        #### general ####
        lines = self.add_gen_par(lines)
        #### oot ####
        lines = self.add_oot_xcm(lines)
        #### backscal ####
        lines = self.add_backscal(lines)

        with open(f'{self.savepath}/bins/annu_{self.regname}_{mdl}.xcm', 'w') as newf:
            newf.write(f'{lines}\n')

        with open(f'{self.pipeline_path}/sample_models/annu_allbkg/annu_{mdl}_ab_mdl.xcm') as f:
            lines = f.read()
        lines = self.add_gen_par(lines)
        with open(f'{self.savepath}/bins/annu_{self.regname}_{mdl}_mdl.xcm', 'w') as newf:
            newf.write(f'{lines}\n')

        # Begin fitting
        os.chdir(self.savepath)
        os.system(f'''
xspec<<EOT
@bins/annu_{self.regname}_{mdl}.xcm
ipl
pl dat
wenv annu_{self.regname}_{mdl}
exit
exit
EOT''')

        os.system(f'''ps2pdf annu_{self.regname}_{mdl}.ps
pdftk annu_{self.regname}_{mdl}.pdf cat 2 output 1.pdf
mv 1.pdf annu_{self.regname}_{mdl}.pdf
rm annu_{self.regname}_{mdl}.ps
mv annu_{self.regname}_{mdl}.pdf figs
mv annu_{self.regname}_{mdl}.pco dats
mv annu_{self.regname}_{mdl}.qdp dats 
mv annu_{self.regname}_{mdl}_chain1000.out logs''')
        print(f'annu fitting for {self.regname} has finished!')



    