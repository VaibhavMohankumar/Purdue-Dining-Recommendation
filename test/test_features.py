import diningrecommendation.data_loader as dl
from datetime import date
import pytest
from diningrecommendation.dining_exception import DiningException

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
        

# Test to ensure json is parsed correctly with all neccessaru columns
def test_parse_data_returns_correct_df_columns():
    _, result = dl.get_json(
        location="Windsor",
        menu_date=date(2026, 11, 1),
        meal_period="LUNCH"
    )
    result = dl.parse_data(result)
    
    assert result.columns.tolist() == ["station_name", "item_name", "item_id", "Serving Size-value",
                            "Calories-value", "Calories from fat-value", "Total fat-value", "Saturated fat-value", "Cholesterol-value",
                            "Sodium-value", "Total Carbohydrate-value", "Sugar-value", "Added Sugar-value", "Dietary Fiber-value", 
                            "Protein-value", "Calcium-value", "Iron-value", "Eggs-value", "Gluten-value", "Milk-value", "Soy-value",
                            "Vegetarian-value", "Wheat-value", "Vegan-value", "Fish-value", "Peanuts-value", "Sesame-value", "Coconut-value"]