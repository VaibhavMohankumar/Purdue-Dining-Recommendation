import data_loader as dl
import data_filterer as dfr
import recommendation_algorithm as ra
from datetime import datetime
import constants
from dining_exception import DiningException

dining_hall = input("Enter which dining hall you want to eat at:\nFord\nWiley\nWindsor\nEarhart\nHillenbrand\n").lower()
while dining_hall not in constants.DINING_HALLS:
    dining_hall = input("Invalid dining hall, choose again from the provided list\nFord\nWiley\nWindsor\nEarhart\nHillenbrand\n").lower()

meal_period = input("Use current meal period or custom?\nType NOW if current else choose:\nBreakfast\nLunch\nDinner\n").upper()
while meal_period not in constants.MEAL_OPTIONS and meal_period != "NOW":
    meal_period = input("Invalid meal period, choose again from the provided list").upper()
meal_period = None if meal_period == "NOW" else meal_period

try:
    menu_data = dl.get_json(dining_hall.capitalize(), datetime.now().date(), meal_period)
except DiningException as e:
    print(e)
    exit()
except Exception as f:
    print(f)
    print("Could not fetch and parse data")
    exit()
    
menu_data = dl.parse_data(menu_data)

dietary_filters = list(input("Enter your dietary restriction from the following list:\nVegetarian\nVegan\n"))
allergens = list(input("Enter allergens from the following list:station_name\nitem_name\nitem_id\nServing Size-value\nCalories-value\nCalories from fat-value\nTotal fat-value\nSaturated fat-value\nCholesterol-value\nSodium-value\nTotal Carbohydrate-value\nSugar-value\nAdded Sugar-value\nDietary Fiber-value\nProtein-value\nCalcium-value\nIron-value\nVegetarian-value\nVegan-value\n"))

menu_data = dfr.filter_dietary_restrictions(menu_data, dietary_filters, allergens)

max_cals = int(input("Enter max calories: "))
min_protein = int(input("Enter min protein: "))
max_carbs = int(input("Enter max carbs: "))
max_fat = int(input("Enter max fat: "))

menu_data = dfr.filter_nutrition_requirements(menu_data, max_cals, min_protein, max_carbs, max_fat)

cals = int(input("Enter desired calories: "))
protein = int(input("Enter desired protein: "))
carbs = int(input("Enter desired carbs: "))
fat = int(input("Enter desired fat: "))

menu_data = ra.recommend_item(menu_data, cals, protein, carbs, fat)
print("Recommendations: ")
print(menu_data[["item_name", "recommendation_reason"]])