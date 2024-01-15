# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 15:45:01 2023

@author: cance
"""

import pandas as pd
import scipy


{'PRISM': 'PRISM Repurposing Public 23Q2',
 'CTD2': 'Drug sensitivity AUC (CTD^2)',
 'GDSC2': 'Drug sensitivity AUC (Sanger GDSC2)',
 'GDSC1': 'Drug sensitivity AUC (Sanger GDSC1)'}

df= pd.read_csv('depmap_export_2023-11-16 19_53_47.652962_subsetted.csv')
df.set_index('Unnamed: 0', inplace=True)
df_prism= pd.DataFrame(index= df.index)
df_ctd2= pd.DataFrame(index= df.index)
df_gdsc2= pd.DataFrame(index= df.index)
df_gdsc1= pd.DataFrame(index= df.index)
for col in df.columns:
    if 'PRISM Repurposing Public 23Q2' in col:
        df_prism= pd.concat([df_prism, df[col]], axis=1)
        df_prism.rename(columns={col: col.split(' ')[4].lower()}, inplace=True)
    if 'Drug sensitivity AUC (CTD^2)' in col:
        df_ctd2= pd.concat([df_ctd2, df[col]], axis=1)
        df_ctd2.rename(columns={col: col.split(' ')[4].lower()}, inplace=True)
    if 'Drug sensitivity AUC (Sanger GDSC2)' in col:
        df_gdsc2= pd.concat([df_gdsc2, df[col]], axis=1)
        df_gdsc2.rename(columns={col: col.split(' ')[5].lower()}, inplace=True)
    if 'Drug sensitivity AUC (Sanger GDSC1)' in col:
        df_gdsc1= pd.concat([df_gdsc1, df[col]], axis=1)
        df_gdsc1.rename(columns={col: col.split(' ')[5].lower()}, inplace=True)
gdsc1_cols= set(df_gdsc1.columns)-set(df_gdsc2.columns)
df_gdsc= pd.concat([df_gdsc2, df_gdsc1[gdsc1_cols]], axis=1)
drugs= set(df_gdsc.columns) & set(df_ctd2.columns) & set(df_prism.columns)
r1_list=[]
p1_list=[]
r2_list=[]
p2_list=[]
r3_list=[]
p3_list=[]
n_cells=[]
n_pg=[]
n_pc=[]
n_gc=[]
for drug in list(drugs):
    cells= set(df_prism[drug].dropna().index) & set(df_gdsc[drug].dropna().index)
    r, p= scipy.stats.spearmanr(df_prism.loc[cells][drug], df_gdsc.loc[cells][drug], nan_policy='omit', alternative='two-sided')
    r1_list.append(r)
    p1_list.append(p)
    n_pg.append(len(cells))
    cells= set(df_prism[drug].dropna().index) & set(df_ctd2[drug].dropna().index)
    r, p= scipy.stats.spearmanr(df_prism.loc[cells][drug], df_ctd2.loc[cells][drug], nan_policy='omit', alternative='two-sided')
    r2_list.append(r)
    p2_list.append(p)
    n_pc.append(len(cells))
    cells= set(df_gdsc[drug].dropna().index) & set(df_ctd2[drug].dropna().index)
    r, p= scipy.stats.spearmanr(df_gdsc.loc[cells][drug], df_ctd2.loc[cells][drug], nan_policy='omit', alternative='two-sided')
    r3_list.append(r)
    p3_list.append(p)
    n_gc.append(len(cells))
df_r= pd.DataFrame(index= list(drugs), data={'PRISM vs GDSC': r1_list, 'PRISM vs CTD2': r2_list, 'GDSC vs CTD2': r3_list})
df_p= pd.DataFrame(index= list(drugs), data={'PRISM vs GDSC': p1_list, 'PRISM vs CTD2': p2_list, 'GDSC vs CTD2': p3_list})   
drugs= [x.upper() for x in list(df_r.index)]
df_r.index= drugs
drugs= [x.upper() for x in list(df_p.index)]
df_p.index= drugs
df_true= df_r*(df_p < 0.05)
df_r.to_excel('DepMap AUC correlations R.xlsx')
df_p.to_excel('DepMap AUC correlations pval.xlsx')
df_true.to_excel('DepMap AUC correlations R with true pvals.xlsx')

