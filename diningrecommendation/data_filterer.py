"""
Filtering utilities for Purdue dining menu data.
"""

import pandas as pd

def filter_dietary_restrictions(df: pd.DataFrame, diet_restriction: str, allergens: list = []) -> pd.DataFrame:
    """
    Filter menu items according to dietary restrictions and allergens.

    Item rows are kept:
        For dietary restrictions: if the item satisifies the restriction.
        For allergens: if the item doesn't contain the allergen.

    Args:
        df: DataFrame containing parsed menu items.
        diet_restrictions: Dietary columns to require, such as
            "Vegetarian-value" or "Vegan-value".
        allergens: Allergen columns to exclude, such as "Milk-value"
            or "Peanuts-value".

    Returns:
        A filtered DataFrame containing only items that satisfy the
        requested dietary restrictions and do not contain selected allergens.
    """
    
    restriction_columns = {
        "gluten": "Gluten-value",
        "sesame": "Sesame-value",
        "soy": "Soy-value",
        "vegetarian": "Vegetarian-value",
        "vegan": "Vegan-value",
        "wheat": "Wheat-value",
        "milk": "Milk-value",
        "eggs": "Eggs-value",
        "coconut": "Coconut-value",
        "fish": "Fish-value",
        "shellfish": "Shellfish-value",
        "peanuts": "Peanuts-value",
        "tree nuts": "Tree Nuts-value",
    }
    
    not_allergen = [
        'station_name', 'item_name', 'item_id', 'Serving Size-value', 'Calories-value',
        'Calories from fat-value', 'Total fat-value', 'Saturated fat-value', 'Cholesterol-value',
        'Sodium-value', 'Total Carbohydrate-value', 'Sugar-value', 'Added Sugar-value', 'Dietary Fiber-value',
        'Protein-value', 'Calcium-value', 'Iron-value', "Vegetarian-value", "Vegan-value"
    ]
    
    dietary_columns = [
        "Vegetarian-value", "Vegan-value"
    ]
    
    if "None" in diet_restriction:
        diet_restriction = ""
        
    # Checking for matching values of diet restrictions and allergens since the streamlit interface
    # does not include the "-value" following the restriction or allergen name to ensure ease of readability
    if diet_restriction.lower() in restriction_columns.keys():
        diet_restriction = str(restriction_columns.get(diet_restriction.lower()))
        
    for i, allergen in enumerate(allergens):
        if allergen.lower() in restriction_columns.keys():
            allergens[i] = restriction_columns.get(allergen.lower())
    
    allergen_columns = [allergen for allergen in df.columns.to_list() if allergen not in not_allergen]
    
    # Only keeps rows that meet dietary restriction using a boolean mask
    for restriction in dietary_columns:
        if restriction in diet_restriction:
            df = df[~df[restriction].isna()]
    
    # Only keeps rows that avoid selected allergens using a boolean mask
    for allergen in allergen_columns:
        if allergen in allergens:
            df = df[df[allergen].isna()]
            
    return df