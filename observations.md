# Tropical Cyclone Severity Prediction Project 

## First observations 

Our goal is to predict TD9636_STAGE. 
Our dataset is divided by 15 different agencies that provide information (not necessarily at the same time). 
We have multiple pieces of data for the same cyclone. 


## List of questions so far 

1. Hurricane Categories from Control Centers: 
- Some control centers classify the type/category of the hurricane without direct information from their central systems. How does this work? 

opinions, understanding:

<br>
<br>

2. Cyclone Type for Each Center 
- Do we really need the type of cyclone for each center, given that our target is the center TD9636 ? 

opinion: 
Arnaud: Personally, I think not, as this category depends on other elements already present in the dataset. 

<br>
<br>

3. Latitude and Longitude 
- Should we remove the LAT and LON columns for each control center.

opinions : 
Arnaud: yes, These duplicate ID 9 and 10. 

<br>
<br>

4. Missing Data 
Target Column TD9636_STAGE has only about 60,000 data points in column 145 (TD9636_STAGE). 
- should we add More Data?

opinions: 
Arnaud: I think not, as it could skew our sample. 

<br>
<br>

5. Relationships Between Agency Categories 
- Are there noticeable relationships between the categories provided by the agencies ?

opinions:
Arnaud: I haven’t yet checked

<br>
<br>
<br>
<br>

## References: 

IDs 89/90: https://severeweather.wmo.int/TCFW/RAIV_Workshop2023/15a_DvorakTechnique_shortversion_JackBeven.pdf 

 



