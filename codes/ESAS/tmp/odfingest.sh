
    export SAS_CCF=/Users/eusracenorth/Documents/work/XGAP-ABUN/alldata/XGAP/SDSSTG3460/ccf.cif
    export SAS_ODF=/Users/eusracenorth/Documents/work/XGAP-ABUN/alldata/XGAP/SDSSTG3460
    odfingest odfdir=$SAS_ODF outdir=$SAS_ODF 2>&1 | tee odfingest.log
    