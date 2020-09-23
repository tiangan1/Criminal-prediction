# -*- coding: utf-8 -*-
"""t-SNE&Visualization.ipynb

Automatically generated by Colaboratory.


import pandas as pd
from google.colab import drive
drive.mount('/content/gdrive')

data_raw = pd.read_csv('/content/gdrive/My Drive/Colab Notebooks/Criminal_Prediction/NYPD_Complaint_Sample_Data.csv')
data_raw.head()

rename_dic = rename_dic = {'CMPLNT_NUM':'COMPLAINT_NUMBER','CMPLNT_FR_DT':'COMPLAINT_FROM_DATE','CMPLNT_FR_TM':'COMPLAINT_FROM_TIME',
              'CMPLNT_TO_DT':'COMPLAINT_TO_DATE','CMPLNT_TO_TM':'COMPLAINT_TO_TIME',
              'ADDR_PCT_CD' : 'ADDRESS_PRECINCT_CODE','RPT_DT' : 'REPORT_DT',
              'KY_CD' : 'OFFENSE_CLASS_CODE', 'OFNS_DESC':'OFFENSE_DESCRIBE',
              'PD_CD' : 'INTERNAL_CLASS_CODE','PD_DESC':'INTERNAL_DESCRIBE',
              'CRM_ATPT_CPTD_CD':'CRIME_ATTEMPT_COMPLETED_CODE','LAW_CAT_CD' : 'LEVEL_OF_OFFENSE',
              'BORO_NM':'BOROUGH_NAME','LOC_OF_OCCUR_DESC':'LOCATION_OF_OCCURRENCE_DESCRIBE',
              'PREM_TYP_DESC':'PREMIUM_TYPE_DESCRIBE','JURIS_DESC':'JURISDICTION_DESCRIBE',
              'PARKS_NM':'PARKS_NAME','HOUSING_PSA':'HOUSING_POLICE_SERVICE_AREA',
              'X_COORD_CD':'X_COORDINATE_CODE','Y_COORD_CD':'Y_COORDINATE_CODE',
              'SUSP_AGE_GROUP':'SUSPECT_AGE_GROUP','SUSP_RACE':'SUSPECT_RACE','SUSP_SEX':'SUSPECT_SEX',
              'PATROL_BORO':'PATROL_BOROUGH','VIC_AGE_GROUP':'VICTIM_AGE_GROUP','VIC_RACE':'VICTIM_RACE','VIC_SEX':'VICTIM_SEX',}

data_raw = data_raw.rename(columns = rename_dic).iloc[:,0:]

# select columns we need
data = data_raw.loc[:,['COMPLAINT_FROM_DATE', 'COMPLAINT_FROM_TIME', 
                       'ADDRESS_PRECINCT_CODE', 'OFFENSE_CLASS_CODE', 
                       'OFFENSE_DESCRIBE','INTERNAL_CLASS_CODE',
                       'LEVEL_OF_OFFENSE', 'BOROUGH_NAME',
                       'SUSPECT_AGE_GROUP',
                       'SUSPECT_RACE', 'SUSPECT_SEX', 
                       'Latitude', 'Longitude', 'PATROL_BOROUGH',
                       'VICTIM_AGE_GROUP', 'VICTIM_RACE', 'VICTIM_SEX']]
# Drop NA                        
data = data.dropna()

# Drop UNKNOWN Values
for i in data.columns:
    data = data[data[i] != 'UNKNOWN']
data = data.reset_index(drop=True)
print("The Shape of dataset:")
print(data.shape)
print()
data.head()

# Change COMPLNT_FR_TM to datetime.time type
data.COMPLAINT_FROM_TIME = pd.to_datetime(data.COMPLAINT_FROM_TIME, format='%H:%M:%S')
data.COMPLAINT_FROM_DATE = pd.to_datetime(data.COMPLAINT_FROM_DATE, format='%Y-%m-%d')

# Remove Violation
crime = data[data.LEVEL_OF_OFFENSE != 'VIOLATION'].reset_index(drop=True)

# Convert values to numeric
susp_age = {'<18':0, '18-24':1, '25-44':2,
            '45-64':3, '65+':4}
crime.SUSPECT_AGE_GROUP = crime.SUSPECT_AGE_GROUP.replace(susp_age)


susp_race = {'AMERICAN INDIAN/ALASKAN NATIVE' : 0,
             'ASIAN / PACIFIC ISLANDER' : 1,
             'BLACK HISPANIC' : 2, 'WHITE' : 3,
             'WHITE HISPANIC' : 4, 'BLACK' : 5}
crime.SUSPECT_RACE = crime.SUSPECT_RACE.replace(susp_race)


susp_sex = {'M':1, 'F':0, 'U':2}
crime.SUSPECT_SEX = crime.SUSPECT_SEX.replace(susp_sex)


vic_age = {'<18':0, '18-24':1, '25-44':2,
            '45-64':3, '65+':4}
crime.VICTIM_AGE_GROUP = crime.VICTIM_AGE_GROUP.replace(vic_age)


vic_race = {'AMERICAN INDIAN/ALASKAN NATIVE' : 0,
             'ASIAN / PACIFIC ISLANDER' : 1,
             'BLACK HISPANIC' : 2, 'WHITE' : 3,
             'WHITE HISPANIC' : 4, 'BLACK' : 5}
crime.VICTIM_RACE = crime.VICTIM_RACE.replace(vic_race)


vic_sex = {'M':1, 'F':0}
crime.VICTIM_SEX = crime.VICTIM_SEX.replace(vic_sex)


lvl_offense = {'MISDEMEANOR':-1, 'FELONY':1}
crime.LEVEL_OF_OFFENSE = crime.LEVEL_OF_OFFENSE.replace(lvl_offense)


b_name = {'BROOKLYN':1, 'MANHATTAN':2, 'BRONX':3, 
          'QUEENS':4, 'STATEN ISLAND':5}
crime.BOROUGH_NAME = crime.BOROUGH_NAME.replace(b_name)

crime.COMPLAINT_FROM_TIME = crime.COMPLAINT_FROM_TIME.dt.hour
crime.COMPLAINT_FROM_DATE = crime.COMPLAINT_FROM_DATE.dt.year

offense_code_describe = crime.OFFENSE_DESCRIBE
crime.drop(columns=['OFFENSE_DESCRIBE'], inplace=True)
crime.head()

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
crime = crime.drop(columns=['PATROL_BOROUGH'])
norm_crime = pd.DataFrame(scaler.fit_transform(crime.iloc[:,1:]), 
                          columns=crime.iloc[:,1:].columns,
                          index=crime.index)

from sklearn.decomposition import PCA

pca = PCA()
pca_crime = pca.fit_transform(norm_crime)

# Do LLE
from sklearn.manifold import LocallyLinearEmbedding as LLE

lle = LLE(n_neighbors=550, n_components=2)
lle_data = lle.fit_transform(norm_crime)

from plotly.subplots import make_subplots
import plotly.graph_objects as go

m = crime['LEVEL_OF_OFFENSE']==-1
f = crime['LEVEL_OF_OFFENSE']==1


fig = make_subplots(rows=2, cols=1, 
                    subplot_titles=("PCA", "LLE"))

# PCA
fig.add_trace(go.Scatter(
    x=pca_crime[m, 0],
    y=pca_crime[m, 1],
    mode="markers",
    name='MISDEMEANOR',
    marker_color='red',
    marker_symbol='circle',
),row=1, col=1)

fig.add_trace(go.Scatter(
    x=pca_crime[f, 0],
    y=pca_crime[f, 1],
    mode="markers",
    name='FELONY',
    marker_color='blue',
    marker_symbol='square',
),row=1, col=1)

# LLE
fig.add_trace(go.Scatter(
    x=lle_data[m, 0],
    y=lle_data[m, 1],
    mode="markers",
    name='MISDEMEANOR',
    marker_color='red',
    marker_symbol='circle',
),row=2, col=1)

fig.add_trace(go.Scatter(
    x=lle_data[f, 0],
    y=lle_data[f, 1],
    mode="markers",
    name='FELONY',
    marker_color='blue',
    marker_symbol='square',
),row=2, col=1)


# Update xaxis properties
fig.update_xaxes(title_text="$PC_{1}$", row=1, col=1)
fig.update_xaxes(title_text="$LLE_{1}$", row=2, col=1)


# Update yaxis properties
fig.update_yaxes(title_text="$PC_{2}$", row=1, col=1)
fig.update_yaxes(title_text="$LLE_{2}$", row=2, col=1)

# Edit layout
fig.update_layout(height=1000, width=1800,)

fig.show()

# Compute t-SNE
from sklearn.manifold import TSNE

data2 = crime.drop(columns=['COMPLAINT_FROM_DATE', 
                            'OFFENSE_CLASS_CODE', 'INTERNAL_CLASS_CODE'])
norm_data = scaler.fit_transform(data2)

tsne = TSNE(n_components=2, perplexity=100)
tsne_data = tsne.fit_transform(norm_data)

# Compute UMAP
import umap

umap_ = umap.UMAP(n_neighbors=50, metric='manhattan',
                init='random', min_dist=0.06, spread=3.0)
umap_data = umap_.fit_transform(norm_data)

from plotly.subplots import make_subplots
import plotly.graph_objects as go

brook = crime.BOROUGH_NAME==1
manh = crime.BOROUGH_NAME==2
bronx = crime.BOROUGH_NAME==3
queens = crime.BOROUGH_NAME==4
staten = crime.BOROUGH_NAME==5
f = crime.LEVEL_OF_OFFENSE == 1
m = crime.LEVEL_OF_OFFENSE == -1

fig = make_subplots(rows=1, cols=2, 
                    subplot_titles=("T-SNE", "UMAP"))

fig.add_trace(go.Scatter(
    x=tsne_data[brook&f, 0],
    y=tsne_data[brook&f, 1],
    mode="markers",
    name='Brooklyn',
    marker_color='red',
    marker_size = 20,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=1)

fig.add_trace(go.Scatter(
    x=tsne_data[brook&m, 0],
    y=tsne_data[brook&m, 1],
    mode="markers",
    name='Brooklyn',
    marker_color='red',
    marker_size = 8,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=1)

fig.add_trace(go.Scatter(
    x=tsne_data[manh&f, 0],
    y=tsne_data[manh&f, 1],
    mode="markers",
    name='Manhattan',
    marker_color='green',
    marker_size = 20,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=1)

fig.add_trace(go.Scatter(
    x=tsne_data[manh&m, 0],
    y=tsne_data[manh&m, 1],
    mode="markers",
    name='Manhattan',
    marker_color='green',
    marker_size = 8,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=1)

fig.add_trace(go.Scatter(
    x=tsne_data[bronx&f, 0],
    y=tsne_data[bronx&f, 1],
    mode="markers",
    name='Bronx',
    marker_color='blue',
    marker_size = 20,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=1)

fig.add_trace(go.Scatter(
    x=tsne_data[bronx&m, 0],
    y=tsne_data[bronx&m, 1],
    mode="markers",
    name='Bronx',
    marker_color='blue',
    marker_size = 8,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=1)

fig.add_trace(go.Scatter(
    x=tsne_data[queens&f, 0],
    y=tsne_data[queens&f, 1],
    mode="markers",
    name='Queens',
    marker_color='pink',
    marker_size = 20,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=1)

fig.add_trace(go.Scatter(
    x=tsne_data[queens&m, 0],
    y=tsne_data[queens&m, 1],
    mode="markers",
    name='Queens',
    marker_color='pink',
    marker_size = 8,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=1)

fig.add_trace(go.Scatter(
    x=tsne_data[staten&f, 0],
    y=tsne_data[staten&f, 1],
    mode="markers",
    name='Staten Island',
    marker_color='yellow',
    marker_size = 20,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=1)

fig.add_trace(go.Scatter(
    x=tsne_data[staten&m, 0],
    y=tsne_data[staten&m, 1],
    mode="markers",
    name='Staten Island',
    marker_color='yellow',
    marker_size = 8,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=1)

fig.add_trace(go.Scatter(
    x=umap_data[brook&f, 0],
    y=umap_data[brook&f, 1],
    mode="markers",
    name='Brooklyn',
    marker_color='red',
    marker_size = 20,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=2)

fig.add_trace(go.Scatter(
    x=umap_data[brook&m, 0],
    y=umap_data[brook&m, 1],
    mode="markers",
    name='Brooklyn',
    marker_color='red',
    marker_size = 8,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=2)

fig.add_trace(go.Scatter(
    x=umap_data[manh&f, 0],
    y=umap_data[manh&f, 1],
    mode="markers",
    name='Manhattan',
    marker_color='green',
    marker_size = 20,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=2)

fig.add_trace(go.Scatter(
    x=umap_data[manh&m, 0],
    y=umap_data[manh&m, 1],
    mode="markers",
    name='Manhattan',
    marker_color='green',
    marker_size = 8,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=2)

fig.add_trace(go.Scatter(
    x=umap_data[bronx&f, 0],
    y=umap_data[bronx&f, 1],
    mode="markers",
    name='Bronx',
    marker_color='blue',
    marker_size = 20,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=2)

fig.add_trace(go.Scatter(
    x=umap_data[bronx&m, 0],
    y=umap_data[bronx&m, 1],
    mode="markers",
    name='Bronx',
    marker_color='blue',
    marker_size = 8,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=2)

fig.add_trace(go.Scatter(
    x=umap_data[queens&f, 0],
    y=umap_data[queens&f, 1],
    mode="markers",
    name='Queens',
    marker_color='pink',
    marker_size = 20,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=2)

fig.add_trace(go.Scatter(
    x=umap_data[queens&m, 0],
    y=umap_data[queens&m, 1],
    mode="markers",
    name='Queens',
    marker_color='pink',
    marker_size = 8,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=2)

fig.add_trace(go.Scatter(
    x=umap_data[staten&f, 0],
    y=umap_data[staten&f, 1],
    mode="markers",
    name='Staten Island',
    marker_color='yellow',
    marker_size = 20,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=2)

fig.add_trace(go.Scatter(
    x=umap_data[staten&m, 0],
    y=umap_data[staten&m, 1],
    mode="markers",
    name='Staten Island',
    marker_color='yellow',
    marker_size = 8,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=2)

# Update xaxis properties
fig.update_xaxes(title_text="$t-SNE_{1}$", row=1, col=1)
fig.update_xaxes(title_text="$UMAP_{1}$", row=1, col=2)


# Update yaxis properties
fig.update_yaxes(title_text="$t-SNE_{2}$", row=1, col=1)
fig.update_yaxes(title_text="$UMAP_{2}$", row=1, col=2)

# Edit layout
fig.update_layout(height=800, width=1800,)

fig.show()

from plotly.subplots import make_subplots
import plotly.graph_objects as go

brook = crime.BOROUGH_NAME==1
manh = crime.BOROUGH_NAME==2
bronx = crime.BOROUGH_NAME==3
queens = crime.BOROUGH_NAME==4
staten = crime.BOROUGH_NAME==5
f = crime.LEVEL_OF_OFFENSE == 1
m = crime.LEVEL_OF_OFFENSE == -1

fig = make_subplots(rows=1, cols=2, 
                    subplot_titles=("T-SNE", "UMAP"))

fig.add_trace(go.Scatter(
    x=tsne_data[manh&f, 0],
    y=tsne_data[manh&f, 1],
    mode="markers",
    name='Manhattan',
    marker_color='green',
    marker_size = 20,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=1)

fig.add_trace(go.Scatter(
    x=tsne_data[manh&m, 0],
    y=tsne_data[manh&m, 1],
    mode="markers",
    name='Manhattan',
    marker_color='green',
    marker_size = 8,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=1)

fig.add_trace(go.Scatter(
    x=umap_data[manh&f, 0],
    y=umap_data[manh&f, 1],
    mode="markers",
    name='Manhattan',
    marker_color='green',
    marker_size = 20,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=2)

fig.add_trace(go.Scatter(
    x=umap_data[manh&m, 0],
    y=umap_data[manh&m, 1],
    mode="markers",
    name='Manhattan',
    marker_color='green',
    marker_size = 8,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=2)

# Update xaxis properties
fig.update_xaxes(title_text="$t-SNE_{1}$", row=1, col=1)
fig.update_xaxes(title_text="$UMAP_{1}$", row=1, col=2)


# Update yaxis properties
fig.update_yaxes(title_text="$t-SNE_{2}$", row=1, col=1)
fig.update_yaxes(title_text="$UMAP_{2}$", row=1, col=2)

# Edit layout
fig.update_layout(height=800, width=1800,)

fig.show()

from sklearn.cluster import KMeans
f_kmeans = KMeans(n_clusters=5, random_state=0).fit(tsne_data[manh&f,:])
m_kmeans = KMeans(n_clusters=5, random_state=0).fit(tsne_data[manh&m,:])

manh_tsne_data = tsne_data[manh, :]

fig = make_subplots(rows=1, cols=2, 
                    subplot_titles=("T-SNE", "kMeans"))

fig.add_trace(go.Scatter(
    x=tsne_data[manh&f, 0],
    y=tsne_data[manh&f, 1],
    mode="markers",
    name='Manhattan',
    marker_color='green',
    marker_size = 20,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=1)

fig.add_trace(go.Scatter(
    x=tsne_data[manh&m, 0],
    y=tsne_data[manh&m, 1],
    mode="markers",
    name='Manhattan',
    marker_color='green',
    marker_size = 8,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=1)

fig.add_trace(go.Scatter(
    x=tsne_data[manh&f, 0][f_kmeans.labels_==0],
    y=tsne_data[manh&f, 1][f_kmeans.labels_==0],
    mode="markers",
    name='Felony_red',
    marker_color='red',
    marker_size = 20,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=2)

fig.add_trace(go.Scatter(
    x=tsne_data[manh&f, 0][f_kmeans.labels_==1],
    y=tsne_data[manh&f, 1][f_kmeans.labels_==1],
    mode="markers",
    name='Felony_green',
    marker_color='green',
    marker_size = 20,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=2)

fig.add_trace(go.Scatter(
    x=tsne_data[manh&f, 0][f_kmeans.labels_==2],
    y=tsne_data[manh&f, 1][f_kmeans.labels_==2],
    mode="markers",
    name='Felony_blue',
    marker_color='blue',
    marker_size = 20,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=2)

fig.add_trace(go.Scatter(
    x=tsne_data[manh&f, 0][f_kmeans.labels_==3],
    y=tsne_data[manh&f, 1][f_kmeans.labels_==3],
    mode="markers",
    name='Felony_orange',
    marker_color='orange',
    marker_size = 20,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=2)

fig.add_trace(go.Scatter(
    x=tsne_data[manh&f, 0][f_kmeans.labels_==4],
    y=tsne_data[manh&f, 1][f_kmeans.labels_==4],
    mode="markers",
    name='Felony_yellow',
    marker_color='yellow',
    marker_size = 20,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=2)

fig.add_trace(go.Scatter(
    x=tsne_data[manh&m, 0][m_kmeans.labels_==0],
    y=tsne_data[manh&m, 1][m_kmeans.labels_==0],
    mode="markers",
    name='Mis_red',
    marker_color='red',
    marker_size = 8,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=2)

fig.add_trace(go.Scatter(
    x=tsne_data[manh&m, 0][m_kmeans.labels_==1],
    y=tsne_data[manh&m, 1][m_kmeans.labels_==1],
    mode="markers",
    name='Mis_green',
    marker_color='green',
    marker_size = 8,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=2)

fig.add_trace(go.Scatter(
    x=tsne_data[manh&m, 0][m_kmeans.labels_==2],
    y=tsne_data[manh&m, 1][m_kmeans.labels_==2],
    mode="markers",
    name='Mis_blue',
    marker_color='blue',
    marker_size = 8,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=2)

fig.add_trace(go.Scatter(
    x=tsne_data[manh&m, 0][m_kmeans.labels_==3],
    y=tsne_data[manh&m, 1][m_kmeans.labels_==3],
    mode="markers",
    name='Mis_orange',
    marker_color='orange',
    marker_size = 8,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=2)

fig.add_trace(go.Scatter(
    x=tsne_data[manh&m, 0][m_kmeans.labels_==4],
    y=tsne_data[manh&m, 1][m_kmeans.labels_==4],
    mode="markers",
    name='Mis_yellow',
    marker_color='yellow',
    marker_size = 8,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=2)

# Update xaxis properties
fig.update_xaxes(title_text="$t-SNE_{1}$", row=1, col=1)
fig.update_xaxes(title_text="$t-SNE_{1}$", row=1, col=2)


# Update yaxis properties
fig.update_yaxes(title_text="$t-SNE_{2}$", row=1, col=1)
fig.update_yaxes(title_text="$t-SNE_{2}$", row=1, col=2)

# Edit layout
fig.update_layout(height=800, width=1800,)

fig.show()

manh_df = crime[crime.BOROUGH_NAME==2]
manh_m_df = manh_df[manh_df.LEVEL_OF_OFFENSE==-1]
manh_f_df = manh_df[manh_df.LEVEL_OF_OFFENSE==1]

pip install geopandas

import geopandas as gpd 
import plotly.offline as py

mapbox_access_token = 'pk.eyJ1IjoiZmlzaGVlcCIsImEiOiJjazgwcXd5amIwMnRtM2ZwNDR5OHRjb2Q1In0.wUN67xk4G_3OYy9-tqoqgA'

d = [   go.Scattermapbox(
        lat=manh_m_df.Latitude[m_kmeans.labels_==0],
        lon=manh_m_df.Longitude[m_kmeans.labels_==0],
        mode='markers',
        name='Mis_red',
        marker=go.scattermapbox.Marker(size=5,color='Red')),
     
        go.Scattermapbox(
        lat=manh_m_df.Latitude[m_kmeans.labels_==1],
        lon=manh_m_df.Longitude[m_kmeans.labels_==1],
        mode='markers',
        name='Mis_green',
        marker=go.scattermapbox.Marker(size=5,color='Green')),
     
        go.Scattermapbox(
        lat=manh_m_df.Latitude[m_kmeans.labels_==2],
        lon=manh_m_df.Longitude[m_kmeans.labels_==2],
        mode='markers',
        name='Mis_blue',
        marker=go.scattermapbox.Marker(size=5, color='Blue')),

        go.Scattermapbox(
        lat=manh_m_df.Latitude[m_kmeans.labels_==3],
        lon=manh_m_df.Longitude[m_kmeans.labels_==3],
        mode='markers',
        name='Mis_orange',
        marker=go.scattermapbox.Marker(size=5, color='orange')),
     
        go.Scattermapbox(
        lat=manh_m_df.Latitude[m_kmeans.labels_==4],
        lon=manh_m_df.Longitude[m_kmeans.labels_==4],
        mode='markers',
        name='Mis_yellow',
        marker=go.scattermapbox.Marker(size=5, color='yellow')),
        # Plot Felony
        go.Scattermapbox(
        lat=manh_f_df.Latitude[f_kmeans.labels_==0],
        lon=manh_f_df.Longitude[f_kmeans.labels_==0],
        mode='markers',
        name='Felony_red',
        marker=go.scattermapbox.Marker(size=8,color='Red')),
        
        go.Scattermapbox(
        lat=manh_f_df.Latitude[f_kmeans.labels_==1],
        lon=manh_f_df.Longitude[f_kmeans.labels_==1],
        mode='markers',
        name='Felony_green',
        marker=go.scattermapbox.Marker(size=8,color='Green')),
     
        go.Scattermapbox(
        lat=manh_f_df.Latitude[f_kmeans.labels_==2],
        lon=manh_f_df.Longitude[f_kmeans.labels_==2],
        mode='markers',
        name='Felony_blue',
        marker=go.scattermapbox.Marker(size=8, color='Blue')),

        go.Scattermapbox(
        lat=manh_f_df.Latitude[f_kmeans.labels_==3],
        lon=manh_f_df.Longitude[f_kmeans.labels_==3],
        mode='markers',
        name='Felony_orange',
        marker=go.scattermapbox.Marker(size=8, color='orange')),
     
        go.Scattermapbox(
        lat=manh_f_df.Latitude[f_kmeans.labels_==4],
        lon=manh_f_df.Longitude[f_kmeans.labels_==4],
        mode='markers',
        name='Felony_yellow',
        marker=go.scattermapbox.Marker(size=8, color='yellow'))
        ]


layout = go.Layout(
    title=dict(text = 'NYC Crimes Locations',
                              y=0.95, x=0.5,
                              xanchor='center',
                              yanchor='top'),
    autosize=True,
    hovermode='closest',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=dict(lat=40.729302,
                    lon=-73.986670),
        pitch=45,
        zoom=10,
        style='mapbox://styles/mapbox/light-v10'),
    height=900)

fig = dict(data=d, layout=layout)

py.iplot(fig)

from sklearn.cluster import DBSCAN
m_clustering = DBSCAN(eps=5, min_samples=150).fit(tsne_data[manh&m,:])
f_clustering = DBSCAN(eps=5, min_samples=50).fit(tsne_data[manh&f,:])

manh_tsne_data = tsne_data[manh, :]

fig = make_subplots(rows=1, cols=2, 
                    subplot_titles=("T-SNE", "DBSCAN"))

fig.add_trace(go.Scatter(
    x=tsne_data[manh&f, 0],
    y=tsne_data[manh&f, 1],
    mode="markers",
    name='Manhattan',
    marker_color='green',
    marker_size = 20,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=1)

fig.add_trace(go.Scatter(
    x=tsne_data[manh&m, 0],
    y=tsne_data[manh&m, 1],
    mode="markers",
    name='Manhattan',
    marker_color='green',
    marker_size = 8,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=1)

fig.add_trace(go.Scatter(
    x=tsne_data[manh&f, 0][f_clustering.labels_==-1],
    y=tsne_data[manh&f, 1][f_clustering.labels_==-1],
    mode="markers",
    name='Felony_red',
    marker_color='red',
    marker_size = 20,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=2)

fig.add_trace(go.Scatter(
    x=tsne_data[manh&f, 0][f_clustering.labels_==0],
    y=tsne_data[manh&f, 1][f_clustering.labels_==0],
    mode="markers",
    name='Felony_green',
    marker_color='green',
    marker_size = 20,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=2)

fig.add_trace(go.Scatter(
    x=tsne_data[manh&f, 0][f_clustering.labels_==1],
    y=tsne_data[manh&f, 1][f_clustering.labels_==1],
    mode="markers",
    name='Felony_blue',
    marker_color='blue',
    marker_size = 20,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=2)

fig.add_trace(go.Scatter(
    x=tsne_data[manh&f, 0][f_clustering.labels_==2],
    y=tsne_data[manh&f, 1][f_clustering.labels_==2],
    mode="markers",
    name='Felony_orange',
    marker_color='orange',
    marker_size = 20,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=2)

fig.add_trace(go.Scatter(
    x=tsne_data[manh&m, 0][m_clustering.labels_==-1],
    y=tsne_data[manh&m, 1][m_clustering.labels_==-1],
    mode="markers",
    name='Mis_red',
    marker_color='red',
    marker_size = 8,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=2)

fig.add_trace(go.Scatter(
    x=tsne_data[manh&m, 0][m_clustering.labels_==0],
    y=tsne_data[manh&m, 1][m_clustering.labels_==0],
    mode="markers",
    name='Mis_green',
    marker_color='green',
    marker_size = 8,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=2)

fig.add_trace(go.Scatter(
    x=tsne_data[manh&m, 0][m_clustering.labels_==1],
    y=tsne_data[manh&m, 1][m_clustering.labels_==1],
    mode="markers",
    name='Mis_blue',
    marker_color='blue',
    marker_size = 8,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=2)

fig.add_trace(go.Scatter(
    x=tsne_data[manh&m, 0][m_clustering.labels_==2],
    y=tsne_data[manh&m, 1][m_clustering.labels_==2],
    mode="markers",
    name='Mis_orange',
    marker_color='orange',
    marker_size = 8,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=2)

# Update xaxis properties
fig.update_xaxes(title_text="$t-SNE_{1}$", row=1, col=1)
fig.update_xaxes(title_text="$t-SNE_{1}$", row=1, col=2)


# Update yaxis properties
fig.update_yaxes(title_text="$t-SNE_{2}$", row=1, col=1)
fig.update_yaxes(title_text="$t-SNE_{2}$", row=1, col=2)

# Edit layout
fig.update_layout(height=800, width=1800,)

fig.show()

fig = make_subplots(rows=1, cols=2, 
                    subplot_titles=("kMeans", "DBSCAN"))

fig.add_trace(go.Scatter(
    x=tsne_data[manh&f, 0][f_kmeans.labels_==0],
    y=tsne_data[manh&f, 1][f_kmeans.labels_==0],
    mode="markers",
    name='Felony_red',
    marker_color='red',
    marker_size = 20,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=1)

fig.add_trace(go.Scatter(
    x=tsne_data[manh&f, 0][f_kmeans.labels_==1],
    y=tsne_data[manh&f, 1][f_kmeans.labels_==1],
    mode="markers",
    name='Felony_green',
    marker_color='green',
    marker_size = 20,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=1)

fig.add_trace(go.Scatter(
    x=tsne_data[manh&f, 0][f_kmeans.labels_==2],
    y=tsne_data[manh&f, 1][f_kmeans.labels_==2],
    mode="markers",
    name='Felony_blue',
    marker_color='blue',
    marker_size = 20,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=1)

fig.add_trace(go.Scatter(
    x=tsne_data[manh&f, 0][f_kmeans.labels_==3],
    y=tsne_data[manh&f, 1][f_kmeans.labels_==3],
    mode="markers",
    name='Felony_orange',
    marker_color='orange',
    marker_size = 20,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=1)

fig.add_trace(go.Scatter(
    x=tsne_data[manh&f, 0][f_kmeans.labels_==4],
    y=tsne_data[manh&f, 1][f_kmeans.labels_==4],
    mode="markers",
    name='Felony_yellow',
    marker_color='yellow',
    marker_size = 20,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=1)

fig.add_trace(go.Scatter(
    x=tsne_data[manh&m, 0][m_kmeans.labels_==0],
    y=tsne_data[manh&m, 1][m_kmeans.labels_==0],
    mode="markers",
    name='Mis_red',
    marker_color='red',
    marker_size = 8,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=1)

fig.add_trace(go.Scatter(
    x=tsne_data[manh&m, 0][m_kmeans.labels_==1],
    y=tsne_data[manh&m, 1][m_kmeans.labels_==1],
    mode="markers",
    name='Mis_green',
    marker_color='green',
    marker_size = 8,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=1)

fig.add_trace(go.Scatter(
    x=tsne_data[manh&m, 0][m_kmeans.labels_==2],
    y=tsne_data[manh&m, 1][m_kmeans.labels_==2],
    mode="markers",
    name='Mis_blue',
    marker_color='blue',
    marker_size = 8,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=1)

fig.add_trace(go.Scatter(
    x=tsne_data[manh&m, 0][m_kmeans.labels_==3],
    y=tsne_data[manh&m, 1][m_kmeans.labels_==3],
    mode="markers",
    name='Mis_orange',
    marker_color='orange',
    marker_size = 8,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=1)

fig.add_trace(go.Scatter(
    x=tsne_data[manh&m, 0][m_kmeans.labels_==4],
    y=tsne_data[manh&m, 1][m_kmeans.labels_==4],
    mode="markers",
    name='Mis_yellow',
    marker_color='yellow',
    marker_size = 8,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=1)

fig.add_trace(go.Scatter(
    x=tsne_data[manh&f, 0][f_clustering.labels_==-1],
    y=tsne_data[manh&f, 1][f_clustering.labels_==-1],
    mode="markers",
    name='Felony_orange',
    marker_color='orange',
    marker_size = 20,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=2)

fig.add_trace(go.Scatter(
    x=tsne_data[manh&f, 0][f_clustering.labels_==0],
    y=tsne_data[manh&f, 1][f_clustering.labels_==0],
    mode="markers",
    name='Felony_green',
    marker_color='green',
    marker_size = 20,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=2)

fig.add_trace(go.Scatter(
    x=tsne_data[manh&f, 0][f_clustering.labels_==1],
    y=tsne_data[manh&f, 1][f_clustering.labels_==1],
    mode="markers",
    name='Felony_red',
    marker_color='red',
    marker_size = 20,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=2)

fig.add_trace(go.Scatter(
    x=tsne_data[manh&f, 0][f_clustering.labels_==2],
    y=tsne_data[manh&f, 1][f_clustering.labels_==2],
    mode="markers",
    name='Felony_blue',
    marker_color='blue',
    marker_size = 20,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=2)

fig.add_trace(go.Scatter(
    x=tsne_data[manh&m, 0][m_clustering.labels_==-1],
    y=tsne_data[manh&m, 1][m_clustering.labels_==-1],
    mode="markers",
    name='Mis_orange',
    marker_color='orange',
    marker_size = 8,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=2)

fig.add_trace(go.Scatter(
    x=tsne_data[manh&m, 0][m_clustering.labels_==0],
    y=tsne_data[manh&m, 1][m_clustering.labels_==0],
    mode="markers",
    name='Mis_green',
    marker_color='green',
    marker_size = 8,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=2)

fig.add_trace(go.Scatter(
    x=tsne_data[manh&m, 0][m_clustering.labels_==1],
    y=tsne_data[manh&m, 1][m_clustering.labels_==1],
    mode="markers",
    name='Mis_blue',
    marker_color='blue',
    marker_size = 8,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=2)

fig.add_trace(go.Scatter(
    x=tsne_data[manh&m, 0][m_clustering.labels_==2],
    y=tsne_data[manh&m, 1][m_clustering.labels_==2],
    mode="markers",
    name='Mis_red',
    marker_color='red',
    marker_size = 8,
    marker_line = dict(color='black',
                       width=1)
),row=1, col=2)

# Update xaxis properties
fig.update_xaxes(title_text="$t-SNE_{1}$", row=1, col=1)
fig.update_xaxes(title_text="$t-SNE_{1}$", row=1, col=2)


# Update yaxis properties
fig.update_yaxes(title_text="$t-SNE_{2}$", row=1, col=1)
fig.update_yaxes(title_text="$t-SNE_{2}$", row=1, col=2)

# Edit layout
fig.update_layout(height=800, width=1800,)

fig.show()

import geopandas as gpd 
import plotly.offline as py

mapbox_access_token = 'pk.eyJ1IjoiZmlzaGVlcCIsImEiOiJjazgwcXd5amIwMnRtM2ZwNDR5OHRjb2Q1In0.wUN67xk4G_3OYy9-tqoqgA'

d = [   go.Scattermapbox(
        lat=manh_m_df.Latitude[m_clustering.labels_==2],
        lon=manh_m_df.Longitude[m_clustering.labels_==2],
        mode='markers',
        name='Mis_red',
        marker=go.scattermapbox.Marker(size=5,color='Red')),
     
        go.Scattermapbox(
        lat=manh_m_df.Latitude[m_clustering.labels_==0],
        lon=manh_m_df.Longitude[m_clustering.labels_==0],
        mode='markers',
        name='Mis_green',
        marker=go.scattermapbox.Marker(size=5,color='Green')),
     
        go.Scattermapbox(
        lat=manh_m_df.Latitude[m_clustering.labels_==1],
        lon=manh_m_df.Longitude[m_clustering.labels_==1],
        mode='markers',
        name='Mis_blue',
        marker=go.scattermapbox.Marker(size=5, color='Blue')),

        go.Scattermapbox(
        lat=manh_m_df.Latitude[m_clustering.labels_==-1],
        lon=manh_m_df.Longitude[m_clustering.labels_==-1],
        mode='markers',
        name='Mis_orange',
        marker=go.scattermapbox.Marker(size=5, color='orange')),
     
        # Plot Felony
        go.Scattermapbox(
        lat=manh_f_df.Latitude[f_clustering.labels_==1],
        lon=manh_f_df.Longitude[f_clustering.labels_==1],
        mode='markers',
        name='Felony_red',
        marker=go.scattermapbox.Marker(size=8,color='Red')),
        
        go.Scattermapbox(
        lat=manh_f_df.Latitude[f_clustering.labels_==0],
        lon=manh_f_df.Longitude[f_clustering.labels_==0],
        mode='markers',
        name='Felony_green',
        marker=go.scattermapbox.Marker(size=8,color='Green')),
     
        go.Scattermapbox(
        lat=manh_f_df.Latitude[f_clustering.labels_==2],
        lon=manh_f_df.Longitude[f_clustering.labels_==2],
        mode='markers',
        name='Felony_blue',
        marker=go.scattermapbox.Marker(size=8, color='Blue')),

        go.Scattermapbox(
        lat=manh_f_df.Latitude[f_clustering.labels_==-1],
        lon=manh_f_df.Longitude[f_clustering.labels_==-1],
        mode='markers',
        name='Felony_orange',
        marker=go.scattermapbox.Marker(size=8, color='orange')),
     
        ]


layout = go.Layout(
    title=dict(text = 'NYC Crimes Locations',
                              y=0.95, x=0.5,
                              xanchor='center',
                              yanchor='top'),
    autosize=True,
    hovermode='closest',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=dict(lat=40.729302,
                    lon=-73.986670),
        pitch=45,
        zoom=10,
        style='mapbox://styles/mapbox/light-v10'),
    height=900)

fig = dict(data=d, layout=layout)

py.iplot(fig)

manh_df

manh_m_df['Clusting'] = m_clustering.labels_
manh_m_df

manh_f_df['Clusting'] = f_clustering.labels_
manh_f_df

# Mapping with folium - works good for 1k not for 100k

locations = manh_df[['Latitude', 'Longitude']]
locationlist = locations.values.tolist()

#Import maps
import folium
from folium import plugins

crime_map = folium.Map(location=[40.6865,-73.9496], 
                       tiles='Stamen Terrain', zoom_start=10)


marker_cluster = plugins.MarkerCluster().add_to(crime_map)

#I don`t know how to add a popup station`s name imported from 
    #df_stations['start_station_name'] column, ordinary solution doesn't work :/
# parse_html=True - this is the solution
#folium.Cricle(locationlist[point],radius=40).add_to(marker_cluster)
for point in range(0, len(manh_m_df)):
    folium.Marker(locationlist[point],
                  icon=folium.Icon(color='blue', icon_color='white', 
                                   icon='fa-circle', angle=0, 
                                   prefix='fa')).add_to(marker_cluster)
folium.Circle(locationlist[point],radius=1600).add_to(marker_cluster)
crime_map

pip install pydeck

import pydeck as pdk

# 2014 locations of car accidents in the UK
UK_ACCIDENTS_DATA = ('https://raw.githubusercontent.com/uber-common/'
                     'deck.gl-data/master/examples/3d-heatmap/heatmap-data.csv')

# Define a layer to display on a map
layer = pdk.Layer(
    'HexagonLayer',
    UK_ACCIDENTS_DATA,
    get_position=['lng', 'lat'],
    auto_highlight=True,
    elevation_scale=50,
    pickable=True,
    elevation_range=[0, 3000],
    extruded=True,                 
    coverage=1)

# Set the viewport location
view_state = pdk.ViewState(
    longitude=-1.415,
    latitude=52.2323,
    zoom=6,
    min_zoom=5,
    max_zoom=15,
    pitch=40.5,
    bearing=-27.36)

# Render
r = pdk.Deck(layers=[layer], initial_view_state=view_state)
r.to_html('demo.html')

UK_ACCIDENTS_DATA

import pandas as pd
import pydeck

# Load in the JSON data
DATA_URL = 'https://raw.githubusercontent.com/uber-common/deck.gl-data/master/examples/geojson/vancouver-blocks.json'
json = pd.read_json(DATA_URL)
polygon_df = pd.DataFrame()

# Parse the geometry out in Pandas and pass it to deck.gl's PolygonLayer
# I'll make the next release such that you don't have to do this
# manual extraction.
polygon_df['coordinates'] = json['features'].apply(lambda row: row['geometry']['coordinates'])
polygon_df['valuePerSqm'] = json['features'].apply(lambda row: row['properties']['valuePerSqm'])
polygon_df['growth'] = json['features'].apply(lambda row: row['properties']['growth'])
polygon_df.head()

INITIAL_VIEW_STATE = pydeck.ViewState(
    latitude=49.254,
    longitude=-123.13,
    zoom=11,
    max_zoom=16,
    pitch=45,
    bearing=0
)

geojson = pydeck.Layer(
    'PolygonLayer',
    polygon_df,
    opacity=0.8,
    get_polygon='coordinates',
    stroked=False,
    filled=True,
    extruded=True,
    wireframe=True,
    get_elevation='valuePerSqm / 20',
    get_fill_color='[255, 255, growth * 255]',
    get_line_color=[255, 255, 255],
    pickable=True
)

r = pydeck.Deck(
    layers=[geojson],
    initial_view_state=INITIAL_VIEW_STATE)
r.to_html(iframe_width=1000)

polygon_df

