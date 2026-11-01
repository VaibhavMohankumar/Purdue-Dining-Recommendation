"""
Utilities for retrieving Purdue dining menu data and selecting a meal period.
"""

import requests
from datetime import datetime, date
import pandas as pd
import constants
from dining_exception import DiningException


def get_meal_period(hour=None) -> str:
    """
    Return the Purdue dining meal period for a given hour.

    Args:
        hour: Hour of the day using the 24-hour clock. If None, the
            current local hour is used.

    Returns:
        "Breakfast" for hours before 10:00,
        "Lunch" for hours from 10:00 through 16:59,
        "Dinner" for hours from 17:00 onward.
    """
    if hour is None:
        hour = datetime.now().time().hour
    
    if (hour < 10):
        return "BREAKFAST"
    elif (hour < 14):
        return "LUNCH"
    else:
        return "DINNER"
    

def get_json(location: str, menu_date: date, meal_period=None, timeout: int=15):
    """
    Fetch a Purdue dining menu and return one meal period.

    Args:
        url: Base URL for the Purdue dining API.
        location: Purdue dining location.
        menu_date: Date of the menu to retrieve.
        meal_period: Meal to return, such as "Breakfast", "Lunch", or "Dinner".
        timeout: Maximum number of seconds to wait for the API response.

    Returns:
        A dictionary containing the requested meal period.

    Raises:
        requests.exceptions.RequestException: If the API request fails.
    """
    try:
        response = requests.post(
            constants.URL,
            json={
                "query": constants.QUERY,
                "variables": {"name": location, "date": str(menu_date)}
            },
            timeout=timeout
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise e
    
    if meal_period is None:
        meal_period = get_meal_period()
    
    data = response.json()
    
    for meal in data.get("data")["diningCourtByName"]["dailyMenu"]["meals"]:
        # Only return the requested meal period data
        if (meal.get("type") == meal_period.upper()):
            if (len(meal.get("stations")) == 0):
                raise DiningException("No Meal Served")
            return (meal.get("type"), meal.get("stations"))
        
    return response.json()


def parse_data(json_data) -> pd.DataFrame:
    """
    Convert nested meal, station, and item JSON data into a pandas DataFrame.

    The function loops through each station and menu item. If an item has
    components, each component is stored as its own row. Otherwise, the main
    item is stored directly.

    Args:
        json_data: List of station dictionaries containing menu items.

    Returns:
        A pandas DataFrame containing station names, item names, item IDs,
        nutrition values, and dietary/allergen traits.
    """
    
    rows = []
    
    for station in json_data:
        station_name = station.get("name")
        
        for item in station.get("items", []):
            name = item.get("displayName")
            
            inner_item = item.get("item", {})
            if not inner_item:
                continue
            
            if (inner_item.get("components")):
                
                for component_item in inner_item.get("components"):
                    
                    name = component_item.get("name")
                    item_id = component_item.get("itemId")
                    nutrition_info = component_item.get("nutritionFacts") or []
                    allergen_info = component_item.get("traits") or []
                    
                    rows.append(parse_info_to_row(station_name, name, item_id, nutrition_info, allergen_info))
            else:
                item_id = inner_item.get("itemId")
                nutrition_info = inner_item.get("nutritionFacts") or []
                allergen_info = inner_item.get("traits") or []

                rows.append(parse_info_to_row(station_name, name, item_id, nutrition_info, allergen_info))
        
    df = pd.DataFrame(rows)
    df.drop_duplicates("item_id")
    return df

def parse_info_to_row(station_name, name, item_id, nutrition_info, allergen_info):
    """
    Convert one menu item's information into a dictionary representing a row in a pandas DataFrame.

    Args:
        station_name: Name of the dining station.
        name: Name of the menu item.
        item_id: unique item ID.
        nutrition_info: List of nutrition dictionaries.
        allergen_info: List of dietary and/or allergen trait dictionaries.

    Returns:
        A dictionary representing an item as a row to be inserted into the pandas DataFrame.
    """
    
    row_data = {
        "station_name": station_name,
        "item_name": name,
        "item_id": item_id,
    }
    
    # Add nutrition facts formatted as "Name-value"
    for info in nutrition_info:
        if info and info.get("name"):
            col_name = f"{info.get("name")}-value"
            row_data[col_name] = info.get("label")

    # Add traits formatted as "Name-value"
    for info in allergen_info:
        if info and info.get("name"):
            col_name = f"{info.get("name")}-value"
            row_data[col_name] = info.get("type")
            
    return row_data