# ROSAT spectrum fix in spex

# Introduction
If fitting rosat spectrum in spex is needed,
correct the rosat.pi & rosat.rsp before use ogip2spex or trafo.

# Dependencies
pyspextools

# Steps
1. change the path to the path you want
2. run both reset_pi.ipynb and reset-res.ipynb
3. To test, run run_ogip2spex_rosat_test.sh 

# Note
reset_pi.ipynb: change POISSERR from F to T in [1] extension
reset_res.ipynb: add a tiny step to channels whose energies are the same
run_ogip2spex_rosat_test.sh: --keep-grouping flag is added 
for trafo: if it ask if you want to keep the grouping, say yes!

# Comments
The original ROSAT spectrum has been grouped substantially. They did it in a way that they made very large groups and only put the photons in the central bin, while keeping the others zero. Therefore, you need to accept the grouping in this case, because there is no sub-bin information. This will make the horizontal error bars in your plot also cover the whole bin width.
-- Jelle de Plaa 09/11/2023