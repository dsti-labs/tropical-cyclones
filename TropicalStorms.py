# -*- coding: utf-8 -*-

## Prediction of tropical storm intensity

# Import packages
import os
import pandas as pd
import numpy as np

# Change current working directory
# current directory:
print(os.getcwd())
# set new directory
os.chdir('D:\_DSTI\A24_Python_Machine_learning\Project3_Tropical_storms')

# Dataset loading
df = pd.read_csv('.\ibtracs.csv', header=0) 
df = df.iloc[1:] # remove 2nd line (with index 1).
df = df.reset_index() #reset indexes ;
# Add a column "Index" corresponding to the previous indexes. Can be removed.
#storms.head()
#print(storms)
# storms: dataframe 297098 lines, 175 columns (174 + 1 for old indexes)

# List of columns
columns_headers=list(df.columns)
print(columns_headers)

# PROBLEM: empty cells are in fact filled with whitespace
df.isna().sum() # it seems that there is no NA, which is false.
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x) # remove whitespace from every cells
df.replace('', np.nan, inplace=True) # replace empty cells with NaN
df_NA = df.isna().sum() # it seems to work. 
# We can remove all columns filled only with NA

# convert data types : 
cols = df.filter(like="_WIND").columns
df[cols] = df[cols].apply(pd.to_numeric, errors="coerce")
df.dtypes

# COLUMNS TO REMOVE:
    # ------------------
    # index: column added by Python when updating indexes after removing the 2nd line.
    # NAME: same as SID except that some storms don't have name. Redundant info
    # NUMBER: number of the storm for the year. Restart at 1 each year. Not useful.
    # REUNION_R64_NE
    # REUNION_R64_SE
    # REUNION_R64_SW
    # REUNION_R64_NW
    # REUNION_GUST
    # TD9636_PRES
    # TD9635_WIND
    # TD9635_PRES
    # TD9635_ROCI
    # MLC_CLASS
    # MLC_WIND
    # MLC_PRES ----- All this previous columns are only empty cells
    # ALL _LAT: all latitude are more or less the same as in column LAT. Redundant info.
    # ALL _LON: all longitude are more or less the same as in column LON. Redundant info.
    # BASIN 
    # SUBBASIN: These two will probably be correlated to LAT and LON. Redundant info.
    # WMO_WIND: all data from agencies but differents units but no adjustement is made for differences in wind speed averaging. Data not comparable.
    # TD9636_WIND: in data description: "subjective, must be interpreted with caution". Not reliable.
    
STORMS = df.drop(columns=['index', 'NAME', 'NUMBER',
                                    'REUNION_R64_NE', 'REUNION_R64_SE', 'REUNION_R64_SW', 'REUNION_R64_NW', 
                                    'REUNION_GUST', 'TD9636_PRES', 'TD9635_WIND', 'TD9635_PRES', 'TD9635_ROCI', 'MLC_CLASS', 'MLC_WIND', "MLC_PRES",
                                    'BASIN', 'SUBBASIN',
                                    'WMO_WIND', 'TD9636_WIND',
                                    ])

col_to_drop = STORMS.columns[STORMS.columns.str.contains('_LAT')] # all columns containing "_LAT"
STORMS.drop(col_to_drop, axis=1, inplace=True) # remove all columns with _LAT
col_to_drop = STORMS.columns[STORMS.columns.str.contains('_LON')] # all columns containing "_LON"
STORMS.drop(col_to_drop, axis=1, inplace=True) # remove all columns with _LON

# parameters common to all agencies:
    # WIND, PRESS

# Create one column with WIND (and one with AGENCY_WIND):
sources_adj = [
    ("USA_WIND", 1.0),  # No adjustment
    ("DS824_WIND", 1.0),  # No adjustment
    ("NEUMANN_WIND", 1.0),  # No adjustment
    ("TOKYO_WIND", 1.12),  # Adjustment factor
    ("HKO_WIND", 1.12),
    ("KMA_WIND", 1.12),
    ("REUNION_WIND", 1.12),
    ("BOM_WIND", 1.12),
    ("NADI_WIND", 1.12),
    ("WELLINGTON_WIND", 1.12)
]

# Create the two columns "WIND" and "AGENCY":
STORMS["WIND"] = np.nan
STORMS["WIND_AGENCY"] = np.nan

# Iterate through the sources
for source, factor in sources_adj:
    mask = pd.isna(STORMS["WIND"]) & ~pd.isna(STORMS[source])  # Where WIND is NaN but source is not NaN
    STORMS.loc[mask, "WIND"] = STORMS.loc[mask, source] * factor
    STORMS.loc[mask, "WIND_AGENCY"] = source

# we can remove all other _WIND columns
col_to_drop = STORMS.columns[STORMS.columns.str.contains('_WIND')] # all columns containing "_WIND"
STORMS.drop(col_to_drop, axis=1, inplace=True) # remove all columns with _WIND
STORMS.isna().sum()




# Detailed explaination for removing columns
# ----------------------------
# List of storms
IDS = df.loc[:, ["SID", "NAME", "NUMBER"]] 
# SID and Name are the same except that some storms don't have names so let's keep SID and remove Name
# NUMBER is the number of the storm for the year. Restart at 1 each year. Remove it. 
IDS.describe() # There are 4767 different storms
IDS.isna().sum() # No NA in SID. 

# LATITUDE
LAT = df.filter(like="LAT", axis=1) # All columns containing "LAT" in their headers
# All latitudes are the same most of the time (+- 0.1, sometimes more but mostly the same).
# All these columns contains the same information. 
LAT = LAT.loc[:, ['LAT']]
LAT.isna().sum() # No na in column LAT

# LONGITUDE
LON = df.filter(like="LON", axis=1)
LON.isna().sum()
# same as with LAT, all longitudes are the same most of the time (+- 0.1, sometimes more but mostly the same).
# All these columns contains the same information. 
LON = LON.loc[:, ['LON']]
LON.isna().sum() # No na in column LAT

# Missing data by location and parameters
STORMS_NA = STORMS.iloc[:, 13:122] # Extract columns with parameters per location
LOC_PARAM = [col.split("_", 1) 
         for col in STORMS_NA.columns] # split headers based on the first _ to split LOC and PARAM
LOC = [p[0] for p in LOC_PARAM] # extract Location from column names
LOC_unique = sorted(set(LOC)) # give a list of unique location
PARAM = [p[1] for p in LOC_PARAM] # extract parameters from column names
PARAM_unique = sorted(set(PARAM)) # give a list of unique parameters

NA = pd.DataFrame(0, index=LOC_unique, columns=PARAM_unique) # Prepare the dataframe to be filled with sum of na

for col in STORMS_NA.columns:
    LOC, PARAM = col.split('_', 1)  # Split only at the first underscore
    NA.loc[LOC, PARAM] += STORMS_NA[col].isna().sum() # sum of NA values
# Not very helpful

# WIND
    # WMO_WIND: all data from agencies but differents units (no adjustement is made for differences in wind speed averaging)
    # I suggest to remove it. No reliable.
    # USA_WIND, DS824_WIND, NEUMANN_WIND, max speed 1-min averaged
    # CMA_WIND, max speed 2-min averaged
    # NEWDELHI_WIND, max speed 3-min averaged
    # TOKYO_WIND, HKO_WIND, KMA_WIND, REUNION_WIND, BOM_WIND, NADI_WIND, WELLINGTON_WIND max speed 10-min averaged
    # TD9636_WIND: in data description "estimates subjective, interpreted with caution". Remove it. 
    # TD9635_WIND, MLC_WIND: only NA
WIND = STORMS.filter(like="WIND", axis =1)
WIND.isna().sum()
WIND.dtypes
# convert wind to numeric
cols = WIND.columns
WIND[cols] = WIND[cols].apply(pd.to_numeric, errors="coerce")
    # We can take USA_WIND as a base because it is where there is the less NAN and complete the missing data with other columns, 
    # especially DS824_WIND and NEUMANN_WIND as it is supposed to be the same unit (max speed 1-min averaged).
"""
WIND.insert(0, "WIND", "")
WIND.insert(1, "AGENCY", "")

for i in WIND.index:
    if not pd.isna(WIND.at[i, "USA_WIND"]):
        WIND.at[i, "WIND"] = WIND.at[i, "USA_WIND"]
        WIND.at[i, "AGENCY"] = "USA_WIND" 
    elif pd.isna(WIND.at[i, "USA_WIND"]) and not pd.isna(WIND.at[i, "DS824_WIND"]):
        WIND.at[i, "WIND"] = WIND.at[i, "DS824_WIND"]
        WIND.at[i, "AGENCY"] = "DS824_WIND"
    elif pd.isna(WIND.at[i, "USA_WIND"]) and pd.isna(WIND.at[i, "DS824_WIND"]) and not pd.isna(WIND.at[i, "NEUMANN_WIND"]):
        WIND.at[i, "WIND"] = WIND.at[i, "NEUMANN_WIND"]
        WIND.at[i, "AGENCY"] = "NEUMANN_WIND"
    else:
        WIND.at[i, "WIND"] = np.nan
        WIND.at[i, "AGENCY"] = np.nan
WIND.isna().sum()
"""
# We don't fill much more data
# WIND.dropna(axis = 0, how='all', inplace = True) # inplace = True is to update the table
# WIND.isna().sum()
# When removing rows with only NA (thus with no data for wind) we still have 30080 rows with NA in WIND and with data somewherelse we could use.
# Problem: data are not in the same unit 
# To convert from max speed 10-min averaged to 1-min averaged : * 1.12
# IBTrACS technical details p5: 
    # "The U.S. agencies (NOAA and JTWC) report a 1 min averaging time for the sustained (i.e. relatively long-lasting) winds. 
    # In most of the rest of the world, a 10 min averaging time is used for "sustained wind". 
    # It is possible to convert from peak 10 min wind to peak 1 min wind (roughly 12% higher for the latter) as a general rule."
# It is not a very accurate method so I suggest not to use it too much.
# (See part 6.2 Wind speed reporting differences from Technical details doc)
"""
for i in WIND.index:
    if pd.isna(WIND.at[i, "USA_WIND"]) and not pd.isna(WIND.at[i, "TOKYO_WIND"]):
        WIND.at[i, "WIND"] = (WIND.at[i, "TOKYO_WIND"] * 1.12)
        WIND.at[i, "AGENCY"] = "TOKYO_WIND"
    elif pd.isna(WIND.at[i, "USA_WIND"]) and not pd.isna(WIND.at[i, "HKO_WIND"]):
        WIND.at[i, "WIND"] = (WIND.at[i, "HKO_WIND"] * 1.12)
        WIND.at[i, "AGENCY"] = "HKO_WIND"
    elif pd.isna(WIND.at[i, "USA_WIND"]) and not pd.isna(WIND.at[i, "KMA_WIND"]):
        WIND.at[i, "WIND"] = (WIND.at[i, "KMA_WIND"] * 1.12)
        WIND.at[i, "AGENCY"] = "KMA_WIND"
    elif pd.isna(WIND.at[i, "USA_WIND"]) and not pd.isna(WIND.at[i, "REUNION_WIND"]):
        WIND.at[i, "WIND"] = (WIND.at[i, "REUNION_WIND"] * 1.12)
        WIND.at[i, "AGENCY"] = "REUNION_WIND"
    elif pd.isna(WIND.at[i, "USA_WIND"]) and not pd.isna(WIND.at[i, "BOM_WIND"]):
        WIND.at[i, "WIND"] = (WIND.at[i, "BOM_WIND"] * 1.12)
        WIND.at[i, "AGENCY"] = "BOM_WIND"
    elif pd.isna(WIND.at[i, "USA_WIND"]) and not pd.isna(WIND.at[i, "NADI_WIND"]):
        WIND.at[i, "WIND"] = (WIND.at[i, "NADI_WIND"] * 1.12)
        WIND.at[i, "AGENCY"] = "NADI_WIND"
    elif pd.isna(WIND.at[i, "USA_WIND"]) and not pd.isna(WIND.at[i, "WELLINGTON_WIND"]):
        WIND.at[i, "WIND"] = (WIND.at[i, "WELLINGTON_WIND"] * 1.12)
        WIND.at[i, "AGENCY"] = "WELLINGTON_WIND" 
WIND.isna().sum() 
"""

# Or in a cleaner way:
sources_adj = [
    ("USA_WIND", 1.0),  # No adjustment
    ("DS824_WIND", 1.0),  # No adjustment
    ("NEUMANN_WIND", 1.0),  # No adjustment
    ("TOKYO_WIND", 1.12),  # Adjustment factor
    ("HKO_WIND", 1.12),
    ("KMA_WIND", 1.12),
    ("REUNION_WIND", 1.12),
    ("BOM_WIND", 1.12),
    ("NADI_WIND", 1.12),
    ("WELLINGTON_WIND", 1.12)
]

# Create the two columns "WIND" and "AGENCY:
WIND["WIND"] = np.nan
WIND["WIND_AGENCY"] = np.nan

# Iterate through the sources
for source, factor in sources_adj:
    mask = pd.isna(WIND["WIND"]) & ~pd.isna(WIND[source])  # Where WIND is NaN but source is not NaN
    WIND.loc[mask, "WIND"] = WIND.loc[mask, source] * factor
    WIND.loc[mask, "WIND_AGENCY"] = source
WIND.dropna(axis = 0, how='all', inplace = True)
WIND.isna().sum()

