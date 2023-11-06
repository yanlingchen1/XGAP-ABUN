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

        with open(f'{self.savepath}/bins/annu_{self.regname}_{mdl}_ab.xcm', 'w') as newf:
            newf.write(f'{lines}\n')

        with open(f'{self.pipeline_path}/sample_models/annu_allbkg/annu_{mdl}_ab_mdl.xcm') as f:
            lines = f.read()
        lines = lines.replace('PATH', self.subdir)
        with open(f'{self.savepath}/bins/annu_{self.regname}_{mdl}_ab_mdl.xcm', 'w') as newf:
            newf.write(f'{lines}\n')

#         # Begin fitting
#         os.chdir(self.savepath)
#         os.system(f'''
# xspec<<EOT
# @bins/annu_{self.regname}_{mdl}_ab.xcm
# ipl
# pl dat
# wenv annu_{self.regname}_{mdl}_ab
# exit
# exit
# EOT''')

#         os.system(f'''ps2pdf annu_{self.regname}_{mdl}_ab.ps
# rm annu_{self.regname}_{mdl}_ab.ps
# mv annu_{self.regname}_{mdl}_ab.pdf figs
# mv annu_{self.regname}_{mdl}_ab.pco dats
# mv annu_{self.regname}_{mdl}_ab.qdp dats 
# mv annu_{self.regname}_chain1000_{mdl}_ab.out logs''')
#         print(f'annu fitting for {self.regname} has finished!')



    