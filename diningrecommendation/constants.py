URL = "https://api.hfs.purdue.edu/menus/v3/GraphQL"
QUERY = """
query DiningCourtMenu($name: String!, $date: Date!) {
    diningCourtByName(name: $name) {
        name
        formalName

        dailyMenu(date: $date) {
            notes

            meals {
                type

                stations {
                    name

                    items {
                        displayName

                        item {
                            itemId

                            nutritionFacts {
                                name
                                value
                                label
                                dailyValueLabel
                            }

                            traits {
                                name
                                type
                            }

                            components {
                                itemId
                                name

                                nutritionFacts {
                                    name
                                    value
                                    label
                                    dailyValueLabel
                                }

                                traits {
                                    name
                                    type
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
"""
DINING_HALLS = ["Ford", "Wiley", "Windsor", "Earhart", "Hillenbrand"]
MEAL_OPTIONS = ["Now", "Breakfast", "Lunch", "Dinner"]
DIETARY_COLUMNS = ["None", "Vegetarian", "Vegan"]
ALLERGEN_COLUMNS = ["Gluten", "Sesame", "Soy", "Wheat", "Milk", "Eggs", "Coconut", "Fish", "Shellfish", "Peanuts", "Tree Nuts"]
NUTRITION_COLUMNS = ['Calories-value', 'Calories from fat-value', 'Total fat-value', 'Saturated fat-value', 'Cholesterol-value',
             'Sodium-value', 'Total Carbohydrate-value', 'Sugar-value', 'Added Sugar-value', 'Dietary Fiber-value',
             'Protein-value', 'Calcium-value', 'Iron-value']