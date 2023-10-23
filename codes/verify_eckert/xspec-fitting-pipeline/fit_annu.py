from my_io import IO
import re
from astropy.io import fits
import numpy as np
import os
from glob import glob
import pandas as pd



class FitAnnu(IO):
    def __init__(self, date, rootdir, srcname1, srcname2, regname, nH, reds, insts = ['mos1S001', 'mos2S002', 'pnS003']):
        super().__init__(date, rootdir, srcname1, srcname2, insts)
        self.regname = regname
        self.subdir = f'{rootdir}/{srcname2}_{regname}'
        self.inst_dict = self.get_backscal()
        self.pipeline_path = '/Users/eusracenorth/Documents/work/XGAP-ABUN/codes/verify_eckert/xspec-fitting-pipeline'
        self.nH = nH
        self.reds = reds
    
    def update_inst_dict(self, new_regname):
        self.regname = new_regname
        self.subdir = f'{self.rootdir}/{self.srcname2}_{new_regname}'
        self.inst_dict = self.get_backscal()

    def get_backscal(self):
        inst_dict = {}
        for name in self.insts:
            f = fits.open(f'{self.subdir}/{name}-back-{self.srcname2}_{self.regname}.pi')
            inst_dict[name] = np.round(f[1].header['BACKSCAL'] * (0.05/60) ** 2, 3)
        return inst_dict

    def load_bkgpar(self):
        df = pd.read_csv(f'{self.savepath}/csvs/cxb_par.csv')
        def judge_spf(norm):
            # ! always set spf to 0 for now
            return 0
            # if float(norm) < 1e-6:
            #     return 0
            # else:
            #     return norm
        outdict = {}
        for i, name in enumerate(df['Name']):
            outdict[name] = df['value'][i]
        
        outdict['spf-m1-n'] = judge_spf(outdict['spf-m1-n'])
        outdict['spf-m2-n'] = judge_spf(outdict['spf-m2-n'])
        outdict['spf-pn-n'] = judge_spf(outdict['spf-pn-n'])
        return outdict
    

    def gen_text(self, appendix):
        self.bkg_dict = self.load_bkgpar()
        print(self.regname)

        FIT_TEXT = f'''xspec<<EOT
log >logs/annu_{self.regname}_fit_{appendix}.log
@bins/annu_{self.regname}_{appendix}.xcm

#### skybkg ####
# extract region area
new 1 {self.inst_dict['mos1S001']}
new 18 {self.inst_dict['mos2S002']}
new 35 {self.inst_dict['pnS003']}
new 7 {self.nH}
new oot:2 0.063

#### LHB ####
new 6 {self.bkg_dict['lhb-n']}
free 3,6
#### GH ####
new 8 {self.bkg_dict['gh-t']}
new 11 {self.bkg_dict['gh-n']}
free 8,11
#### cxb ####
new 17 {self.bkg_dict['cxb-n']}
free 16,17
#### spf ####
new spf:6 0
new spf:12 0
new spf:18 0
free spf:6,12,18
#### icm ####
new 12 1
new 15 1e-4
new 14 {self.reds}
free 14
thaw 12,13,15

### fit ###
fit 200 1e-2
setp energy
pl dat rat
ipl
pl dat
wenv annu_{self.regname}_{appendix}
exit
log none
save all bins/annu_{self.regname}_2nd_{appendix}.xcm
log >logs/annu_{self.regname}_allpar_{appendix}.log
sho par
log none
log >logs/annu_{self.regname}_freepar_{appendix}.log
sho fre
log none
chain length 1000
chain run annu_{self.regname}_chain1000_{appendix}.out
log >logs/annu_{self.regname}_chain1000_par_{appendix}.log
err 12,13,15
log none
cpd annu_{self.regname}_{appendix}.ps/ocps
setp rebin 3 30
pl lda ra
exit
EOT'''

        SAV_TEXT = f'''
ps2pdf annu_{self.regname}_{appendix}.ps
rm annu_{self.regname}_{appendix}.ps
mv annu_{self.regname}_{appendix}.pdf figs
mv annu_{self.regname}_{appendix}.pco dats
mv annu_{self.regname}_{appendix}.qdp dats 
mv annu_{self.regname}_chain1000_{appendix}.out logs
'''
        return FIT_TEXT, SAV_TEXT

    def replace_lines(origintext, replacetext, start_marker, end_marker):
        #### replace some lines ####
        start_pos = origintext.find(start_marker)
        end_pos = origintext.find(end_marker) + len(end_marker)
        # Create the updated string by replacing the block with the replacement rows
        updated_string = origintext[:start_pos] + replacetext + origintext[end_pos:]
        
        return updated_string

    def edit_run_xcm(self, xcmfile, appendix):
        # Alter the inputs in sample_*.xcm
        with open(f'{self.pipeline_path}/sample_models/{xcmfile}') as f:
            lines = f.readlines()
        newlines = [re.sub(r'SDSSTG828', self.srcname2, line) for line in lines]
        newlines = [re.sub(r'bkg', self.regname, line) for line in newlines]
        newlines = [re.sub(r'path', self.subdir, line) for line in newlines]
        newf = open(f'{self.savepath}/bins/annu_{self.regname}_{appendix}.xcm', 'w')
        for line in newlines:
            newf.write(f'{line}\n')
        
        #### oot ####
        value_data = []
        with open(f'{self.savepath}/logs/oot_{self.regname}_par.log', 'r') as file:
            lines = file.readlines()
        for line in lines:
            if line.startswith('# '):
                if re.search(r'\d', line): 
                    columns = line.split()
                    if 'frozen' in line:
                        value = columns[-2]
                    else:
                        value = columns[-3]
                    value_data.append(value)

        # Write the Value data
        for i, value in enumerate(value_data):
            newf.write(f'new oot:{int(i+1)} {value}\n' )
        newf.write(f'free oot:1-14\n')
        newf.close()

        

    def fit_1T(self):
        os.chdir(self.savepath)
        fit_text, sav_text = self.gen_text('')
        self.edit_run_xcm('sample_data.xcm', '')
        os.system(fit_text)
        os.system(sav_text)
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

    
    def fit_2T(self):
        os.chdir(self.savepath)
        fit_text, sav_text = self.gen_text('2T')
        self.edit_run_xcm('sample_data_2T.xcm', '2T')
        replace_text = f'''err 12,13,15,icm2:4,icm2:7'''
        newfit_text = re.sub(r'err\s+12,13,15', replace_text, fit_text)
        os.system(newfit_text)
        os.system(sav_text)
        print(f'annu fitting for {self.regname} has finished!')
    



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
        root_dir = glob(f"/Users/eusracenorth/Documents/work/XGAP-ABUN/data/{srcname1}/eckert/{srcname1}/*")[0]

        # # io issues
        io_instance = IO(date, root_dir, srcname1, srcname2)

        fit_annu = FitAnnu(date, root_dir, srcname1, srcname2, 'reg5', nH, reds) 
        fit_annu.edit_run_xcm('sample_data_2T.xcm', '2T')
        
