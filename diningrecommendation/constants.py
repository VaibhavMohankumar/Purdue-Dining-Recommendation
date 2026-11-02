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