"""
Purdue Dining Recommendation Streamlit Application.

This application helps Purdue students find menu items that match their
nutrition goals, dietary restrictions, and allergen preferences.

The application:

1. Fetches menu data from the Purdue Dining API.
2. Parses the API response into a pandas DataFrame.
3. Filters items based on dietary restrictions and allergens.
4. Ranks compatible items using a nearest-neighbors algorithm.
5. Displays personalized recommendations through Streamlit.
"""

from datetime import date
from dining_exception import DiningException
import requests
import streamlit as st
import pandas as pd
import constants
import data_loader as dl
import data_filterer as dfr
import recommendation_algorithm as ra

# Session states to keep menu data and recommendations consistent
if "selections" not in st.session_state:
    st.session_state.selections = []
if "recommendations" not in st.session_state:
    st.session_state.recommendations = None
if "builder_menu" not in st.session_state:
    st.session_state.builder_menu = None

def _update_selection(item_name, key):
    """
    Add or remove a menu item from the user's custom meal selections.

    Reads the checkbox state from Streamlit's session state. If the checkbox
    is selected, the item name is added to ``st.session_state.selections``.
    If it is deselected, the item name is removed.

    Args:
        item_name: Name of the menu item associated with the checkbox.
        key: Session-state key used by that checkbox.
    """
    if st.session_state[key]:
        if item_name not in st.session_state.selections:
            st.session_state.selections.append(item_name)
    else:
        if item_name in st.session_state.selections:
            st.session_state.selections.remove(item_name)

def _item_loader(menu_data):
    """
    Display menu items as Streamlit containers.

    Each card shows the item's name, station, serving size, dietary traits,
    and listed allergens. In the recommendation tab, it also displays the
    recommendation reason and a nutrition comparison chart. In the custom
    meal builder tab, it displays a checkbox for selecting the item.

    Args:
        menu_data: DataFrame containing menu items to display. It may contain
            recommendation details when used to show ranked results.

    Returns:
        The names of the items currently selected for the custom meal,
        stored in ``st.session_state.selections``.
    """
    for i, (_, row) in enumerate(menu_data.iterrows()):
            with st.container(border=True, width="stretch"):
                
                # Include a spot for the checkbox if on builder tab
                if build.open:
                    left, right = st.columns([0.9, 0.1])
                else:
                    left, right = st.columns([0.99, 0.01])
                with left:
                    st.subheader(row["item_name"])
                    st.caption(row['station_name'])
                    if "recommendation_reason" in row.index:
                        st.write(row["recommendation_reason"])
                    st.write("Serving Size: " + row["Serving Size-value"] if pd.notna(row["Serving Size-value"]) else "Not available")
                    
                    diet_restrictions = []
                    known_allergens = []
                    
                    # Adds list of dietary restrictions and allergens for each item to 
                    # each item container object in the streamlit interface
                    for col_name, value in row.items():
                        if pd.notna(value):
                            if col_name.partition("-")[0] in constants.ALLERGENS:
                                known_allergens.append(col_name.partition("-")[0])
                            if col_name.partition("-")[0] in constants.DIETARY_COLUMNS:
                                diet_restrictions.append(col_name.partition("-")[0])
                    
                    st.write("Meets dietary restrictions for: ", "None" if (len(diet_restrictions) == 0) else (", ".join(diet_restrictions)))
                    st.write("Contains: ", "No listed allergens" if (len(known_allergens) == 0) else (", ".join(known_allergens)))
                    
                    # Nutrition bar vizualizer to aid user in seeing how much of their prefernce was met
                    if recommender.open:
                        nutrition_targets = {
                            "Calories": desired_cals,
                            "Carbohydrates (g)": desired_carbs,
                            "Protein (g)": desired_protein,
                            "Fat (g)": desired_fat
                        }

                        nutrition_values = {
                            "Calories": row.get("Calories-value", 0),
                            "Carbohydrates (g)": row.get("Total Carbohydrate-value", 0),
                            "Protein (g)": row.get("Protein-value", 0),
                            "Fat (g)": row.get("Total fat-value", 0)
                        }
                        
                        # Calculates percentage of user preference met for each nutrition labal
                        percentage_values = {}
                        for nutrition, preference in nutrition_targets.items():
                            actual = nutrition_values[nutrition]

                            actual = pd.to_numeric(nutrition_values[nutrition], errors="coerce")

                            if pd.notna(actual) and preference is not None and preference != 0:
                                percentage_values[nutrition] = (actual / preference) * 100

                        st.caption("Percentage of nutrition preference met")
                        nutrition_chart = pd.DataFrame({"Percent of preference": percentage_values})
                        st.bar_chart(nutrition_chart, y_label="percentage of preference", horizontal=True, height=180)
                with right:
                    # Updates selections by users for their custom meal
                    if build.open:
                        key = f"builder_select_{i}_{row['item_id']}"
                        st.checkbox(
                            f"Select {row['item_name']}",
                            key=key,
                            on_change=_update_selection,
                            args=(row["item_name"], key),
                            label_visibility="collapsed",
                        )
    return st.session_state.selections


st.title("Purdue Dining Recommendation")
recommender, build = st.tabs(["Dining Recommender", "Custom Meal Builder"], on_change="rerun")

with st.sidebar:
    location = st.selectbox("Dining location", constants.DINING_HALLS)
    menu_date = st.date_input("Menu date", date.today())
    meal_period = st.selectbox("Meal period", constants.MEAL_OPTIONS)
    
    dietary_restrictions = st.selectbox("Dietary Restrictions", constants.DIETARY_COLUMNS)
    allergens = st.multiselect("Allergies", constants.ALLERGENS)
    
    # Desired nutritonal info only required to recommend
    if recommender.open:
        desired_cals = st.number_input("Desired calories", min_value=50, max_value=800, value=400, step=50) or None
        desired_protein = st.number_input("Desired protein (g)", min_value=5, max_value=30, value=10, step=5) or None
        desired_carbs = st.number_input("Desired carbs", min_value=10, max_value=150, value=50, step=10) or None
        desired_fat = st.number_input("Desired fat", min_value=5, max_value=50, value=20, step=5) or None
        limit = st.slider("Recommendations", 1, 20, 5)


with recommender:
    st.write("Find Purdue dining items that match your nutrition and dietary preferences.")
        
    if st.button("Recommend items", type="primary"):
        try:
            with st.spinner("Fetching Purdue menu data"):
                menu_data = dl.get_json(location=location, menu_date=menu_date, meal_period= meal_period)
                menu_data = dl.parse_data(menu_data)
                menu_data = dfr.filter_dietary_restrictions(menu_data, diet_restriction=dietary_restrictions, allergens=allergens)
                menu_data = ra.recommend_item(menu_data, desired_cals, desired_protein, desired_carbs, desired_fat, limit=limit)
            st.session_state.recommendations = menu_data
        except (DiningException, requests.exceptions.RequestException) as e:
            st.error(f"Could not load Purdue dining data: {e}")
        except Exception as f:
            st.error(f"Unexpected error: {f}")

    # Keep recommendations visible after tab switches
    recommendations = st.session_state.recommendations
    if recommendations is not None:
        if recommendations.empty:
            st.error("No items meet search criteria")
        else:
            _item_loader(recommendations)
                
                
with build:
    st.write("Build a Custom Meal")
    
    if st.button("Load items", type="primary"):
        try:
            with st.spinner("Fetching Purdue menu data"):
                menu_data = dl.get_json(location=location, menu_date=menu_date, meal_period= meal_period)
                menu_data = dl.parse_data(menu_data)
                menu_data = dfr.filter_dietary_restrictions(menu_data, diet_restriction=dietary_restrictions, allergens=allergens)
                st.session_state.builder_menu = menu_data
        except (DiningException, requests.exceptions.HTTPError, requests.exceptions.RequestException) as e:
            st.error(f"Could not load Purdue dining data: {e}")
        except Exception as f:
            st.error(f"Unexpected error: {f}")

    # Keep the builder list visible after checkboxes are selected
    builder_menu = st.session_state.builder_menu
    if builder_menu is not None:
        if builder_menu.empty:
            st.error("No items meet search criteria")
        else:
            _item_loader(builder_menu)
