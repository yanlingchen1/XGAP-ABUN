# ROSAT spectrum fix in spex

# Introduction
If fitting rosat spectrum in spex is needed,
correct the rosat.pi & rosat.rsp before use ogip2spex or trafo.

# Dependencies
pyspextools

# Steps
change the path to the path you want
run both reset_pi.ipynb and reset-res.ipynb
To test, run run_ogip2spex_rosat_test.sh 

# Note
reset_pi.ipynb: change POISSERR from F to T in [1] extension
reset_res.ipynb: add a tiny step to channels whose energies are the same
