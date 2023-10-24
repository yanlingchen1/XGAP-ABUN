# spex-fitting-pipeline
An automatic SPEX spectral fitting package. 
Aiming to fit all the annuli of the source automatically. 
Design for X-COP samples.

# Getting started

## Dependencies
conda activate spex
brew install ghostscript

## Input files structure
1. Subdir with names of '{src}_reg*' '{src}_bkg'
2. In every subdir, EPIC (incl. MOS & PN) spectrums and their rmf, arf, qpb, for pn, oot spec is required. 


## Output files
A new subdir named fit_result in every annuli subdir is created. The output files will be saved there
1. pn oot fit results. 'pn-oot-fit-results.csv'
2. qpb fit results. '{inst}-qpb-fit-results.csv'
'inst' will be 'mos1S001, mos2S002, pnS003'
3. bkg fit results. 'bkg-fit-results.csv'
4. data fit results. 'data-1stfit-results.csv'


## Steps
0. Check the files. 
1. Fit the pn oot spectrum. 
2. Fit the qpb spectrum.
3. Fit the bkg spectrum.
4. Fit the data spectrum.
    1) Determine the backscal of the spectrums. 
    2) use chain+err command for the parameters.
5. Sanity check of the data fit results. 
    1) If the abun fit has >75% uncertainties, freeze the abun to 0.3 and fit again. -> 'data-2ndfit-results.csv'
    

# Version History
- 0.1
    1. initial release
    2. For Soft proton we are fitting the norm with bkg region, which is not correct for now. It will be updated after the paper has been published. 

# License
This project is licensed under the MIT License





