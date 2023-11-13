"""
Steps:
1. load the data and both src and diag rmf
2. load the smoothed qpb model or the modelled qpb model
3. load the skybkg model
4. atable skybkg and qpb model
5. write rate and rate err to *allbkg* files

"""
import numpy as np
import os
from fit_frame import FitFrame
from glob import glob
from astropy.io import fits
import pandas as pd

class AtableBKG(FitFrame):
    def bkgsmooth(self):
        for inst in self.inst_dict.keys():
            if 'pn' in inst:
                sellim = (90, 3000)
            elif 'mos' in inst:
                sellim = (65, 2300)
            else:
                raise ValueError('Wrong inst name!')
            if os.path.isfile(f'{self.subdir}/{inst}-back-smoothed_savgol-140-5.pi'):
                continue
            else:
                os.system(f'''
bkgsmooth<<EOT
read {self.subdir}/{inst}-back-{self.srcname2}_{self.regname}.pi
select {sellim[0]} {sellim[1]}
savgol 140 5
write {self.subdir}/{inst}-back-smoothed_savgol-140-5.pi
quit
EOT
''')
    def plot_smoothbkg(self):
        pass

    def gen_qpbmdltxt(self):
        for inst in self.inst_dict.keys():
            filename = f'{self.subdir}/{inst}-back-smoothed_savgol-140-5.pi'
            rmfname = f'{self.subdir}/{inst}-{self.srcname2}_{self.regname}.rmf'
            output_dict = {}
            # read the rate from smoothed qpb pi
            with fits.open(rmfname) as f:
                output_dict['elo'] = f[2].data['E_MIN']
                output_dict['ehi'] = f[2].data['E_MAX']
            # read the rate from smoothed qpb pi, 
            with fits.open(filename) as f:
                output_dict['rate'] = f[1].data['RATE']
            df = pd.DataFrame(output_dict)
            df.to_csv(f'{self.subdir}/{inst}-back-smoothed_savgol-140-5.txt', index = False, header = None, sep = ' ')
            os.system(f'ftflx2tab infile={self.subdir}/{inst}-back-smoothed_savgol-140-5.txt modelname={inst.split("S")[0]}_qpb outfile={self.subdir}/{inst}-back-smoothed_savgol-140-5.mdl nspec=1 additive=yes redshift=no xunit=keV clobber=yes')

    def atable_allbkg(self):
        self.bkg_dict = self.load_bkgpar()
        mod_spl = '\n' * 20
        for inst in self.inst_dict.keys():
            os.system(f'''
xspec<<EOT
data {self.subdir}/{inst}-back-{self.srcname2}_{self.regname}.pi
none	
res 1:1 {self.subdir}/{inst}-{self.srcname2}_{self.regname}.rmf
arf 1:1 {self.subdir}/{inst}-{self.srcname2}_{self.regname}.arf
res 2:1 {self.subdir}/../{inst.split("S")[0]}-diag.rsp
mo const*const*(apec+tbabs*(apec+pow))
{mod_spl}
mo 2:spf_qpb const*const*(pow)+atable{{{self.subdir}/{inst}-back-smoothed_savgol-140-5.mdl}}
{mod_spl}
## set inst const
new 1 {self.inst_dict[inst]}
new spf_qpb:1=1
new spf_qpb:2=2
new 3 0.11
new 6 {self.bkg_dict["lhb-n"]}
new 7 {self.nH}
new 8 {self.bkg_dict["gh-t"]}
new 11 {self.bkg_dict["gh-n"]}
new 12 1.46
new 13 {self.bkg_dict["cxb-n"]}
new spf_qpb:3 0.7
new spf_qpb:4 0
new spf_qpb:5 1
save all {self.savepath}/bins/atable_{inst}_{self.regname}.xcm
ipl
wenv atable_{inst}_{self.regname}
pl data
quit
# save plot
setp rebin 10 30
setp energy
ign **-0.5
ign 10.-**
cpd atable_{inst}_{self.regname}.ps/ocps
pl ldat
quit
EOT
ps2pdf atable_{inst}_{self.regname}.ps
pdftk atable_{inst}_{self.regname}.pdf cat 2 output 1.pdf
mv 1.pdf atable_{inst}_{self.regname}.pdf
rm atable_{inst}_{self.regname}.ps
mv atable_{inst}_{self.regname}.pdf {self.savepath}/figs
mv atable_{inst}_{self.regname}.qdp {self.savepath}/dats
mv atable_{inst}_{self.regname}.pco {self.savepath}/dats
''')

    def qdp2ogip(self):
        """
        CAUTION:
        Now the errors of the *allbkg*pi have been forced to 1e-20
        
        """
        bkg_instdict = {'mos1S001': 93.632, 'mos2S002': 127.285, 'pnS003': 118.604}
        for inst in self.inst_dict.keys():
            output_file = f'{self.subdir}/{inst}-allbkg-{self.srcname2}_{self.regname}.pi'
            qpb_file = f'{self.subdir}/{inst}-back-{self.srcname2}_{self.regname}.pi'
            os.system(f'cp {qpb_file} {output_file}')
            mdl_file = f'{self.savepath}/dats/atable_{inst}_{self.regname}.qdp'
            mdl_df = pd.read_csv(mdl_file, skiprows=3, header=None, delim_whitespace=True)

            #### calculate the poisson error ####
            with fits.open(qpb_file) as f:
                srcheader = f[1].header
            with fits.open(output_file, mode = 'update') as f:
                ctr = mdl_df.iloc[:, 4]
                columns = [
                    fits.Column(name='CHANNEL', format='J', array=mdl_df.iloc[:, 0]),
                    fits.Column(name='RATE', format='E', array=ctr),
                    fits.Column(name='STAT_ERR', format='E', array=np.ones(len(ctr))*1e-20)
                ]
                new_bintable = fits.BinTableHDU.from_columns(columns)
                f[1] = new_bintable
                f[1].header = srcheader
                f[1].header['HDUCLAS3'] = 'RATE'
                f[1].header['TUNIT2'] = 'counts/s'
                f[1].header['TUNIT3'] = 'counts/s'
                f[1].header['POISSERR'] = 'T'
                f.flush()  

    #### check the sum bkg file in xspec in every subdir ####
    def qdp2txt(self):
        self.bkg_dict = self.load_bkgpar()
        output_dict = {}
        # read the elo ehi from bkg txt file
        bkgpath = f'{self.rootdir}/{self.srcname2}_bkg'
        for inst in self.insts:
            df_e = pd.read_csv(f'{bkgpath}/{inst}-back-smoothed_savgol-140-5.txt', header = None, delim_whitespace=True)
            output_dict['elo'] = df_e.iloc[:,0]
            output_dict['ehi'] = df_e.iloc[:,1]
            # read the rate from qpb file
            qpbfile = f'{self.savepath}/dats/atable_{inst}_{self.regname}.qdp'
            df_r = pd.read_csv(qpbfile, skiprows=3, header=None, delim_whitespace=True)
            output_dict['rate'] = df_r.iloc[:,4]
            df = pd.DataFrame(output_dict)
            df.to_csv(f'{self.savepath}/dats/atable_{inst}_{self.regname}.txt', index = False, header = None, sep = ' ')
            os.system(f'ftflx2tab infile={self.savepath}/dats/atable_{inst}_{self.regname}.txt modelname={inst.split("S")[0]}_ab outfile={self.subdir}/atable_{inst}_{self.regname}.mdl nspec=1 additive=yes redshift=no xunit=keV clobber=yes')

