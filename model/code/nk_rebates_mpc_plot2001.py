#%%
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
from cycler import cycler
from tables import mpctable

plt.rc('font', size=16) #controls default text size

# ------------------------------------------------------------------------
# Tables and Figure Settings
# ------------------------------------------------------------------------

parasetnames = ['nondurablesonly2001'] # 'gefeedback',,'inelasticsupply','strongmp' #['inelasticdurables']#
parasettitles = ['Baseline Model']

# parasetnames = ['baseline','durableprice']
# parasettitles = ['Baseline Model','Model with Less Elastic Durable Supply']



plot_names = ['JPS Nondurables'] #,

table_dict = {'JPS Nondurables': 'c1'}
vars_to_plot = {'JPS Nondurables'}

model_names = dict()
model_names['Real'] = ['c1']

Tmax = 15
modeldates = pd.date_range(start='2001-05-01', freq='MS', periods=Tmax)

# graph defaults
plt.rc('font', size=12)
new_prop_cycle = (cycler('color', ['k','tab:blue','tab:purple','tab:green','r']) + 
                  cycler('linestyle', ['-','dashdot',(5, (10, 3)),(0, (3, 1, 1, 1)),'--']))                         
plt.rc('axes', prop_cycle=new_prop_cycle)

# ------------------------------------------------------------------------
# Data for counterfactual
# ------------------------------------------------------------------------

dfreal = pd.read_parquet('../input/jpsexpenditurereal.parquet')
dfnom = pd.read_parquet('../input/jpsexpenditure.parquet')


dforg = {}
for df, defl in zip([dfreal, dfnom],['Real', 'Nominal']):
    dforg[defl] = df.rename(columns={'DataValue': 'JPS Nondurables'})

# forecast
dffc = pd.read_stata('../input/forecasts2001.dta').rename(columns={'mdate': 'TimePeriod'}).set_index('TimePeriod')
dffc = dffc.rename(columns={'rcndur_jpscatforB': 'Pessimistic Forecast', 'rcndur_jpscatforD': 'Contemporary Forecast'})
dffcset = {'Real': dffc['Pessimistic Forecast']}

# normalize to 2008 m5 nominal spending
for var in dforg['Real'].columns:
    dforg['Real'][var] = dforg['Real'][var] / dforg['Real'].loc['2001-05-01',var] * dforg['Nominal'].loc['2001-05-01',var]
#%%
# add names (manual)
episodes = {'Date': ['Jan-Apr 2020', 'Sep-Nov 2008', 'Apr-Jul 1960', 'Jan-Apr 1980'],
            'Episode': ['COVID lockdowns', 'Lehman Collapse', 'Prior Spike Up', 'Credit controls, Volcker']}
dates = pd.to_datetime(['2020-04-01','2008-11-01','1960-07-01','1980-06-01'])
dfnames = pd.DataFrame(data = episodes, index=dates)

dfdecline = dict()
for var, cutoff in zip(['JPS Nondurables'],[-1.3]):

    # 3-month growth rates
    pcegrowth = dfreal.pct_change(periods = 3) * 100

    # largest 3-month declines
    largestdeclines = pcegrowth[pcegrowth<=cutoff].dropna()

    # strip out adjecent dates
    dates = largestdeclines.index
    maxdeclines = []
    for date in dates:
        # find adjecent dates
        currdates = dates[abs(dates - date).days < 300]

        # find the largest decline
        currdecline = pcegrowth.loc[currdates.date].idxmin()[0]
        
        if currdecline not in maxdeclines:
            maxdeclines.append(currdecline)

    # table of max declines
    dfdeclinetemp = np.round(-pcegrowth.loc[maxdeclines].sort_values(by='DataValue', ascending=True).rename(columns={'DataValue': 'Decline'}),1)

    dfdeclinetemp = dfdeclinetemp.merge(dfnames, how='left', left_index=True, right_index=True)

    dfdecline[var] = dfdeclinetemp[['Date', 'Episode', 'Decline']]

print(dfdecline)

# ------------------------------------------------------------------------
# Tables and Figures
# ------------------------------------------------------------------------


for parasetname, parasettitle in zip(parasetnames, parasettitles):

    output = pickle.load( open( '../output/' + parasetname + '.pkl', 'rb' ) )
    parameter_set = output.keys()

    for parameter in parameter_set:

        mpcset = output[parameter].keys()
        info_set = output[parameter][list(mpcset)[0]]['shock'].keys()
        GEset = output[parameter][list(mpcset)[0]]['MPCs'].keys()

        # calculate MPCs:
        for info in info_set:
            for GE in GEset:
                for mpcval in mpcset:
                    if mpcval == 'micro-MPC = 0.01':
                        continue
                    for var in table_dict.values():
                        deltac = output[parameter][mpcval]['shock'][info][GE][var].sum() * output[parameter][mpcval]['steady'][var]
                        deltat = -output[parameter][mpcval]['shock'][info][GE]['t'].sum() * output[parameter][mpcval]['steady']['t']
                        output[parameter][mpcval]['MPCs'][GE][var]['12 months cumulative'] = deltac / deltat

        savetitle = 'mpcs' + parameter + parasetname
        mpctable(output[parameter], table_dict, list(mpcset)[:-1], parasettitle, savetitle)
        
   

    # create figures
    for parameter in parameter_set:
        for info in info_set:
            for GE in GEset:
                for defl in model_names.keys():
                    for varname, model_name, var in zip(plot_names, model_names[defl], vars_to_plot):

                        df = dforg[defl][var].copy().rename('Data').to_frame()

                        for mpcval in mpcset:
                            # if var=='Relative Durable Price' and parasetname=='durableprice':
                            #     stop
                            
                            dfmodel = pd.DataFrame.from_dict(output[parameter][mpcval]['shock'][info][GE][model_name])
                            dfmodel.columns = [mpcval]
                            dfmodel = dfmodel.rename(index=dict(zip(range(Tmax), modeldates)))
                            df = df.merge(dfmodel, how='left', left_index=True, right_index=True)
                            
                            df[mpcval] = df['Data'] * ( 1 - df[mpcval] )

                        dfplot = df.loc['2001-03-01':'2002-05-01', :]


                        if varname=='JPS Nondurables':
                            dfplotset = [dfplot, dfplot.merge(dffcset[defl], how='left', left_index=True, right_index=True)]
                        else:
                            dfplotset = [dfplot]

                        if GE=='GE':
                            dftab =  np.round(- (df.loc['2001-09-01', list(mpcset)] / df.loc['2001-06-01', list(mpcset)] - 1) * 100 , 1)

                            dftab = dftab.to_frame(name='Decline').reset_index().rename(columns={'index': 'Episode'})
                            dftab['Date'] = ''
                            
                            dfexp = pd.concat([dfdecline[var], dftab], axis=0, ignore_index=True).sort_values(by=['Decline'], ascending=False)
                            
                            dfexp.to_latex('../output/' + defl + '_' + varname + '_drop_' + GE + '_' + parasetname + '.tex', index=False)

                            mpc911 = list(mpcset)
                            mpc911.remove('micro-MPC = 0.01')
                            arrays = [
                                ['Forecast of 9/11 Effect', 'Forecast of 9/11 Effect', 'Forecast of 9/11 Effect'] + ['Macro Counterfactual'] * len(list(mpc911)),
                                ['Our Pessimistic Forecast', 'September Greenbook', 'Barsky-Sims (2012)'] + list(mpc911),
                                ]

                            # Create the MultiIndex
                            multi_index = pd.MultiIndex.from_arrays(arrays, names=('Scenario', 'Specification'))

                            df911 = pd.DataFrame(index = multi_index, columns = ['September 2001 Impact', 'Through December 2001'])

                            
                            for mpc in mpc911:
                                df911.loc[pd.IndexSlice[:,mpc],'September 2001 Impact'] = df.loc['2001-09-01', mpc] - df.loc['2001-09-01','Data']
                                df911.loc[pd.IndexSlice[:,mpc], ['Through December 2001']] = (df.loc['2001-05-01':'2001-12-01', mpc] - df.loc['2001-05-01':'2001-12-01','Data']).sum()

                            # Forecast
                            with open('../input/pessimistic_diff911.txt', 'r') as file:
                                content = file.read().strip()
                                df911.loc[pd.IndexSlice[:,'Our Pessimistic Forecast'], 'September 2001 Impact'] = float(content)
                            with open('../input/pessimistic_sum911.txt', 'r') as file:
                                content = file.read().strip()
                                df911.loc[pd.IndexSlice[:,'Our Pessimistic Forecast'], 'Through December 2001'] = float(content)
                            # df911.loc[pd.IndexSlice[:,'Our Pessimistic Forecast'], 'September 2001 Impact'] = 1.165478 
                            # df911.loc[pd.IndexSlice[:,'Our Pessimistic Forecast'], 'September 2001 Impact'] = 3.055495 

                            # Greenbook
                            df911.loc[pd.IndexSlice[:,'September Greenbook'],:] = df.loc['2001Q2','Data'].sum() * -0.0025 

                            # Barsky Sims
                            # 15 is the E5Y drop in September, by December normalized
                            # Their shock raises E5Y by 7.5 and C by 0.0015% in the first quarter (Fig 2)
                            df911.loc[pd.IndexSlice[:,'Barsky-Sims (2012)'],'September 2001 Impact'] = df.loc['2001-09-01','Data'].sum() * -15 / 7.5 * 0.0015
                            df911.loc[pd.IndexSlice[:,'Barsky-Sims (2012)'],'Through December 2001'] = df.loc['2001-09-01':'2001-11-01','Data'].sum() * -15 / 7.5 * 0.0015

                            # round to one digit and format
                            df911 = -df911
                            df911 = df911.apply(pd.to_numeric, errors='coerce').round(1)
                            df911 = df911.applymap(lambda x: f"\${x}bn" if pd.notnull(x) else "")

                            # now convert to string and add '$' at the beginning and 'bn' at end

                            df911.to_latex('../output/' + defl + '_' + varname.replace(' ','') + '_911_' + GE + '_' + parasetname + '.tex',
                                          caption = 'Estimated 9/11 Impact on JPS Nondurables vs Our Counterfactuals')
                            
                            
                            
                        # full plot
                        for dfplot, fc in zip(dfplotset, ['','fc']):
                            dfplotc = dfplot.copy()
                            # for dfpl, colors, psmj in zip((dfplotc, dfplotc.drop([list(mpcset)[0]], axis=1), dfplotc.drop(list(mpcset)[1:], axis=1)),(new_prop_cycle,new_prop_cycle_psmj,new_prop_cycle_orw),('','PSMJ','ORW')):
                            # for dfpl, colors, psmj in zip(dfplotc,new_prop_cycle,''):
                            dfpl = dfplotc
                            colors = new_prop_cycle
                            psmj = ''
                            fig, ax = plt.subplots()
                            # plt.rc('font', size=12) #controls default text size
                            ax.set_prop_cycle(colors)
                            # ax.set_color_cycle(['k','tab:blue','tab:orange','tab:green'])
                            # plt.plot(dfpl, linewidth=3)
                            for col in dfpl.columns:
                                if col=='Data':
                                    order = 2.5
                                else:
                                    order = 2
                                if col == 'micro-MPC = 0.01':
                                    lowmpc, = plt.plot(dfpl[col], linewidth=2, zorder=order)
                                else: 
                                    plt.plot(dfpl[col], linewidth=2, zorder=order)
                            plt.xlim(datetime.datetime(2001,3,1), datetime.datetime(2002,5,1))
                            # ax.xaxis.set_major_locator(mdates.MonthLocator())
                            ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
                            plt.xlabel('March 2001 - May 2002')
                            # plt.xticks(rotation=45)
                            plt.ylim(305,318)
                            plt.ylabel('Billion $')
                            # plt.title(defl + ' ' + varname)
                            plt.legend(list(dfpl.columns), loc='upper left')
                            plt.tight_layout(pad=0)
                            # plt.savefig('../output/mpc' + parameter + defl + varname.replace(' ','') + GE + info + parasetname + '.eps')

                            plt.savefig('../output/' + defl + '_' + varname.replace(' ','') + fc + '_' + GE + '_' + parasetname + psmj + '_appendix.eps')
                            
                            # make low mpc invisible for standard graphs
                            lowmpc.set_visible(False)
                            # labels = list(dfpl.columns)
                            # labels.remove('micro-MPC = 0.01')
                            
                            handles_labels = [(line, label) for line, label in zip(ax.get_lines(), list(dfpl.columns))
                                            if line.get_visible() and line.get_label() != '_nolegend_']

                            if handles_labels:
                                handles, labels = zip(*handles_labels)
                                ax.legend(handles, labels)
                            else:
                                ax.legend([])
                            


                            plt.savefig('../output/' + defl + '_' + varname.replace(' ','') + fc + '_' + GE + '_' + parasetname + psmj + '.eps')

                            

                            # plt.title(defl + ' ' + varname)
                            ax.legend_ = None
                            # plt.savefig('../output/mpc' + parameter + defl + varname.replace(' ','') + GE + info + parasetname + '.eps')
                            plt.savefig('../output/' + defl + '_' + varname.replace(' ','') + fc + '_' + GE + '_' + parasetname + psmj + '_nolegend.eps')
                            plt.close()
                        
 
                        
                # save all variables to excel:
                for mpcval in output[parameter].keys():
                    dfirf = pd.DataFrame.from_dict(output[parameter][mpcval]['shock'][info][GE])
                    dfirf = dfirf.rename(index=dict(zip(range(Tmax), modeldates)))


                    dfirf.to_excel('../output/irfs' + parameter + 'mpc' + mpcval[-2:] + GE + info + parasetname + '.xlsx')
                    
                
                    



# ------------------------------------------------------------------------
# Output parameters
# ------------------------------------------------------------------------

        ss = output[parameter][list(mpcset)[0]]['steady']

        tablenames = {
            'beta': ['$\\beta$', 'Subjective discount factor'],
            'sigma': ['$\\sigma$', 'Utility curvature on consumption'],
            'share1': ['$s_1$', 'Share of JPS Nondurable Consumption in Total Consumption'],
            'eta': ['$\\eta$', 'Durable operating cost'],
            'nu': ['$\\nu$', 'Weight on disutility of labor'],
            'phi': ['$\\phi$', 'Inverse of the Frisch elasticity of labor supply'],
            'gamma': ['$\\gamma$', 'Fraction of Hand-to-Mouth consumers'],
            'alpha': ['$\\alpha$', 'Exponent on private capital in production function'],
            'delta': ['$\\delta$', 'Depreciation of private capital'],
            'kappa': ['$\\kappa$', 'Investment adjustment cost parameter'],
            'delta1': ['$\\delta_1$', 'Parameter on linear term of capital utilization cost'],
            'delta2': ['$\\delta_2$', 'Parameter on quadratic term of capital utilization cost'],
            'mup_ss': ['$\\mu_p$', 'Steady-state price markup'],
            'muw_ss': [ '$\\mu_W$', 'Steady-state wage markup'],
            'theta': ['$\\theta_p$', 'Calvo parameter on price adjustment'],
            'thetaw': ['$\\theta_W$','Calvo parameter on wage adjustment'],
            'eps': ['$\\iota$', 'Elasticity of Substitution Across Consumption Varieties'],
            'epsw': ['$\\epsilon_W$', 'Elasticity of substitution between types of labor'],
            'gyfrac': ['$gy$', 'Steady-state share of total govt spending to GDP'],
            'phib': ['$\\phi_b$', 'Debt feedback coefficient in fiscal rule'],
            'rhor': ['$\\rho_{r}$', 'Monetary policy interest rate smoothing'],
            'phipi': ['$\\phi_{\\pi}$', 'Monetary policy response to inflation'],
            'phigap': ['$\\phi_{gap}$', 'Monetary policy response to the output gap'],
        }
        tabletitles = ['Parameter', 'Value', 'Description']
        tableformat = ['l','S[table-format=2.3]','l']

        # create smaller version
        presentation = ['sigma','share1','phi','gamma','phib']
        tablenames_presentation = dict()
        for para in presentation:
            tablenames_presentation[para] = tablenames[para]

        # nondurable version
        nondur = ['beta','sigma','share1','nu','phi','gamma','alpha','kappa','delta1','delta2','mup_ss','muw_ss','theta','thetaw','eps','epsw','gyfrac','phib','rhor','phipi','phigap']
        tablenames_nondur = dict()
        for para in nondur:
            tablenames_nondur[para] = tablenames[para]

        for table, tablesave in zip([tablenames, tablenames_presentation, tablenames_nondur],['calibration','calibration_small','calibration_nondur']):
            f = open('../output/' + tablesave + parasetname + parameter + '.tex', 'w')
            f.write('\\begin{table}[htbp]\n')
            if tablesave!='calibration_small':
                f.write('\\caption{Baseline Calibration of the Model}\n') 
            f.write('\\begin{tabular}{' + ''.join(tableformat) + '}\\toprule\n') 
            for i, title in enumerate(tabletitles):
                if tableformat[i][0]=='S':
                    title = '\\multicolumn{1}{l}{' + title + '}'
                if 1+i<len(tabletitles):
                    f.write(title + ' & ')
                else:
                    f.write(title + ' \\\\ \\midrule \n')
            for param, text in table.items():
                if ss[param]==0:
                    continue
                if param in ['gamma','thetad', 'mpx']:
                    f.write(text[0] + ' & \\text{varies}')
                else:
                    f.write(text[0] + ' & ' + str(round(ss[param], 3)) )
                for col in text[1:]:
                    f.write(' & ' + col)
                f.write('\\\\ \n')
            f.write('\\bottomrule\\end{tabular}\n') 
            f.write('\\begin{minipage}{\hsize} \\rule{0pt}{9pt} \\footnotesize \n')
            if 'gamma' in table.keys():
                f.write('The model is calibrated at a monthly frequency. The parameter $\\gamma$ is calibrated to either 0.375, or 0.66, which corresponds to the 3-month and 6-month non-durable MPCs respectively. See the text for details. ')
            f.write('\\end{minipage}\n')
            f.write('\\label{tab:' + tablesave + '}\n')    
            f.write('\\end{table}\n')    
            f.close()

# %%
