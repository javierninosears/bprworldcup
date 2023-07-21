#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# SETUP CODE #
import pandas as pd
import numpy as np
import pymannkendall as mk
import math
import statsmodels.api as sm
import matplotlib.pyplot as plt



df_raw = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vSlb_NZnb8vDjXwHPsSf47Yh1poBera1Gqpm-i6m1Z1mTZo5Nxbx-yaWSjrizd29IHgzUxyZ3AGlIAg/pub?gid=0&single=true&output=csv")
hrv_data = pd.read_csv("https://tinyurl.com/civ-libs-vdem-owid")
hrp_data = pd.read_csv("https://tinyurl.com/phys-integr-libs-vdem-owid")
pf_data = pd.read_csv("https://tinyurl.com/freedom-of-the-press")
foe_data = pd.read_csv("https://tinyurl.com/freeexpr-vdem-owid-2")
foa_data = pd.read_csv("https://tinyurl.com/freeassoc-vdem-owid")
time_data = pd.read_csv("https://tinyurl.com/time-graph")

def str_to_list(inp):
    return [inp]

score_list = []

# CREATE HRV_SCORE #
for i in range(len(df_raw)):
    hrv_country = pd.DataFrame()
    hrp_country = pd.DataFrame()
    pf_country = pd.DataFrame()
    foe_country = pd.DataFrame()
    foa_country = pd.DataFrame()
    val = 0
    if "/" in df_raw['Country'][i]:
        df_raw['Country'][i] = df_raw['Country'][i].split("/")
    else:
        df_raw['Country'][i] = str_to_list(df_raw['Country'][i])
    val = 0
    new_list = df_raw['Country'][i]
    for k in range(len(new_list)):
        hrv_country = hrv_country.append(hrv_data[(hrv_data['Entity'] == new_list[k])])
        hrp_country = hrp_country.append(hrp_data[(hrp_data['Entity'] == new_list[k])])
        pf_country = pf_country.append(pf_data[(pf_data['Entity'] == new_list[k])])
        foe_country = foe_country.append(foe_data[(foe_data['Entity'] == new_list[k])])
        foa_country = foa_country.append(foa_data[(foa_data['Entity'] == new_list[k])])  
    hrv_country = hrv_country.reset_index()
    hrp_country = hrp_country.reset_index()
    pf_country = pf_country.reset_index()
    foe_country = foe_country.reset_index()
    foa_country = foa_country.reset_index()
    if (df_raw['Comp. Year'][i] == df_raw['Hosting Year'][i]):
        for j in range(len(hrv_country)):
            if hrv_country['Year'][j] == df_raw['Comp. Year'][i]:
                val += 2*(hrv_country['civ_libs_vdem_owid'][j])
            elif hrv_country['Year'][j] == (df_raw['Comp. Year'][i] - 3):
                val -= 2*(hrv_country['civ_libs_vdem_owid'][j])
        for j in range(len(hrp_country)):
            if hrp_country['Year'][j] == df_raw['Comp. Year'][i]:
                val += hrp_country['phys_integr_libs_vdem_owid'][j]
            elif hrp_country['Year'][j] == (df_raw['Comp. Year'][i] - 3):
                val -= hrp_country['phys_integr_libs_vdem_owid'][j]
        for j in range(len(pf_country)):
            if pf_country['Year'][j] == df_raw['Comp. Year'][i]:
                val += pf_country['fp_scaled'][j]
            elif pf_country['Year'][j] == (df_raw['Comp. Year'][i] - 3):
                val -= pf_country['fp_scaled'][j]
        for j in range(len(foe_country)):
            if foe_country['Year'][j] == df_raw['Comp. Year'][i]:
                val += foe_country['freeexpr_vdem_owid'][j]
            elif foe_country['Year'][j] == (df_raw['Comp. Year'][i] - 3):
                val -= foe_country['freeexpr_vdem_owid'][j]
        for j in range(len(foa_country)):
            if foa_country['Year'][j] == df_raw['Comp. Year'][i]:
                val += foa_country['freeassoc_vdem_owid'][j]
            elif foa_country['Year'][j] == (df_raw['Comp. Year'][i] - 3):
                val -= foa_country['freeassoc_vdem_owid'][j]
        score_list.append(val / len(df_raw['Country'][i]))
    else:
        for j in range(len(hrv_country)):
            if hrv_country['Year'][j] == df_raw['Comp. Year'][i]:
                val += 2*(hrv_country['civ_libs_vdem_owid'][j])
            elif hrv_country['Year'][j] == (df_raw['Hosting Year'][i]):
                val -= 2*(hrv_country['civ_libs_vdem_owid'][j])
        for j in range(len(hrp_country)):
            if hrp_country['Year'][j] == df_raw['Comp. Year'][i]:
                val += hrp_country['phys_integr_libs_vdem_owid'][j]
            elif hrp_country['Year'][j] == (df_raw['Hosting Year'][i]):
                val -= hrp_country['phys_integr_libs_vdem_owid'][j]
        for j in range(len(pf_country)):
            if pf_country['Year'][j] == df_raw['Comp. Year'][i]:
                val += pf_country['fp_scaled'][j]
            elif pf_country['Year'][j] == (df_raw['Hosting Year'][i]):
                val -= pf_country['fp_scaled'][j]
        for j in range(len(foe_country)):
            if foe_country['Year'][j] == df_raw['Comp. Year'][i]:
                val += foe_country['freeexpr_vdem_owid'][j]
            elif foe_country['Year'][j] == (df_raw['Hosting Year'][i]):
                val -= foe_country['freeexpr_vdem_owid'][j]
        for j in range(len(foa_country)):
            if foa_country['Year'][j] == df_raw['Comp. Year'][i]:
                val += foa_country['freeassoc_vdem_owid'][j]
            elif foa_country['Year'][j] == (df_raw['Hosting Year'][i]):
                val -= foa_country['freeassoc_vdem_owid'][j]
        score_list.append(val / len(df_raw['Country'][i]))
                
df_raw["HRV Score"] = score_list



# df_raw now contains the HRV Score for each competition in the dataset

# CODE TO CREATE TIME-SERIES DATA

for r in range(len(time_data)):
    if pd.isnull(time_data['Comp. Year'][r]):
        time_data.drop(r, axis=0, inplace=True)

value_list = time_data['Avg HRV Score']
century_value_list = value_list[21:]
twentieth_century_vl = value_list[:21]


#Code to run Mann-Kendall Test on the time-series data of human rights violation scores over time
#mk.original_test(value_list)


