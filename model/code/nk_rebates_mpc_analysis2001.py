#%%
import numpy as np
import pandas as pd
import pickle

# these are the sequence space packges
import utils
from simple_block import simple
import jacobian as jac
import nonlinear

# these are the model files
from nk_rebates_mpc_monthly_ss import nkrebate
from nk_rebates_mpc_model import investment, household_o, household_r, pricesetting, union, monetary, fiscal, marketclearing, durablesupply, twogoodsnondur

# ------------------------------------------------------------------------
# Spending profile of tax shock
# ------------------------------------------------------------------------

# rebate scaled as a fraction of PCE
taxshock = pd.read_stata('../input/rel_rebate2001.dta')['rel_rebate'].to_numpy()
Tmax = taxshock.shape[0]


ratelist = ['r','pi','rr','rk']
#%%
# ------------------------------------------------------------------------
# Variable Parameters
# ------------------------------------------------------------------------

mpctargets = [0.375, 0.66]
plotlist = ['micro-MPC = 0.375', 'micro-MPC = 0.66']

parasetnames = ['nondurablesonly2001'] # #'gefeedback',,'inelasticsupply','strongmp' #['inelasticdurables']#
parasets = [{'xc': 0}] 


parameter_set = ['gamma'] #, 'xi'
info_set = ['no-anticipation'] #['full-info'] # , 'no-anticipation'
# vars_to_plot = ['Personal consumption expenditures','Durable goods', 'Nondurable goods'] #'Motor vehicle parts and accessories (58)',

model_names = dict()
model_names['Real'] = ['c1']

# ------------------------------------------------------------------------
# Set-ups for solving the model
# ------------------------------------------------------------------------

T = {'micro': 60, 'GE': 200}

block_list = dict()
block_list['micro'] = [household_o, household_r, marketclearing, fiscal, twogoodsnondur] #
block_list['GE'] = [investment, household_o, union, pricesetting, monetary, fiscal, marketclearing, household_r, durablesupply, twogoodsnondur]

def getlists(block_list):
    allexogenous = set()
    allunknowns = set()
    targets = []
    for block in block_list:
        allexogenous = allexogenous | block.exogenous
        allunknowns = allunknowns | block.unknowns
        targets = targets + block.output_list

    exog = allexogenous - allunknowns
    unknowns = allunknowns - exog 
    unknowns = list( unknowns )
    exog = list( exog )

    return exog, unknowns, targets

exog=dict()
unknowns=dict()
targets=dict()

for key in T.keys():
    exog[key], unknowns[key], targets[key] = getlists(block_list[key])




# ------------------------------------------------------------------------
# Steady state parameters that match MPCs
# ------------------------------------------------------------------------


for parasetname, paraset in zip(parasetnames, parasets):
    print(paraset, parasetname)

    # find MPC
    mpc = dict()
    G = dict()
    output = dict()
    # , 'xi'
    for parameter in parameter_set:
        
        for mpctarget in mpctargets:
            print(parameter, mpctarget)
            mpclen = 3
            if mpctarget == 0.66:
                currmpc = 0.385 / 0.66 / 3
                lagmpc = (0.66 - 0.385) / 0.66 / 3
                mpclen = 6
                paraset = {**paraset, **{'lag1': currmpc, 'lag2': currmpc, 'lag3': lagmpc, 'lag4': lagmpc, 'lag5': lagmpc}}
            print(paraset)

            gamma = mpctarget

            maxit = 4000

            for kk in range(maxit):

                ss = nkrebate(gamma=gamma, **paraset) 
                
                G['micro'] = jac.get_G(block_list=block_list['micro'],
                                exogenous=exog['micro'],
                                unknowns=unknowns['micro'],
                                targets=targets['micro'],
                                T=T['micro'], ss=ss)

                diffmpc  = G['micro']['c1']['incshock'][0:mpclen,0].sum() - mpctarget

                                
                if parameter=='gamma':
                    gamma = gamma - 0.1 * diffmpc
                   

                diff = np.abs(diffmpc)


                if diff<10**-6:
                    break
                
                # print(diffmpc, diffelas, gamma, sigmad)
            assert kk<maxit-1, 'did not converge'
            
            print('Found parameters')
            print(gamma)
            G['GE'] = jac.get_G(block_list=block_list['GE'],
                                exogenous=exog['GE'],
                                unknowns=unknowns['GE'],
                                targets=targets['GE'],
                                T=T['GE'], ss=ss)
            
            print('Solved GE')            

            # calculating MPCs (combine with later?)
            GEdict = {}
            for key in T.keys():
                vardict = {}
                for var in model_names['Real']:
                    hdict = {}
                    for h in range(12):
                        hdict[str(h+1) + ' month'] = G[key][var]['tshock'][h,0].sum() / ss['exp']
                    vardict[var] = hdict
                    hdict['3 months cumulative'] = G[key][var]['tshock'][0:3,0].sum() / ss['exp']
                    hdict['12 months cumulative'] = G[key][var]['tshock'][0:12,0].sum()  / ss['exp']                           
                GEdict[key] = vardict

            print('Computed MPC')

            # calculating IRFs
            modelshock = dict()

            for info in info_set: # 
                modelshockGE = dict()

                for GEkey in G.keys():
                    modelshockvar = dict()

                    for variable in G['GE'].keys():
                        
                    
                        if variable not in G[GEkey].keys():
                            continue

                        if info in ['full-info']:
                            modelshockbase = G[GEkey][variable]['tshock'][0:Tmax,0:Tmax] @ taxshock 
                        elif info in ['no-anticipation']:
                            modelshockbase = G[GEkey][variable]['tshock'][0:Tmax,0] * taxshock[0]
                            for t in range(1,Tmax):
                                modelshockbase[t:] = modelshockbase[t:] + G[GEkey][variable]['tshock'][0:Tmax-t,0] * taxshock[t]

                        modelshockvar[variable] = modelshockbase
                    
                    modelshockGE[GEkey] = modelshockvar
                    
                modelshock[info] = modelshockGE

                

            for info in modelshock.keys():
                for GE in modelshock[info].keys():
                    for variable in modelshock[info][GE].keys():
                    
                        if variable not in ratelist:
                            if ss[variable]!=0:
                                modelshock[info][GE][variable] = modelshock[info][GE][variable] / ss[variable]
                            else:
                                modelshock[info][GE][variable] = modelshock[info][GE][variable] / ss['y']
                        elif variable in ratelist:
                            modelshock[info][GE][variable] = (1 + modelshock[info][GE][variable])**12  - 1            
            print('Computed IRFs')

            mpc['micro-MPC = ' + str(round(mpctarget,2))] = {'MPCs': GEdict,
                                    'value': ss[parameter],
                                    'parameter': parameter,
                                    'steady': ss,
                                    'G': G,
                                    'shock': modelshock} 

        output[parameter] = mpc

    # save output
    pickle.dump( output , open( '../output/' + parasetname + '.pkl', 'wb' ) )

# %%
