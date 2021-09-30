import matplotlib.pyplot as plt 

# Read a cfg file [filename]
# See instructions at the beginning of the file config/plots.cfg
# Return a string containing matplotlib instruction to create plots
# Assume that the data collection fill find in a dictionnary: data[variable] 
#
# To-do:
# - add title
# - add possibility to choose the range

def LoadPlots(filename, alpha=0.5):
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
                    #command="{axis}.hist("+str(d.get('xvar'))
                    command="{axis}.hist(data['"+str(d.get('xvar'))+"']"
                    command+=",alpha="+str(alpha)
                    if eval(d.get('ylog','False')) : command+=",log=True"
                    if eval(d.get('norm','False')) : command+=",density=True"
                    if d.get('xbins',False):
                        command+=",bins = "+str(d['xbins'])
                if d['type']=='2d' and d.get('xvar',False) and d.get('yvar',False):
                    command="{axis}.hist2d("+str(d['xvar'])+","+str(d['yvar'])
                    if d.get('xbins',False) and d.get('ybins',False):
                        command+=",bins = ("+str(d['xbins'])+','+str(d['ybins'])
                command+=",label='{label}'"
                command+=")\n"
                commands+=command
                nvar+=1
    return commands,nvar


# Read a cfg file [filename]
# See instructions at the beginning of the file config/plots.cfg
# create subplots with the correct nx,ny size
# outputs are the fit, the axes and nx, ny

def createPlots(filename):
    commands,nvar = LoadPlots(filename)
    nx=1
    ny=1
    nx=int(m.ceil(m.sqrt(nvar)))
    ny=int(m.ceil(nvar/nx))
    fig, ax = plt.subplots(nx,ny)
    return fig, ax, nx, ny

def AddLegend(ax,nx,ny):
    for i in range(nx):
        for j in range(ny):
            ax[i][j].legend()

def FillPlots(filename,fig,ax,nx,ny,label='',**data):
    commands,nvar = LoadPlots("config/plots.cfg")
    counter=1
    ix=0
    iy=0
    for c in commands.split('\n'):
        print(c)
        tmp=""

        if ny>1:
            tmp="app = c.format(axis"+"='ax["+str(ix)+"]["+str(iy)+"]'"+",label='"+str(label)+"')"
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
        exec(tmp)
        print(tmp)
        print(locals()['app'])
        exec(locals()['app'])
    #plt.show()


if __name__ == "__main__":
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

    FillPlots("config/plots.cfg",fig,ax,nx,ny,label='A',Ih=Ih,eta=eta,p=p,Ias=Ias)
    Ih2 = np.random.default_rng().standard_gamma(6,npseudo)
    eta2 = np.random.default_rng().normal(0.5, 2, npseudo)
    p2 = np.random.default_rng().exponential(6, npseudo)
    Ias2 = np.random.default_rng().normal(0.3, 0.05, npseudo)
    FillPlots("config/plots.cfg",fig,ax,nx,ny,label='B',Ih=Ih2,eta=eta2,p=p2,Ias=Ias2)
    AddLegend(ax,nx,ny)
    plt.show()
    
    exit()
    counter=1
    ix=0
    iy=0
    for c in commands.split('\n'):
        #print(c)
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
        #print("here")
        #print("tmp=",tmp)
        exec(tmp)
        exec(app)
        #exec(c)
    plt.show()
