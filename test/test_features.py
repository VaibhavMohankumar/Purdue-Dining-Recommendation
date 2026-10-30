import diningrecommendation.data_loader as dl
from datetime import date

# Tests to ensure get_meal_period() returns correct meal period based on time of day
def test_breakfast_period():
    assert dl.get_meal_period(8) == "Breakfast"


def test_lunch_period():
    assert dl.get_meal_period(12) == "Lunch"


def test_dinner_period():
    assert dl.get_meal_period(18) == "Dinner"


# Tests to ensure get_json() correctly returns json according to meal period
def test_get_json_returns_correct_meal_period_given():
    result = dl.get_json(
        url=dl.URL,
        location="Wiley",
        menu_date=date(2026, 10, 29),
        meal_period="Lunch"
    )
    
    assert result["Name"] == "Lunch"
    
def test_get_json_returns_correct_meal_period_absent():
    result = dl.get_json(
        url=dl.URL,
        location="Wiley",
        menu_date=date(2026, 10, 29)
    )
    
    # Changes based on time
    meal_period = dl.get_meal_period()
        
    assert result["Name"] == meal_period