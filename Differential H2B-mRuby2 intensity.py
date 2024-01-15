# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 22:25:37 2023

@author: Timofei Lebedev
"""

import pandas as pd
import numpy as np
import scipy
import statsmodels.stats.multitest

df= pd.read_csv('Combined H2B 24h intensities.csv')
fields= df.groupby(['Cell', 'Full_name', 'Metadata_Conc', 'Metadata_Rep', 'Metadata_Field']).mean()['MeanIntNorm']
fields= fields.reset_index()
cells=[]
drugs=[]
concs=[]
ps=[]
diffs=[]
for cell in set(fields['Cell']):
    for drug in set(fields[fields['Cell']==cell]['Full_name']):
        for conc in set(fields[(fields['Cell']==cell) & (fields['Full_name']==drug)]['Metadata_Conc']):
            if conc != 0:
                diff= fields[(fields['Cell']==cell) & (fields['Full_name']==drug) & (fields['Metadata_Conc']==conc)]['MeanIntNorm'].mean() - fields[(fields['Cell']==cell) & (fields['Full_name']==drug) & (fields['Metadata_Conc']==0)]['MeanIntNorm'].mean()
                s,p= scipy.stats.mannwhitneyu(fields[(fields['Cell']==cell) & (fields['Full_name']==drug) &(fields['Metadata_Conc']==conc)]['MeanIntNorm'], fields[(fields['Cell']==cell) & (fields['Full_name']==drug) & (fields['Metadata_Conc']==0)]['MeanIntNorm'])
                cells.append(cell)
                drugs.append(drug)
                concs.append(conc)
                ps.append(p)
                diffs.append(diff)
p_adj= statsmodels.stats.multitest.multipletests(ps, alpha=0.05, method='fdr_bh')
df_diff= pd.DataFrame(data= {'Cell': cells, 'Drug': drugs, 'Conc': concs, 'p-val': ps, 'diff': diffs, 'p-adj': p_adj[1]})
df_diff['valid']= np.where((df_diff['p-adj']<0.001) & (df_diff['diff']>0.5), 'true', 'false')
df_diff['q']= df_diff['p-adj'].apply(lambda x: -np.log10(x))
df_diff.to_excel('H2B diff.xlsx')