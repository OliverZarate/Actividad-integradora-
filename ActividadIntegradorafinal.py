import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

imagen = Image.open("C:/Users/olive/Desktop/Patch_of_the_San_Francisco_Police_Department.jpg")

st.image(imagen, caption='Police Department Logo', use_column_width=True)

st.title('Police Incident Reports from 2018 to 2020 in San Francisco')

df = pd.read_csv("Police_Department_Incident_Reports__2018_to_Present.csv")

st.markdown('The data shown below belongs to incident reports in the city of San Francisco, from the year 2018 to 2020, with details from each case such as date, day of the week, police district, neighborhood in which it happened, type of incident in category and subcategory, exact location and resolution.')

mapa = pd.DataFrame()
mapa['Date'] = df['Incident Date']
mapa['Day'] = df['Incident Day of Week']
mapa['Police District'] = df['Police District']
mapa['Neighborhood'] = df['Analysis Neighborhood']
mapa['Incident Category'] = df['Incident Category']
mapa['Incident Subcategory'] = df['Incident Subcategory']
mapa['Resolution'] = df['Resolution']
mapa['lat'] = df['Latitude']
mapa['lon'] = df['Longitude']
mapa = mapa.dropna()

filtro_de_color = st.sidebar.color_picker("Select Graph Color", "#1f77b4")

subset_data2 = mapa
police_district_input = st.sidebar.multiselect(
    'Police District',
    mapa.groupby('Police District').count().reset_index()['Police District'].tolist()
)
if len(police_district_input) > 0:
    subset_data2 = mapa[mapa['Police District'].isin(police_district_input)]

subset_data1 = subset_data2

neighborhood_input = st.sidebar.multiselect(
    'Neighborhood',
    subset_data2.groupby('Neighborhood').count().reset_index()['Neighborhood'].tolist()
)
if len(neighborhood_input) > 0:
    subset_data1 = subset_data2[subset_data2['Neighborhood'].isin(neighborhood_input)]

selected_days = st.sidebar.multiselect(
    'Select Days of the Week',
    mapa['Day'].unique()
)
if len(selected_days) > 0:
    subset_data1 = subset_data1[subset_data1['Day'].isin(selected_days)]

subset_data = subset_data1

incident_input = st.sidebar.multiselect(
    'Incident Category',
    subset_data1.groupby('Incident Category').count().reset_index()['Incident Category'].tolist()
)
if len(incident_input) > 0:
    subset_data = subset_data1[subset_data2['Incident Category'].isin(incident_input)]

subset_data
st.markdown('It is important to mention that any police district can answer to any incident, the neighborhood in which it happened is not related to the police district.')
st.markdown('Crime locations in San Francisco')
st.map(subset_data, color=filtro_de_color)  
st.markdown('Crimes occurred per day of the week')
st.bar_chart(subset_data['Day'].value_counts(), color=filtro_de_color)  
st.markdown('Crimes occurred per date')
st.line_chart(subset_data['Date'].value_counts())
st.markdown('Type of crimes committed')
st.bar_chart(subset_data['Incident Category'].value_counts(), color=filtro_de_color)  
agree = st.button('Click to see Incident Subcategories')
if agree:
    st.markdown('Subtype of crimes committed')
    st.bar_chart(subset_data['Incident Category'].value_counts(), color=filtro_de_color)  
st.markdown('Resolution status')
fig1, ax1 = plt.subplots()
labels = subset_data['Resolution'].unique()
ax1.pie(subset_data['Resolution'].value_counts(), labels=labels, autopct='1.1f%%', startangle=20)
st.pyplot(fig1)


show_last_chart = st.checkbox('Show/Hide Last Chart')
if show_last_chart:
    st.markdown('Incidents per Police District')
    st.bar_chart(subset_data['Police District'].value_counts(), color=filtro_de_color)

st.text("Oliver Zárate Palafox A01610960")


