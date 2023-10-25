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
        self.pippath = '/Users/eusracenorth/Documents/work/XGAP-ABUN/codes/verify_eckert/spex-fitting-pipeline'
        
    def make_output_dir(self):
        savepath = f'{self.rootdir}/fit_spex_{self.date}'
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
                file_names.append(f'{inst}-{self.srcname2}_{regname}.rmf')
                file_names.append(f'{inst}-{self.srcname2}_{regname}.arf')
                file_names.append(f'{inst}-back-{self.srcname2}_{regname}.pi')
                file_names.append(f'{inst}-obj-{self.srcname2}_{regname}-grp.pi')
                file_names.append(f'{inst}-obj-{self.srcname2}_{regname}.pi')
                file_names.append(f'{subdir}/pnS003-obj-oot-{self.srcname2}_{regname}-grp.pi')
                file_names.append(f'{subdir}/pnS003-obj-oot-{self.srcname2}_{regname}.pi')
            
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

    def tidy_dict2df(self, output_dict, appendix, bigkeys = ['T', 'Z', 'n']):

        """
        input output_dict
        return df
        
        """
        # add col to output_dict
        output_dict['reg'] = []
        output_dict['rhi'] = []
        output_dict['rlo'] = []

        # read mcmc errors
        par_files = glob(f'{self.savepath}/logs/annu_reg*_chain1000_par{appendix}.log')
        par_files = np.array(par_files)[sort_files(par_files)]
        for regnum, file in enumerate(par_files):
            output_dict[f'reg'].append(f'reg{regnum}')
            # read the annuli from eckert regionfile
            regpath = f'{self.savepath}/../regions'
            with open(f'{regpath}/{self.srcname2}_reg{regnum}.reg') as f:
                line = f.readlines()[-1]
                output_dict[f'rhi'].append(line.split(',')[-1][:-3])

            with open(file) as f:
                lines = f.readlines()
            for i in range(len(bigkeys)):
                if len(lines)> 20:
                    errlo = 999
                    errhi = 999
                else:
                    start_idx = next((index for index, line in enumerate(lines) if '(90%)' in line), None)
                    errlo = lines[int(start_idx+1+i)].split('(')[-1].split(',')[0]
                    errhi = lines[int(start_idx+1+i)].split('(')[-1].split(',')[-1][:-2]

                output_dict[f'{bigkeys[i]}-errlo'].append(abs(float(errlo)))
                output_dict[f'{bigkeys[i]}-errhi'].append(float(errhi))

        # read value
        files = glob(f'{self.savepath}/logs/annu_reg*_freepar{appendix}.log')
        files = np.array(files)[sort_files(files)]
        for file in files:
            with open(file) as f:
                text = f.read()
            pattern = r'([+-]?[\d]*\.?[\d]+(?:[eE][-+]?\d+)?)\s+\+/-'
            values = re.findall(pattern, text)
            for i in range(len(bigkeys)):
                output_dict[f'{bigkeys[i]}-value'].append(float(values[i]))

        # # read in bkg ICM row
        # file = glob(f'{self.savepath}/logs/bkg_bkg_freepar.log')[0]
        # with open(file) as f:
        #     lines = f.readlines()[25:28]
        #     for i, line in enumerate(lines):
        #         value = line.split('+/-')[0].split()[-1]
        #         output_dict[f'{bigkeys[i]}-value'].append(float(value))

        # define rlo column
        output_dict['rlo'] = np.insert(np.array(output_dict['rhi'][:-1]), 0, 0)
        # Create a Pandas DataFrame from the extracted data
        df = pd.DataFrame(output_dict)

        return df

    def tidy_outputs(self, appendix, bigkeys = ['T', 'Z', 'n'], reson_vrange = {'T':[0,5] , 'Z':[0,2] ,'n':[0,1e-2]}):
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
        
        ## initialize the output dictionary
        keyslst = ['value', 'errlo', 'errhi']
        output_dict = {}
        
        for bigkey in bigkeys:
            for seckey in keyslst:
                output_dict[f'{bigkey}-{seckey}'] = []
        
        # tidy para to a dataframe
        df = self.tidy_dict2df(output_dict, appendix, bigkeys = bigkeys)

        # judge if the value is unconstrained, 
        # add the status columns to df
        for bigkey in bigkeys:
            errlo = np.array(df[f'{bigkey}-errlo'])
            errhi = np.array(df[f'{bigkey}-errhi'])
            value = np.array(df[f'{bigkey}-value'])

            cond1 = np.min([errlo, errhi], axis=0) > (0.5 * value)
            cond2 = (df[f'{bigkey}-value'] < reson_vrange[bigkey][1]) & (df[f'{bigkey}-value'] > reson_vrange[bigkey][0])
            status = np.where((cond1 | ~cond2), 'u', 'c')

            df[f'{bigkey}-status'] = status

        # Save the final DataFrame to a CSV file
        output_file = f"{self.savepath}/csvs/{self.srcname2}_annuli_mypar{appendix}.csv"
        df.to_csv(output_file, index=False)
        
        print(f"Annuli data saved to {output_file} !")
    
    def tidy_outputs_2nd(self, appendix, appendix2, bigkeys = ['T', 'n']):
        '''
        Read the csv of previous parameter
        if Z is unconstrained, load the refit par file 
        and save all the para to new csv.

        appendix refer to ICM model, 
        appendix2 refer to 2nd refit when fix Z
        '''
        
        # load the 1st para csv
        df = pd.read_csv(f'{self.savepath}/csvs/{self.srcname2}_annuli_mypar{appendix}.csv')
        for regname in df['reg'][df['Z-status'] == 'u']:
            regnum = int(regname.split('g')[-1])

            # read mcmc errors
            file = f'{self.savepath}/logs/annu_{regname}_chain1000_par{appendix}_{appendix2}.log'
            with open(file) as f:
                lines = f.readlines()
                start_idx = next((index for index, line in enumerate(lines) if '(90%)' in line), None)
                lines = lines[int(start_idx+1):int(start_idx+1+len(bigkeys))]
                for i, line in enumerate(lines):
                    errlo = line.split('(')[-1].split(',')[0][1:]
                    errhi = line.split('(')[-1].split(',')[-1][:-2]
                    df[f'{bigkeys[i]}-errlo'][regnum] = errlo
                    df[f'{bigkeys[i]}-errhi'][regnum] = errhi
                df[f'Z-errlo'][regnum] = 0.0
                df[f'Z-errhi'][regnum] = 0.0


            # read value
            file = f'{self.savepath}/logs/annu_{regname}_freepar{appendix}_{appendix2}.log'
            with open(file) as f:
                text = f.read()
            pattern = r'([+-]?[\d]*\.?[\d]+(?:[eE][-+]?\d+)?)\s+\+/-'
            values = re.findall(pattern, text)
            for i in range(len(bigkeys)):
                df[f'{bigkeys[i]}-value'][regnum] = values[i]
            df[f'Z-value'][regnum] = 0.3

        # Save the DataFrame to a CSV file
        output_file = f"{self.savepath}/csvs/{self.srcname2}_annuli_mypar{appendix}_{appendix2}.csv"
        df.to_csv(output_file, index=False)

        print(f"Annuli data saved to {output_file} !")



    def get_keyvalue(self, key):
        inst_dict = {}
        for name in self.insts:
            f = fits.open(f'{self.subdir}/{name}-back-{self.srcname2}_{self.regname}.pi')
            inst_dict[name] = np.round(f[1].header[key] * (0.05/60) ** 2, 3)
        return inst_dict
    
    def edit_header(self, fits_file, ext, key, newvalue):
        """
        Edit a keyword in the FITS header of a given file.

        Parameters:
        fits_file (str): The path to the FITS file.
        ext (int): The fits extension
        key (str): The keyword to edit.
        newvalue: The new value to set for the keyword.
        """
        # Open the FITS file for editing
        hdulist = fits.open(fits_file, mode='update')
        # Get the header (primary header in this example)
        header = hdulist[ext].header
        # Check if the key exists in the header
        if key in header:
            # Update the value for the specified key
            header[key] = newvalue
            print(f"Updated header keyword '{key}' to '{newvalue}'.")
        else:
            print(f"Header keyword '{key}' not found.")
        # Save the changes
        hdulist.flush()
        hdulist.close()

    def edit_hduclas3(self):
        # get all the subdirectories in root dir
        subdir_lst = glob(f'{self.rootdir}/{self.srcname2}_*')
        # print(subdir_lst)
        for subdir in subdir_lst:
            regname = f'{subdir.split(".")[0].split("_")[-1]}'
            for inst in self.insts:
                self.edit_header(f'{inst}-obj-{self.srcname2}_{regname}.pi',1, 'HDUCLAS3', 'COUNTS')
            for inst in ['mos1S001', 'mos2S002']:
                self.edit_header(f'{inst}-back-{self.srcname2}_{regname}.pi',1, 'HDUCLAS3', 'COUNTS')
            
            self.edit_header(f'{subdir}/pnS003-back-{self.srcname2}_{regname}.pi',1, 'HDUCLAS3', 'RATE')
            self.edit_header(f'{subdir}/pnS003-obj-oot-{self.srcname2}_{regname}.pi',1, 'HDUCLAS3', 'COUNTS')
    
    def xspec2spex(self):
        """
        trafo works for mos
        ogip2spex works for pn in pipeline
        
        """
        # get all the subdirectories in root dir
        subdir_lst = glob(f'{self.rootdir}/{self.srcname2}_*')
        # print(subdir_lst)
        for subdir in subdir_lst:
            regname = f'{subdir.split(".")[0].split("_")[-1]}'
            for inst in self.insts:
                if 'mos' in inst:
                    with open(f'{self.pippath}/sample_models/trafo_mos.sh') as f:
                        text = f.read()
                else:
                    with open(f'{self.pippath}/sample_models/trafo_pn.sh') as f:
                        text = f.read()
                    with open(f'{self.pippath}/sample_models/ogip2spex.sh') as f:
                        text2 = f.read()
                    
                replace_dict = {
'PHAFILE':f'{subdir}/{inst}-obj-{self.srcname2}_{regname}.pi',
'BKGFILE':f'{subdir}/{inst}-back-{self.srcname2}_{regname}.pi',
'RMFFILE':f'{subdir}/{inst}-{self.srcname2}_{regname}.rmf',
'ARFFILE':f'{subdir}/{inst}-{self.srcname2}_{regname}.arf',
'SPOFILE':f'{subdir}/{inst}-{self.srcname2}_{regname}',
'../mos1-diag':f'{subdir}/../{inst.split("S")[0]}-diag'
}
                def replace_text(text, oldv, newv):
                    return text.replace(oldv, newv)
                for key, value in replace_dict.items():
                    text = replace_text(text, key, value)
                with open(f'{subdir}/trafo_{inst}.sh', 'w') as f:
                    f.write(text)
            ### for pn oot ###
            replace_dict['PHAFILE'] = f'pnS003-obj-oot-{self.srcname2}_{regname}.pi'
            replace_dict['SPOFILE'] = f'pnS003-pn-oot-{self.srcname2}_{regname}.pi'
            for key, value in replace_dict.items():
                text2 = replace_text(text2, key, value)
            with open(f'{subdir}/trafo_pnS003-oot.sh', 'w') as f:
                f.write(text2)
            os.makedirs(f'{subdir}/spex_single', exist_ok=True)
            os.system(f'mv {subdir}/*.spo {subdir}/spex_single')
            os.system(f'mv {subdir}/*.res {subdir}/spex_single')
        with open(f'{self.rootdir}/run_all_trafo.sh', 'w') as f:
            f.write(f'''for f in */trafo_*.sh
do
sh $f
done''')
        
        print(f'cd {self.rootdir}\n sh run_all_trafo.sh')
                    


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


