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
DINING_HALLS = ["ford", "wiley", "windsor", "earhart", "hillenbrand"]
MEAL_OPTIONS = ["BREAKFAST", "LUNCH", "DINNER"]
DIETARY_COLUMNS = ["Vegetarian-value", "Vegan-value"]
NOT_ALLERGEN = [
    'station_name', 'item_name', 'item_id', 'Serving Size-value', 'Calories-value',
    'Calories from fat-value', 'Total fat-value', 'Saturated fat-value', 'Cholesterol-value',
    'Sodium-value', 'Total Carbohydrate-value', 'Sugar-value', 'Added Sugar-value', 'Dietary Fiber-value',
    'Protein-value', 'Calcium-value', 'Iron-value', "Vegetarian-value", "Vegan-value"
]