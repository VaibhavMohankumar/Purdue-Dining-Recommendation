import diningrecommendation.data_loader as dl
import diningrecommendation.data_filterer as dfr
from datetime import date, datetime
import pytest

# Tests to ensure get_meal_period() returns correct meal period based on time of day
def test_breakfast_period():
    assert dl.get_meal_period(8) == "BREAKFAST"


def test_lunch_period():
    assert dl.get_meal_period(12) == "LUNCH"


def test_dinner_period():
    assert dl.get_meal_period(18) == "DINNER"


# Tests to ensure get_json() correctly returns json according to meal period
def test_get_json_returns_correct_meal_period_given():
    meal, _ = dl.get_json(
        location="Wiley",
        menu_date=date(2026, 10, 29),
        meal_period="LUNCH"
    )
    
    assert meal == "LUNCH"
    
def test_get_json_returns_correct_meal_period_absent():
    meal, _ = dl.get_json(
        location="Wiley",
        menu_date=date(2026, 10, 29)
    )
    
    # Changes based on time
    meal_period = dl.get_meal_period()
        
    assert meal == meal_period
    

# Test to ensure DiningException is raised when no meal is served for that meal period    
def test_get_json_returns_DiningException():
    with pytest.raises(Exception) as exc:
        dl.get_json(
            location="Wiley",
            menu_date=date(2026, 11, 1),
            meal_period="LUNCH"
        )
        
        assert exc.typename == "DiningException"
        
# Fixture runs to get API data once before tests that require the data run
@pytest.fixture
def menu_dataframe():
    data = dl.get_json(
        location="Ford",
        menu_date=datetime.now().date(),
    )

    df = dl.parse_data(data)

    if df.empty:
        pytest.skip("No menu data available today")

    return df


# 4 Tests to ensure nutrition filtering return filtered menu items
def test_max_calories(menu_dataframe):
    max_calories = 500

    result = dfr.filter_nutrition_requirements(
        menu_dataframe,
        max_cals=max_calories,
    )

    assert (result["Calories-value"] <= max_calories).all()


def test_minimum_protein(menu_dataframe):
    minimum_protein = 10

    result = dfr.filter_nutrition_requirements(
        menu_dataframe,
        min_protein=minimum_protein,
    )

    assert (result["Protein-value"] >= minimum_protein).all()


def test_maximum_carbohydrates(menu_dataframe):
    maximum_carbs = 60

    result = dfr.filter_nutrition_requirements(
        menu_dataframe,
        max_carbs=maximum_carbs,
    )

    assert (result["Total Carbohydrate-value"] <= maximum_carbs).all()


def test_maximum_fat(menu_dataframe):
    maximum_fat = 25

    result = dfr.filter_nutrition_requirements(
        menu_dataframe,
        max_fat=maximum_fat,
    )

    assert (result["Total fat-value"] <= maximum_fat).all()
    

# 2 Tests to ensure diet and allergen requirements/restrictions are filtered
def test_live_nutrition_filter(menu_dataframe):
    result = dfr.filter_nutrition_requirements(
        menu_dataframe,
        max_cals=500,
        min_protein=10,
        max_carbs=60,
        max_fat=25,
    )

    assert (result["Calories-value"] <= 500).all()
    assert (result["Protein-value"] >= 10).all()
    assert (result["Total Carbohydrate-value"] <= 60).all()
    assert (result["Total fat-value"] <= 25).all()


def test_live_dietary_filter(menu_dataframe):
    result = dfr.filter_dietary_restrictions(
        menu_dataframe,
        diet_restrictions=["Vegetarian-value"],
        allergens=["Milk-value"],
    )

    assert result["Vegetarian-value"].notna().all()
    assert result["Milk-value"].isna().all()