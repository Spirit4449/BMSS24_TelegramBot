def get_menu(day):
    if day == '23':
        message = """
Breakfast:
 - Burritos, Fruit Loops, Milk, Tea, Coffee

Lunch:
 - Kathi Rolls, French Fries, Soda

Snack:
 - Cheese Cubes, Ritz Crackers, Chips Ahoy Cookies, Tea, Cold Coffee

Dinner
- Chili, Cheese, Sour Cream, Cornbread, Salad with Dressing, Frito Chips, Fruit Punch/Lemondae

Dessert
 - Brownie Sundae
"""

    elif day == '24':
        message = """
Breakfast:
 - Crossiants, Cocoa Puffs, Milk, Bataka Pao, Tea, Coffee

Lunch:
 - Loaded Nachos (Black Beans, Melted Cheese, Lettuce, Tomato, Jalapenos), Salsa, Sour Cream, Mexican Rice, Soda

Snack:
 - Watermelon, Grapes, Skinny Popcorn, Tea, Cold Coffee

Dinner:
 - OUTDOOR DINNER
   - Station 1: Paneer Tikka with Cilantro Chutney (Tandoor Style)
   - Station 2: Falafel, Pita Chips and Hummus
   - Station 3: Spring Rolls, Samosa, Sauce
   - Station 4: Pani Puri
   - Soda/Lemonades Station: Soda, Fresh Lemonade
   - Dessert Station: Cheesecake Mini and Oreo Truffles

Dessert:
 - Mini Cheesecake and Oreo Truffles
"""
    elif day == '25':
        message = """
Breakfast:
 - Hashbrown with Ketchup, Handvo, Fruit Loops, Milk, Tea, Coffee

Lunch:
 - Pasta Bake, Red Sauce, Bread, Capri Sun
 - To-Go for Kishore Mandal: Pasta Salad, Lays Chips, Water Bottles, Individual Packs of Cookies

Snack:
 - Chips Ahoy, Cheese Its, Nature Valley Chewy Bars, Cold Coffee

Dinner:
 - Burritos (Pre-Made), Salsa, Sour Cream, Tortilla Chips, Guacamole

Dessert:
 - Cookie Ice Cream Sandwich
"""
    elif day == '26':
        message = """
Breakfast:
 - Breakfast Burritos (Tofu Scrambled, Cheese, Shredded Potato, Black Beans), Fruit Loops, Milk, Tea, Coffee

Lunch:
 - Kathi Rolls, French Fries, Soda/Lemonade

Snack:
 - Cheese Cubes, Ritz Crackers, Chips Ahoy Cookies, Tea, Cold Coffee

Dinner:
 - Chili, Cheese, Sour Cream, Cornbread, Salad with Dressing, Frito Chips, Fruit Punch

Dessert:
 - Brownie Sundaes
"""
    elif day == '27':
        message = """
Breakfast:
 - Crossiants, Cocoa Puffs, Milk, Bataka Pao, Tea, Coffee

Lunch:
 - Loaded Nachos (Black Beans, Melted Cheese, Lettuce, Tomato, Jalapenos), Salsa, Sour Cream, Mexican Rice, Soda

Snack:
 - Watermelon, Grapes, Skinny Popcorn, Tea, Cold Coffee

Dinner:
 - OUTDOOR DINNER
   - Station 1: Paneer Tikka with Cilantro Chutney (Tandoor Style)
   - Station 2: Falafel, Pita Chips and Hummus
   - Station 3: Spring Rolls, Samosa, Sauce
   - Station 4: Pani Puri
   - Soda/Lemonades Station: Soda, Fresh Lemonade
   - Dessert Station: Cheesecake Mini and Oreo Truffles

Dessert:
 - Mini Cheesecake and Oreo Truffles
"""
    elif day == '28':
        message = """
Breakfast:
 - Cheese Covered Hashbrown with Ketchup, Handvo, Fruit Loops, Milk, Tea, Coffee

Lunch:
 - Pasta Salad To-Go, Lays Chips, Granola Bar, Water Bottles, Soda/Lemonade

Snack:
 - Hotel Snacks: Cheese Its, Lays Chips, Oreos, Fruit Snacks, Pretzels

Dinner:
 - Soda/Lemonades Station: Work with coke to get coolers and fill with Soda/Lemonades for each meal

Dessert:
 - Order Snacks: Hotel
"""
    else:
        message = "No menu available for this day."


    return message