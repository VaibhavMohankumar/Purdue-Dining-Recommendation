# Purdue-Dining-Recommendation

## Project Goal

- Help Purdue students find meals matching their dietary restrictions, allergies, preferences, and nutrition goals.
- Reduce the time spent searching through multiple dining menus.

## MVP Scope

- Fetch Purdue dining menu data.
- Temporarily store API data as JSON.
- Parse nutrition features into a pandas DataFrame.
- Filter unwanted dietary, allergen, calorie, protein, and sodium features.
- Rank compatible meals.
- Display recommendations and explanations.

## Future Plans

- Improve recommendation explanations
- Add nutrition visualizations
- Add scheduled fetcher for daily meal updates at dining halls based on a provided preference

## Tech Stack

- Python: programming language
- pandas: data storage and filtering
- NumPy: nutrition calculations
- scikit-learn `NearestNeighbors`: rank meal recommendations
- Streamlit: display results
- `requests` and JSON: fetch and temporarily store API data
- Git/GitHub: version control and documentation
