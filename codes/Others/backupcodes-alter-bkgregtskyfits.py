# for *bkgregt*.fits

os.chdir(datapath)

CDELT = 6.94E-04 * 3600 # arcsec per pixel

for name in ['mos1S001', 'mos2S002', 'pnS003']:

    os.system(f'cp ori1-bkgregtsky.fits {name}-bkgregtsky.fits')
    datf = open(f'sources_mos2S002_xy_srcreg.reg')
    lines = datf.readlines()[1:]
    datf.close()
    print(lines)
    orif = fits.open(f'{name}-bkgregtsky.fits', mode='update')
    dat = orif[1].data

    # initialize
    arr = [[[]] * 6] * len(lines)
    for i in range(len(lines)):
        line = lines[i]
        # SHAPE, X, Y, R, ROTANG, COMPONENT
        arr[i][0] = f"!{line.split('(')[0].upper()}"
        arr[i][1] = [float(line.split('(')[-1].split(',')[0]), 0,0,0]
        arr[i][2] = [float(line.split(',')[1]),0,0,0]
        arr[i][3] = [float(line.split(',')[2][:-1]) * CDELT, float(line.split(',')[3][:-1]) * CDELT,0,0]
        arr[i][4] = [float(line.split(',')[-1].split(')')[0]),0,0,0]
        arr[i][5] = 1
    
    dat = arr
    print(dat)
    orif.flush()
