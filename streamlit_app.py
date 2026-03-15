# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col,when_matched
import requests  

# Write directly to the app
st.title(":cup_with_straw: Customize your smoothie :cup_with_straw:")
st.write(
  """Chose the Fruite you want for your Smoothi.
  """
)

cnx = st.connection("snowflake")
session=cnx.session()

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
ingredients_list = st.multiselect("Choose up to 5 ingredients:", my_dataframe, max_selections=5)

if ingredients_list:

    ingredients_string =''

    for fruit_chosen in ingredients_list:
        ingredients_string+=fruit_chosen +' '
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+fruit_chosen)  
        sf_df=st.dataframe(data=smoothiefroot_response.json())

    st.write(ingredients_string)    

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                    values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    
    time_to_insert = st.button('Submit Order')


    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
      

