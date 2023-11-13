# Intro
For now, we use xspec then use spex to fit spectra.
We smooth and add all the bkg component (skybkg, qpb, spf) in bkg region
and scale this to different regions using xspec. 
Then read this as bkg in spex. 

1. spf
currently, spf norm in spex or xspec are all set to 0
2. bkg modelling
fit skybkg, qpb in xspec
define the model here
use this model to do atable in xspec
in spex, load total bkg with trafo.
in xspec, only load qpb model. 

# Dependence
1. pyspextools 0.3.4 by Jelle de Plaa

# Steps
All steps except model skybkg are in main.py
Please change the file structures according to your own data.

1. Smooth the qpb in bkg region using 'bkgsmooth' in pyspextools

2. Model the skybkg in bkg region
fit_other.fit_bkg() in xspec-fitting-pipeline can be used
Or a file named cxb_par.csv can be created. 
See cxb_par.csv in sample_files/

3. add the smoothed qpb and the skybkg model as final bkg 

4. calculate the rate and rate stat_err and save for the final bkg
final file -> {subdir}/{inst}-allbkg-{srcname2}_bkg.pi

5. In spex, read it in trafo
see spex_fitting_pipeline/trafo/trafo_epic_loadallbkg.sh

-------------- divert steps -----------------
6. In xspec, read the {subdir}/{inst}-back-smoothed_savgol-140-5.mdl as qpb model, don't use backgrnd command. 

