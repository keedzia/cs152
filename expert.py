from pyswip import Prolog

class RestaurantExpert:
    def __init__(self):
        self.prolog = Prolog()
        self.prolog.consult("places.pl") # knowledge base
        self.remaining = self.get_all_places() # this will shrink as we ask questions
        
    def get_all_places(self):
        query = "restaurant(Name, _, _, _, _, _, _, _, _, _, _)"
        results = list(self.prolog.query(query))
        return [r['Name'] for r in results]
    
    # FILTERING FUNCTIONS (ASKABLES)
    def filter_by_type(self, place_type):
        # restaurant or bar
        filtered = []
        for place in self.remaining:
            query = f"matches_type('{place}', {place_type})"
            if list(self.prolog.query(query)):
                filtered.append(place)
        self.remaining = filtered
        
    def filter_by_budget(self, budget):
        # cheap, medium, expensive
        filtered = []
        for place in self.remaining:
            query = f"matches_budget('{place}', {budget})"
            if list(self.prolog.query(query)):
                filtered.append(place)
        self.remaining = filtered
    
    def filter_by_distance(self, max_dist):
        # distance in kilometers
        filtered = []
        for place in self.remaining:
            query = f"matches_distance('{place}', {max_dist})"
            if list(self.prolog.query(query)):
                filtered.append(place)
        self.remaining = filtered
    
    def filter_by_meal(self, meal_type):
        # breakfast, lunch, dinner, snack
        filtered = []
        for place in self.remaining:
            query = f"matches_meal('{place}', {meal_type})"
            if list(self.prolog.query(query)):
                filtered.append(place)
        self.remaining = filtered
    
    def filter_by_cuisine(self, cuisine):
        # indian, chinese, mexican, american, italian, etc.
        filtered = []
        for place in self.remaining:
            # handle cuisines with spaces
            if ' ' in cuisine:
                query = f"matches_cuisine('{place}', '{cuisine}')"
            else:
                query = f"matches_cuisine('{place}', {cuisine})"
            if list(self.prolog.query(query)):
                filtered.append(place)
        self.remaining = filtered
    
    def filter_by_vibe(self, vibe):
        # casual, formal, trendy, family_friendly, romantic, etc.
        filtered = []
        for place in self.remaining:
            query = f"matches_vibe('{place}', {vibe})"
            if list(self.prolog.query(query)):
                filtered.append(place)
        self.remaining = filtered
    
    def filter_by_reservations(self, needs_res):
        # yes or no
        filtered = []
        for place in self.remaining:
            query = f"matches_reservations('{place}', {needs_res})"
            if list(self.prolog.query(query)):
                filtered.append(place)
        self.remaining = filtered
    
    def filter_by_group_size(self, size):
        # solo, small group (2-5), large group (6+)
        filtered = []
        for place in self.remaining:
            query = f"matches_group_size('{place}', {size})"
            if list(self.prolog.query(query)):
                filtered.append(place)
        self.remaining = filtered
    
    def filter_by_wifi(self, needs_wifi):
        # yes or no (doesn't matter is handled by not filtering)
        filtered = []
        for place in self.remaining:
            query = f"matches_wifi('{place}', {needs_wifi})"
            if list(self.prolog.query(query)):
                filtered.append(place)
        self.remaining = filtered
    
    def filter_by_dietary(self, dietary):
        # any, vegetarian, vegan, gluten_free, halal
        filtered = []
        for place in self.remaining:
            query = f"matches_dietary('{place}', {dietary})"
            if list(self.prolog.query(query)):
                filtered.append(place)
        self.remaining = filtered
    
    # METHODS TO GET AVAILABLE OPTIONS
    def get_available_cuisines(self):
        # return list of cuisines in remaining places
        if not self.remaining:
            return []
        places_str = '[' + ','.join([f"'{p}'" for p in self.remaining]) + ']'
        query = f"get_cuisines({places_str}, Cuisines)"
        results = list(self.prolog.query(query))
        if results:
            return results[0]['Cuisines']
        return []
    
    def get_available_vibes(self):
        # return list of vibes in remaining places
        if not self.remaining:
            return []
        places_str = '[' + ','.join([f"'{p}'" for p in self.remaining]) + ']'
        query = f"get_vibes({places_str}, Vibes)"
        results = list(self.prolog.query(query))
        if results:
            return results[0]['Vibes']
        return []
    
    def get_available_meals(self):
        # return list of meal types in remaining places
        if not self.remaining:
            return []
        places_str = '[' + ','.join([f"'{p}'" for p in self.remaining]) + ']'
        query = f"get_meal_types({places_str}, Meals)"
        results = list(self.prolog.query(query))
        if results:
            return results[0]['Meals']
        return []
    
    def get_available_types(self):
        # return list of place types in remaining places
        if not self.remaining:
            return []
        places_str = '[' + ','.join([f"'{p}'" for p in self.remaining]) + ']'
        query = f"get_types({places_str}, Types)"
        results = list(self.prolog.query(query))
        if results:
            return results[0]['Types']
        return []
    
    def get_available_budgets(self):
        # return list of budgets in remaining places
        if not self.remaining:
            return []
        places_str = '[' + ','.join([f"'{p}'" for p in self.remaining]) + ']'
        query = f"get_budgets({places_str}, Budgets)"
        results = list(self.prolog.query(query))
        if results:
            return results[0]['Budgets']
        return []
    
    def get_distance_range(self):
        # get min and max distance from remaining places
        if not self.remaining:
            return None, None
        places_str = '[' + ','.join([f"'{p}'" for p in self.remaining]) + ']'
        
        max_query = f"get_max_distance({places_str}, MaxDist)"
        max_results = list(self.prolog.query(max_query))
        max_dist = max_results[0]['MaxDist'] if max_results else 0
        
        min_query = f"get_min_distance({places_str}, MinDist)"
        min_results = list(self.prolog.query(min_query))
        min_dist = min_results[0]['MinDist'] if min_results else 0
        
        return min_dist, max_dist
    
    def check_wifi_options(self):
        # returns tuple (has_wifi, has_no_wifi)
        if not self.remaining:
            return False, False
        places_str = '[' + ','.join([f"'{p}'" for p in self.remaining]) + ']'
        
        has_wifi = bool(list(self.prolog.query(f"has_wifi_available({places_str})")))
        has_no_wifi = bool(list(self.prolog.query(f"has_no_wifi_available({places_str})")))
        
        return has_wifi, has_no_wifi
    
    def check_reservation_options(self):
        # returns tuple (has_reservations, has_no_reservations)
        if not self.remaining:
            return False, False
        places_str = '[' + ','.join([f"'{p}'" for p in self.remaining]) + ']'
        
        has_res = bool(list(self.prolog.query(f"has_reservations_available({places_str})")))
        has_no_res = bool(list(self.prolog.query(f"has_no_reservations_available({places_str})")))
        
        return has_res, has_no_res
    
    def get_group_size_range(self):
        # returns (min_size, max_size)
        if not self.remaining:
            return None, None
        places_str = '[' + ','.join([f"'{p}'" for p in self.remaining]) + ']'
        
        max_query = f"get_max_group_size({places_str}, MaxSize)"
        max_results = list(self.prolog.query(max_query))
        max_size = max_results[0]['MaxSize'] if max_results else 0
        
        min_query = f"get_min_group_size({places_str}, MinSize)"
        min_results = list(self.prolog.query(min_query))
        min_size = min_results[0]['MinSize'] if min_results else 0
        
        return min_size, max_size
    
    def get_available_dietary(self):
        # return list of dietary options in remaining places
        if not self.remaining:
            return []
        places_str = '[' + ','.join([f"'{p}'" for p in self.remaining]) + ']'
        query = f"get_dietary_options({places_str}, Options)"
        results = list(self.prolog.query(query))
        if results:
            return results[0]['Options']
        return []


def ask_multiple_choice(prompt, options):
    # display prompt and options, not showing unavailable irrelevant choices for the askable
    print(f"\n{prompt}")
    for i, opt in enumerate(options, 1):
        print(f"  {i}. {opt}")
    
    while True:
        try:
            choice = input("choose (number): ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(options):
                return options[idx]
            print("invalid choice, try again")
        except ValueError:
            print("enter a number")


def run_expert_system():
   
    print("=== restaurant recommendation system ===")
    print("finding the perfect place near esmeralda 920...\n")
    
    expert = RestaurantExpert()

    # main loop
    while len(expert.remaining) > 1:
        print(f"\ncurrent matches: {len(expert.remaining)}")
        
        # ask type first if multiple types available
        available_types = expert.get_available_types()
        if len(available_types) > 1:
            place_type = ask_multiple_choice(
                "what type of place?",
                available_types
            )
            expert.filter_by_type(place_type)
            if len(expert.remaining) <= 1:
                break
        
        # ask about meal type
        available_meals = expert.get_available_meals()
        if len(available_meals) > 1:
            meal = ask_multiple_choice(
                "what meal?",
                available_meals
            )
            expert.filter_by_meal(meal)
            if len(expert.remaining) <= 1:
                break
        
        # ask about cuisine if multiple available
        available_cuisines = expert.get_available_cuisines()
        if len(available_cuisines) > 1:
            cuisine = ask_multiple_choice(
                "what cuisine?",
                available_cuisines
            )
            expert.filter_by_cuisine(cuisine)
            if len(expert.remaining) <= 1:
                break
        
        # ask about budget - only show available budgets
        if len(expert.remaining) > 1:
            available_budgets = expert.get_available_budgets()
            if len(available_budgets) > 1:
                budget = ask_multiple_choice(
                    "what's your budget?",
                    available_budgets
                )
                expert.filter_by_budget(budget)
                if len(expert.remaining) <= 1:
                    break
        
        # ask about distance - smart based on what's available
        if len(expert.remaining) > 1:
            min_dist, max_dist = expert.get_distance_range()
            
            # build options based on what's available
            options = []
            distance_map = {}
            
            if max_dist <= 2:
                options.append('short (0-2km)')
                distance_map['short (0-2km)'] = 2
            elif min_dist <= 2:
                options.append('short (0-2km)')
                distance_map['short (0-2km)'] = 2
                if max_dist <= 5:
                    options.append('medium (2-5km)')
                    distance_map['medium (2-5km)'] = 5
                else:
                    options.append('medium (2-5km)')
                    distance_map['medium (2-5km)'] = 5
                    options.append('long (>5km)')
                    distance_map['long (>5km)'] = 100
            else:  # all places are > 2km
                if max_dist <= 5:
                    options.append('medium (2-5km)')
                    distance_map['medium (2-5km)'] = 5
                else:
                    options.append('medium (2-5km)')
                    distance_map['medium (2-5km)'] = 5
                    options.append('long (>5km)')
                    distance_map['long (>5km)'] = 100
            
            if len(options) > 1:
                distance = ask_multiple_choice(
                    "max distance from esmeralda 920?",
                    options
                )
                expert.filter_by_distance(distance_map[distance])
                if len(expert.remaining) <= 1:
                    break
        
        # ask about vibe if multiple available
        available_vibes = expert.get_available_vibes()
        if len(available_vibes) > 1:
            vibe = ask_multiple_choice(
                "what vibe are you looking for?",
                available_vibes
            )
            expert.filter_by_vibe(vibe)
            if len(expert.remaining) <= 1:
                break
        
        # ask about wifi - smart handling
        if len(expert.remaining) > 1:
            has_wifi, has_no_wifi = expert.check_wifi_options()
            
            # only ask if there's a mix
            if has_wifi and has_no_wifi:
                wifi = ask_multiple_choice(
                    "is wifi important for you?",
                    ['yes', "doesn't matter"]
                )
                if wifi == 'yes':
                    expert.filter_by_wifi('yes')
                # if "doesn't matter", don't filter
                if len(expert.remaining) <= 1:
                    break
        
        # ask about reservations - smart handling
        if len(expert.remaining) > 1:
            has_res, has_no_res = expert.check_reservation_options()
            
            # only ask if there's a mix
            if has_res and has_no_res:
                reservations = ask_multiple_choice(
                    "do you need to make reservations?",
                    ['yes', "doesn't matter"]
                )
                if reservations == 'yes':
                    expert.filter_by_reservations('yes')
                # if "doesn't matter", don't filter
                if len(expert.remaining) <= 1:
                    break
        
        # ask about group size - smart based on ranges
        if len(expert.remaining) > 1:
            min_size, max_size = expert.get_group_size_range()
            
            # build options based on what's available
            options = []
            size_map = {}
            
            if max_size >= 1:
                options.append('solo')
                size_map['solo'] = 1
            if max_size >= 6:
                options.append('small (2-6)')
                size_map['small (2-6)'] = 6
            if max_size >= 7:
                options.append('big (7+)')
                size_map['big (7+)'] = 7
            
            if len(options) > 1:
                size = ask_multiple_choice(
                    "how many people?",
                    options
                )
                expert.filter_by_group_size(size_map[size])
                if len(expert.remaining) <= 1:
                    break
        
        # ask about dietary restrictions - only show available options
        if len(expert.remaining) > 1:
            available_dietary = expert.get_available_dietary()
            if available_dietary:
                # always include "any" option
                options = ['any'] + available_dietary
                dietary = ask_multiple_choice(
                    "any dietary restrictions?",
                    options
                )
                expert.filter_by_dietary(dietary)
                if len(expert.remaining) <= 1:
                    break
    
    # show results
    print("\n" + "="*40)
    if len(expert.remaining) == 0:
        print("sorry, no places match your criteria :(")
    elif len(expert.remaining) == 1:
        print(f"recommendation: {expert.remaining[0]}")
    else:
        print("remaining options:")
        for place in expert.remaining:
            print(f"  - {place}")


if __name__ == "__main__":
    run_expert_system()