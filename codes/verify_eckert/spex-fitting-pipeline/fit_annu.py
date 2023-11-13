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
        # Alter the inputs in sample_annu.com
        with open(f'{self.pipeline_path}/sample_models/annu/fit_annu_{mdl}.com') as f:
            lines = f.read()
        
        lines = lines.replace('MDL', mdl)
        #### general ####
        lines = self.add_gen_par(lines)
        #### oot ####
        lines = self.add_oot_com(lines)
        #### backscal ####
        lines = self.add_backscal(lines)

        with open(f'{self.savepath}/bins/annu-{self.regname}-{mdl}.com', 'w') as newf:
            newf.write(lines)

        # Begin fitting
        os.chdir(self.savepath)
#         os.system(f'''
# rm logs/annu-{self.regname}* 
# rm dats/annu-{self.regname}* 
# rm figs/annu-{self.regname}* 
# source /Users/eusracenorth/miniconda3/envs/spex/opt/spex/spex-activate.sh    
# spex<<EOT
# log exe bins/annu-{self.regname}-{mdl}
# quit
# EOT''')
#         os.system(f'''
# ps2pdf annu-{self.regname}-{mdl}.ps
# mv annu-{self.regname}-{mdl}.pdf figs/annu-{self.regname}-{mdl}.pdf
# rm annu-{self.regname}-{mdl}.ps
# ''')
#         print(f'annu fitting for {self.regname} has finished!')