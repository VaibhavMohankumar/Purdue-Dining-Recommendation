import streamlit as st
import constants
from datetime import date
import data_loader as dl
import data_filterer as dfr
import recommendation_algorithm as ra
import pandas as pd

st.title("Purdue Dining Recommendation")
st.write("Find Purdue dining items that match your nutrition and dietary preferences.")

with st.sidebar:
    location = st.selectbox("Dining location", constants.DINING_HALLS)
    menu_date = st.date_input("Menu date", date.today())
    meal_period = st.selectbox("Meal period", constants.MEAL_OPTIONS)
    
    dietary_restrictions = st.selectbox("Dietary Restrictions", constants.DIETARY_COLUMNS)
    allergens = st.multiselect("Allergies", constants.ALLERGENS)
    
    desired_cals = st.number_input("Desired calories", min_value=50, max_value=800, value=400, step=50) or None
    desired_protein = st.number_input("Desired protein (g)", min_value=10, max_value=30, value=10, step=5) or None
    desired_carbs = st.number_input("Desired carbs", min_value=10, max_value=150, value=50, step=10) or None
    desired_fat = st.number_input("Desired fat", min_value=5, max_value=50, value=20, step=5) or None
    
    limit = st.slider("Recommendations", 1, 20, 5)
    
if st.button("Recommend items", type="primary"):
    try:
        with st.spinner("Fetching Purdue menu data"):
            menu_data = pd.DataFrame()
            menu_data = dl.get_json(location=location, menu_date=menu_date, meal_period= meal_period)
            menu_data = dl.parse_data(menu_data)
            menu_data = dfr.filter_dietary_restrictions(menu_data, diet_restriction=dietary_restrictions, allergens=allergens)
            menu_data = ra.recommend_item(menu_data, desired_cals, desired_protein, desired_carbs, desired_fat, limit=limit)
        if menu_data.empty:
            st.error("No items meet search criteria")
        else:
            for _, row in menu_data.iterrows():
                print(row)
                with st.container(border=True):
                    st.subheader(row["item_name"])
                    st.caption(f"{row['station_name']}")
                    st.write(row["recommendation_reason"])
                    
                    diet_restrictions = []
                    known_allergens = []
                    for col_name, value in row.items():
                        print(value)
                        print(col_name.partition("-")[0])
                        if pd.notna(value):
                            if col_name.partition("-")[0] in constants.ALLERGENS:
                                known_allergens.append(col_name.partition("-")[0])
                            if col_name.partition("-")[0] in constants.DIETARY_COLUMNS:
                                diet_restrictions.append(col_name.partition("-")[0])
                    
                    st.write("Meets dietary restrictions for: ", "None" if (len(diet_restrictions) == 0) else (", ".join(diet_restrictions)))
                    st.write("Contains: ", "No listed allergens" if (len(known_allergens) == 0) else (", ".join(known_allergens)))
    except Exception as e:
        st.error(f"Could not load Purdue dining data: {e}")
            