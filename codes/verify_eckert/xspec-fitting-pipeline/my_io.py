import os
from glob import glob
import pandas as pd
import re

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
        f = open(f'{self.rootdir}/logs/missing_files.log', 'w')

        for subdir in subdir_lst:
            os.chdir(f'{subdir}')

            # define the files I want to check
            file_names = []
            for inst in self.insts:
                file_names.append(f'{inst}-{self.srcname2}_{self.regname}.rmf')
                file_names.append(f'{inst}-{self.srcname2}_{self.regname}.arf')
                file_names.append(f'{inst}-back-{self.srcname2}_{self.regname}.pi')
                file_names.append(f'{inst}-obj-{self.srcname2}_{self.regname}-grp.pi')
                file_names.append(f'{inst}-obj-{self.srcname2}_{self.regname}.pi')
                file_names.append(f'pnS003-obj-oot-{self.srcname2}_{self.regname}-grp.pi')
                file_names.append(f'pnS003-obj-oot-{self.srcname2}_{self.regname}.pi')

            for file_name in file_names:
                if not glob(file_name):
                    missing_files.append(f'{subdir}/file_name')
                    f.write(f'{subdir}/file_name \n')
        
        # Check for missing files
        if missing_files:
            print("The following files are missing:")
            for missing_file in missing_files:
                print(missing_file)
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

        names = ['lhb-n', 'gh-t', 'gh-n', 'cxb-n', 'icm-t', 'icm-Z', 'icm-n', 'spf-m1-n', 'spf-m2-n', 'spf-pn-n']
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

    

    def tidy_outputs():
        '''
        1. Get the bkg logged parameter to a csv
        2. Get all the oot logged parameter to a csv
        3. Get all the qpb logged parameter to a csv
        4. Get all the annuli logged parameter to a csv
        
        '''
