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

def test_live_dietary_filter(menu_dataframe):
    result = dfr.filter_dietary_restrictions(
        menu_dataframe,
        diet_restriction="Vegetarian-value",
        allergens=["Milk-value"],
    )

    assert result["Vegetarian-value"].notna().all()
    assert result["Milk-value"].isna().all()