import streamlit as st
import pickle
import numpy as np

st.markdown("<div style='background-color:#219C90; border-radius:50px; align-items:center; justify-content: center;'><h1 style='text-align:center; color:white;'>Resale Price Insights</h1></div>",unsafe_allow_html=True)


st.title('Find the best price for your car')

df = pickle.load(open('df.pkl','rb'))
pipe = pickle.load(open('pipe.pkl','rb'))

col1 , col2  = st.columns(2)

with col1:
    st.image('car3.jpg', use_column_width=True)
    st.image('car.jpg', use_column_width=True)
    st.image('car1.jpg', use_column_width=True)
with col2:#select brand
    brand = st.selectbox('Select Brand of your Car',df['brand'].unique(),index=None,placeholder="Select the brand of your car")

    #selecting only cars of selected brand
    filt = df['brand'] ==brand
    car_filt = df.loc[filt,'full_name'].unique()
    car_name = st.selectbox('Select Your Car Name',car_filt,index=None,placeholder="Select the Model of your car")
    #select transmission of car
    filt = df['full_name'] == car_name
    transmission_filt = df.loc[filt, 'transmission_type'].unique()

    transmission = st.selectbox('Automatic vs Manual', transmission_filt,placeholder="Select the transmission type")


    #select Regsieterd year
    year = st.selectbox('Choose Registered Year',np.sort(df['registered_year'].unique())[::-1],index=None)

    if year:
        age = 2023 - year
    else:
        age = df['registered_year'].mode()

    #select insurance
    insurance_list = list(df['insurance'].unique())
    insurance = st.selectbox('Which insurance do you have',insurance_list,placeholder="Select the insurance of your car")




    owner = st.selectbox('Owner Type',df['owner_type'].unique(),placeholder="Select the owner type")
    fuel = st.selectbox('Fuel Type',df['fuel_type'].unique(),placeholder="Select the fuel type")

    #selecting engines  of selected cars
    filt = df['full_name'] == car_name
    engine_filt = df.loc[filt,'engine_capacity'].unique()
    engine = st.selectbox('Engine Capacity',engine_filt)

    kms_driven = st.slider('How Much Car You Drove (Kms Driven)',500,150000)



    button_clicked = st.button('predict car price')
    if button_clicked:
        result = pipe.predict([[car_name,engine,year,insurance,transmission,kms_driven,owner,fuel,brand,age]])
        result = np.round(np.exp(result))
        st.write('resale price of your car should be :')
        st.write(str(result[0]))



