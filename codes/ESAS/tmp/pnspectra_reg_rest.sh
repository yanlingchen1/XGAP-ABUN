
source set_chips_on.txt
source set_sas.txt

export PN=pnS003
export ELO=700
export EHI=1200

for pat in 0 #4
do
for num in 0
do
for regfile in spec_reg/reg${num}-mos1S001.reg
do
regname=$(basename $regfile | cut -d'-' -f 1)
echo $PN
echo $regname

rm ${regname}/logs/pnspectra_${pat}_${PN}.log
rm ${regname}/logs/pnback_${pat}_${PN}.log

pnspectra eventfile=${PN}-allevc.fits ootevtfile=${PN}-allevcoot.fits keepinterfiles=yes withregion=yes regionfile=spec_reg/${regname}-${PN}.reg pattern=${pat} withsrcrem=yes maskdet=${PN}-bkgregtdet.fits masksky=${PN}-bkgregtsky.fits elow=${ELO} ehigh=${EHI} quads="${PNON}" badpixelresolution=1 -V=7 2>&1 | tee  ${regname}/logs/pnspectra_${pat}_${PN}.log
pnback inspecfile=${PN}-fovt.pi inspecoot=${PN}-fovtoot.pi elow=${ELO} ehigh=${EHI} quads="${PNON}" 2>&1 | tee ${regname}/logs/pnback_${pat}_${PN}.log 


done
done
done
