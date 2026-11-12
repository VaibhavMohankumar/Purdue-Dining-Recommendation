"""
Meal recommendation utility.
"""

import warnings
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors

def recommend_item(df: pd.DataFrame, calories=None, protein=None, carbs=None, fat=None, limit=5):
    """
    Recommend menu items based on user nutrition preferences.

    The function selects the nutrition values provided by the user, converts
    the corresponding DataFrame columns into numeric values, scales the
    features, and uses NearestNeighbors to find the closest meals.

    Args:
        df: DataFrame containing menu items and nutrition columns.
        calories: Preferred calorie amount.
        protein: Preferred protein amount in grams.
        carbs: Preferred carbohydrate amount in grams.
        fat: Preferred fat amount in grams.
        limit: Maximum number of recommendations to return.

    Returns:
        A DataFrame containing the recommended menu items, their distances
        from the user's target, and an explanation for each recommendation.
    """
    
    user_preferences = {}
    if calories is not None:
        user_preferences["Calories-value"] = calories
    if protein is not None:
        user_preferences["Protein-value"] = protein
    if carbs is not None:
        user_preferences["Total Carbohydrate-value"] = carbs
    if fat is not None:
        user_preferences["Total fat-value"] = fat

    
    df = _extract_nutrition_values(df, list(user_preferences.keys()))
            
    scaler = StandardScaler()
    
    warnings.filterwarnings("ignore", category=UserWarning)
    X = scaler.fit_transform(df[list(user_preferences.keys())])
    
    user_target = scaler.transform([list(user_preferences.values())])

    model = NearestNeighbors(n_neighbors=min(limit, len(df)))
    model.fit(X)

    distances, indexes = model.kneighbors(user_target)

    recommendations = df.iloc[indexes[0]].copy()
    recommendations["distance"] = distances[0]
    recommendations["recommendation_reason"] = recommendations.apply(
        lambda row: f"Closest nutrition match: {row['Calories-value']:.0f} calories, {row['Protein-value']:.0f}g protein, {row['Total Carbohydrate-value']:.0f}g carbs, and {row['Total fat-value']:.0f}g fat."
        if pd.notna(row["Protein-value"]) and pd.notna(row["Calories-value"]) and pd.notna(row["Total Carbohydrate-value"]) and pd.notna(row["Total fat-value"])
        else "Matches your filters; some nutrition data is unavailable", axis=1
    )
            
    return recommendations

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