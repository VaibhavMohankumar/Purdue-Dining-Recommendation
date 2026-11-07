"""
Filtering utilities for Purdue dining menu data.
"""

import pandas as pd
import constants

def filter_nutrition_requirements(df: pd.DataFrame, max_cals: int=0, min_protein: int=0, max_carbs: int=0, max_fat: int=0) -> pd.DataFrame:
    """
    Filter menu items according to nutritional requirements entered by user.

    Args:
        df: DataFrame containing parsed menu items.
        max_cals: Maximum allowed calories. A value of 0 means no limit.
        min_protein: Minimum required protein. A value of 0 means no minimum.
        max_carbs: Maximum allowed carbohydrates. A value of 0 means no limit.
        max_fat: Maximum allowed total fat. A value of 0 means no limit.

    Returns:
        A filtered DataFrame containing only items that meet the
        specified nutrition requirements.
    """
    
    nutrition_columns = [
        "Calories-value",
        "Protein-value",
        "Total Carbohydrate-value",
        "Total fat-value",
    ]
    
    df = _extract_nutrition_values(df, nutrition_columns)
    
    if (max_cals != 0):
        df = df[(df["Calories-value"] <= max_cals)]
        
    if (min_protein != 0):
        df = df[(df["Protein-value"] >= min_protein)]
        
    if (max_carbs != 0):
        df = df[(df["Total Carbohydrate-value"] <= max_carbs)]
            
    if (max_fat != 0):
        df = df[(df["Total fat-value"] <= max_fat)]
        
    return df

def filter_dietary_restrictions(df: pd.DataFrame, diet_restrictions: list = [], allergens: list = []) -> pd.DataFrame:
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
    
    allergen_columns = [allergen for allergen in df.columns.to_list() if allergen not in constants.NOT_ALLERGEN]
    
    for restriction in constants.DIETARY_COLUMNS:
        if restriction in diet_restrictions:
            df = df[~df[restriction].isna()]
    
    for allergen in allergen_columns:
        if allergen in allergens:
            df = df[df[allergen].isna()]
            
    return df

def _extract_nutrition_values(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Extract numeric nutrition values from DataFrame columns.

    Nutrition values may contain units or text, and this function extracts
    the first numeric value and stores it.

    Args:
        df: DataFrame containing nutrition columns.
        columns: List of nutrition column names to convert.

    Returns:
        The DataFrame with the selected nutrition columns converted
        to numeric values.
    """
    for column in columns:
            df[column] = (
                df[column]
                .astype(str)
                .str.extract(r"(\d+\.?\d*)")[0]
            )
            df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0)
            
    return df