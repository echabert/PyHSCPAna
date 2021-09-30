

# Read a cfg file [filename]
# See instructions at the beginning of the file config/plots.cfg
# Return a string containing matplotlib instruction to create plots
# Assume that the data collection while have the name of the data_variable 
#
# To-do:
# - add x/y logscale
# - add title
# - add possibility to choose the range

def LoadPlots(filename):
    commands=""
    nvar=0
    with open(filename) as file:
        for line in file:
            #print(line)
            command=""
            if not line.startswith("#"):
                # create a dictionnary from the line
                l = line.split()
                d = {el[:-1]:l[l.index(el)+1]  for el in l if el.find(':')>0}
                #print(d)
                if not d or ('type' not in d) or (d['type'] not in ['1d','2d']): continue
                #print("there")
                if d['type']=='1d' and d.get('xvar',False):
                    command="{axis}.hist("+str(d.get('xvar'))
                    if d.get('xbins',False):
                        command+=",bins = "+str(d['xbins'])
                if d['type']=='2d' and d.get('xvar',False) and d.get('yvar',False):
                    command="{axis}.hist2d("+str(d['xvar'])+","+str(d['yvar'])
                    if d.get('xbins',False) and d.get('ybins',False):
                        command+=",bins = ("+str(d['xbins'])+','+str(d['ybins'])
                if d.get('label',False): command+=",label='"+str(d['label'])+"'"
                command+=")\n"
                commands+=command
                nvar+=1
    return commands,nvar


if __name__ == "__main__":
    from ConfigLoader import *
    import matplotlib.pyplot as plt 
    import numpy as np
    import math as m


    ###############################################
    # Test ConfigLoader with
    ###############################################

    commands,nvar = LoadPlots("config/plots.cfg")

    # Fixing random state for reproducibility
    np.random.seed(19680801)

    # Variables are Ih, p, eta, Ias
    # Ih follows a standard gamma distribution
    # p follows an expotential
    # eta follows a gaussian
    # Ias follows a gaussian
    npseudo = 10000
    Ih = np.random.default_rng().standard_gamma(5,npseudo)
    eta = np.random.default_rng().normal(0, 1, npseudo)
    p = np.random.default_rng().exponential(10, npseudo)
    Ias = np.random.default_rng().normal(0.2, 0.01, npseudo)

    nx=1
    ny=1
    nx=int(m.ceil(m.sqrt(nvar)))
    ny=int(m.ceil(nvar/nx))
    fig, ax = plt.subplots(nx,ny)

    counter=1
    ix=0
    iy=0
    for c in commands.split('\n'):
        print(c)
        tmp=""
        if ny>1:
            tmp="app = c.format(axis"+"='ax["+str(ix)+"]["+str(iy)+"]')"
        else:
            if nx==1 and ny==1:
                tmp="app = c.format(axis"+"='ax')"
            else:
                tmp="app = c.format(axis"+"='ax["+str(ix)+"]')"
        if iy<(ny-1): 
            iy+=1
        else:
            ix+=1
            iy=0
        #print(tmp)
        exec(tmp)
        exec(app)
        #exec(c)
    plt.show()
