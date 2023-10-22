import os
from glob import glob
import pandas as pd
import re
import numpy as np
from astropy.io import fits

def sort_files(flist):
    pattern = r'_reg(\d+)'
    idxlst = []
    for file_name in flist:
        match = re.search(pattern, file_name)
        number = match.group(1)
        idxlst.append(int(number))
    return np.argsort(idxlst)

class IO:
    def __init__(self, date, rootdir, srcname1, srcname2, insts=['mos1S001', 'mos2S002', 'pnS003']):
        self.date = date
        self.rootdir = rootdir
        self.srcname1 = srcname1
        self.srcname2 = srcname2
        self.insts = insts
        self.savepath = self.make_output_dir()
        

    def make_output_dir(self):
        savepath = f'{self.rootdir}/fit_{self.date}'
        os.makedirs(savepath, exist_ok=True)
        os.makedirs(f'{savepath}/logs', exist_ok = True)
        os.makedirs(f'{savepath}/bins', exist_ok = True)
        os.makedirs(f'{savepath}/csvs', exist_ok = True)
        os.makedirs(f'{savepath}/figs', exist_ok = True)
        os.makedirs(f'{savepath}/dats', exist_ok = True)
        return savepath
    

    def check_files(self):
        '''
        Iterate among the subdir in main source dir 
        to check if all the files are available. 

        If not, an error and the subdir name will be reported.
        '''

        # get all the subdirectories in root dir
        subdir_lst = glob(f'{self.rootdir}/{self.srcname2}_*')

        # Initialize a list to store missing files
        missing_files = []
        f = open(f'{self.savepath}/logs/missing_files.log', 'w')

        for subdir in subdir_lst:
            regname = f'{subdir.split(".")[0].split("_")[-1]}'
            # define the files I want to check
            file_names = []
            for inst in self.insts:
                file_names.append(f'{subdir}/{inst}-{self.srcname2}_{regname}.rmf')
                file_names.append(f'{subdir}/{inst}-{self.srcname2}_{regname}.arf')
                file_names.append(f'{subdir}/{inst}-back-{self.srcname2}_{regname}.pi')
                file_names.append(f'{subdir}/{inst}-obj-{self.srcname2}_{regname}-grp.pi')
                file_names.append(f'{subdir}/{inst}-obj-{self.srcname2}_{regname}.pi')
                file_names.append(f'{subdir}/pnS003-obj-oot-{self.srcname2}_{regname}-grp.pi')
                file_names.append(f'{subdir}/pnS003-obj-oot-{self.srcname2}_{regname}.pi')
            

            print(file_names)
            for file_name in file_names:
                if not glob(file_name):
                    missing_files.append(f'{file_name}')
                    f.write(f'{file_name} \n')
        
        # Check for missing files
        if missing_files:
            raise ValueError(f"Files are missing. Check {subdir}missing_files.txt")

        else:
            print("All required files are present in the directory and its subdirectories.")

        f.close()


    def tidy_bkgpar(self):
        f = open(f'{self.savepath}/logs/bkg_bkg_freepar.log')
        input_text = f.read()
        f.close()
        # Initialize a list to store the extracted data
        data = []
        # Define a regular expression pattern to match parameter lines
        pattern = r'(\w+)\s+([-+]?\d*\.\d+(?:[Ee][-+]?\d+)?)\s+\+/-\s+([-+]?\d*\.\d+(?:[Ee][-+]?\d+)?)\s+'

        # Find and extract parameter lines
        matches = re.findall(pattern, input_text)

        names = ['lhb-n', 'gh-t', 'gh-n', 'cxb-n', 'icm-t', 'icm-n', 'spf-m1-n', 'spf-m2-n', 'spf-pn-n']
        # Organize extracted data into a list of dictionaries
        for i, match in enumerate(matches):
            value, error = match[1], match[2]
            data.append({"Name": names[i], f"value": value, f"error": error})

        # Create a Pandas DataFrame from the extracted data
        df = pd.DataFrame(data)

        # Save the DataFrame to a CSV file
        output_file = f"{self.savepath}/csvs/cxb_par.csv"
        df.to_csv(output_file, index=False)

        print(f"Data saved to {output_file}")

    

    def tidy_outputs(self):
        '''
        Get all the annuli logged parameter to a csv
        1. read mcmc err from *_chain1000_par.log
        2. read value from *freepar.log

        Output
        ----------
        {self.srcname2}_annuli_par.csv in csvs dir with columns
        'reg', 'T-value', 'T-errlo', 'T-errhi', 'T-status', 'Z-value', ..., 'n-value', ...
        
        status has two flags: 'u' or 'c', 
        'u' stands for unconstrained, 'c' stands for constrained.
        constrained means the min error is <=75% for the value & the value is reasonable
        '''

        reson_vrange = {'T':[0,5] , 'Z':[0,2] ,'n':[0,1e-2]}
        ## initialize the output dictionary
        keyslst = ['value', 'errlo', 'errhi']
        bigkeys = ['T', 'Z', 'n']
        output_dict = {}
        output_dict['reg'] = []
        for bigkey in bigkeys:
            for seckey in keyslst:
                output_dict[f'{bigkey}-{seckey}'] = []


        # read mcmc errors
        par_files = glob(f'{self.savepath}/logs/annu_reg*_chain1000_par.log')
        par_files = np.array(par_files)[sort_files(par_files)]
        for regnum, file in enumerate(par_files):
            output_dict[f'reg'].append(f'reg{regnum}')
            with open(file) as f:
                lines = f.readlines()[6:9]
                for i, line in enumerate(lines):
                    errlo = line.split('(')[-1].split(',')[0][1:]
                    errhi = line.split('(')[-1].split(',')[-1][:-2]
                    output_dict[f'{bigkeys[i]}-errlo'].append(float(errlo))
                    output_dict[f'{bigkeys[i]}-errhi'].append(float(errhi))

        # read value
        files = glob(f'{self.savepath}/logs/annu_reg*_freepar.log')
        files = np.array(files)[sort_files(files)]
        for file in files:
            with open(file) as f:
                lines = f.readlines()[11:14]
            for i, line in enumerate(lines):
                value = line.split('+/-')[0].split()[-1]
                output_dict[f'{bigkeys[i]}-value'].append(float(value))

        # # read in bkg ICM row
        # file = glob(f'{self.savepath}/logs/bkg_bkg_freepar.log')[0]
        # with open(file) as f:
        #     lines = f.readlines()[25:28]
        #     for i, line in enumerate(lines):
        #         value = line.split('+/-')[0].split()[-1]
        #         output_dict[f'{bigkeys[i]}-value'].append(float(value))

        print(output_dict)
        # Create a Pandas DataFrame from the extracted data
        df = pd.DataFrame(output_dict)
        print(df)
        # judge if the value is unconstrained
        for bigkey in bigkeys:
            errlo = np.array(df[f'{bigkey}-errlo'])
            errhi = np.array(df[f'{bigkey}-errhi'])
            value = np.array(df[f'{bigkey}-value'])

            cond1 = np.min([errlo, errhi], axis=0) > (0.75 * value)
            cond2 = (df[f'{bigkey}-value'] < reson_vrange[bigkey][1]) & (df[f'{bigkey}-value'] > reson_vrange[bigkey][0])
            print(cond2)
            status = np.where((cond1 | ~cond2), 'u', 'c')

            df[f'{bigkey}-status'] = status

        # Save the DataFrame to a CSV file
        output_file = f"{self.savepath}/csvs/{self.srcname2}_annuli_mypar.csv"
        df.to_csv(output_file, index=False)

        print(f"Annuli data saved to {output_file} !")

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

    def get_backscal(self):
        inst_dict = {}
        for name in self.insts:
            f = fits.open(f'{self.subdir}/{name}-back-{self.srcname2}_{self.regname}.pi')
            inst_dict[name] = np.round(f[1].header['BACKSCAL'] * (0.05/60) ** 2, 3)
        return inst_dict


if __name__ == '__main__':
    
    date = 231019

    # Some basic prefixes
    srcnum = '3460'
    srcname1 = f'ID{srcnum}'
    srcname2 = f'SDSSTG{srcnum}'

    root_dir = glob(f"/Users/eusracenorth/Documents/work/XGAP-ABUN/data/{srcname1}/eckert/{srcname1}/*")[0]

    # # io issues
    io_instance = IO(date, root_dir, srcname1, srcname2)

    io_instance.tidy_outputs()


