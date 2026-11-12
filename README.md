# Purdue Dining Recommendation

A Streamlit application that recommends Purdue dining menu items based on nutrition goals, dietary restrictions, and allergens.

## The Problem

Purdue students may have difficulty finding dining options that match their dietary restrictions, allergies, and nutrition goals. Searching through multiple dining menus and nutrition labels can be time-consuming.

This project helps students find menu items that meet their requirements with the click of a button.

## How It Works

1. The user selects a dining hall, date, and meal period.
2. The user enters their preferred nutrition goals and dietary/allergen information.
3. The application fetches menu data from the Purdue Dining API.
4. The API response is parsed into a pandas DataFrame.
5. Items that violate dietary, allergen, or nutrition requirements are removed.
6. Nutrition features are standardized.
7. `NearestNeighbors` ranks the remaining items based on the user’s nutrition preferences.
8. Streamlit displays the recommended items and explains each match alongisde displaying dietary/allergen information.

\
![System Diagram](System%20Diagram.png)

## Tech Stack

- Python — programming language
- pandas — DataFrame storage and filtering
- requests — API requests
- JSON — temporary API data format
- scikit-learn — `StandardScaler` and `NearestNeighbors`
- Streamlit — user interface
- pytest — testing
- Git/GitHub — version control and documentation
- Purdue Dining API — menu, nutrition, dietary, and allergen data

## Setup and Installation

### Prerequisites

This project requires:

- Python 3.10 or newer
- `pip`
- Internet access for Purdue Dining API requests

Check whether Python and pip are installed:

```bash
python3 --version
python3 -m pip --version
```

If these commands do not work, install Python from:

https://www.python.org/downloads/

pip is included with most modern Python installations.

### 1. Clone the Repository

```bash
git clone <https://github.com/VaibhavMohankumar/Purdue-Dining-Recommendation.git>
cd Purdue-Dining-Recommendation
```

### 2. Create a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install requirements.txt
```

### 4. Run the Application

```bash
cd diningrecommendation
streamlit run app.py
```

### 5. Run the Tests

```bash
# Enter directory if not already in the directory: Purdue-Dining-Recommendation/diningrecommendation
cd diningrecommendation 
python -m pytest
```

## Example

### Example Input

```text
Dining location: Wiley
Menu date: 2026-11-12
Meal period: Lunch
Dietary restriction: Vegetarian
Allergens: Gluten
Desired calories: 400
Desired protein: 20g
Desired carbohydrates: 20g
Desired fat: 30g
Number of recommendations: 5
```

### Example Output

```text
Paneer Curry
Gluten Friendly

Closest nutrition match:
521 calories, 22g protein, 6g carbs, and 47g fat.

Meets dietary restrictions for: Vegetarian
Contains: Milk
```

The exact menu items and recommendations change because the application uses live data from Purdue Dining API data.

## Roadmap

- [x] Define the project problem and MVP scope
- [x] Create the project README
- [x] Create the system diagram
- [x] Connect to the Purdue Dining API
- [x] Parse nested meal, station, and item data
- [x] Store parsed data in a pandas DataFrame
- [x] Convert nutrition values into numeric values
- [x] Filter items by nutrition requirements
- [x] Filter items by dietary restrictions
- [x] Filter items by allergens
- [x] Implement the `NearestNeighbors` recommendation algorithm
- [x] Build the Streamlit interface
- [x] Add tests for major functions
- [ ] Add custom meals made from multiple station items
- [ ] Add nutrition visualizations
- [ ] Add scheduled fetcher for daily meal update
- [ ] Add user feedback to improve recommendations


## Demo

[Watch the project walkthrough](<link>)

The walkthrough demonstrates:

- Selecting a dining hall and meal period
- Entering nutrition preferences
- Selecting dietary restrictions and allergens
- Fetching current menu data
- Filtering menu items
- Viewing ranked recommendations
