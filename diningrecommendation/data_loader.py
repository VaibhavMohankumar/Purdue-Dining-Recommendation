"""
Utilities for retrieving Purdue dining menu data and selecting a meal period.
"""

import requests
from datetime import datetime, date

URL = "https://api.hfs.purdue.edu/menus/v2"

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
        return "Breakfast"
    elif (hour < 14):
        return "Lunch"
    else:
        return "Dinner"
    

def get_json(url: str, location: str, menu_date: date, meal_period=None, timeout: int=15):
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
        response = requests.get(
            url=(f"{url}/locations/{location}/{menu_date.isoformat()}"),
            timeout=timeout
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise e
    
    if meal_period is None:
        meal_period = get_meal_period()
    
    data = response.json()
    
    for meal in data.get("Meals", []):
        if meal.get("Name") == meal_period:
            return meal
    return response.json()