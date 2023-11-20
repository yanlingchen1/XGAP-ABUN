for f in *.rmf
do
# Insert "obj-" before "SDSS" and remove the extension
specname=$(basename "$f" | sed 's/-/-obj-/' | sed 's/\.[^.]*$//')
ftgrouppha infile=$specname.pi outfile=$specname-grp.pi respfile=$f grouptype=opt clobber=yes
done

for f in *.rmf
do
specname=$(basename "$f" | sed -E '/pn/ s/-/-obj-oot-/' | sed 's/\.[^.]*$//')
ftgrouppha infile=$specname.pi outfile=$specname-grp.pi respfile=$f grouptype=opt clobber=yes
done


