from pyswip import Prolog

class RestaurantExpert:
    def __init__(self):
        self.prolog = Prolog()
        self.prolog.consult("restaurants.pl")
        # start with all places
        self.remaining = self.get_all_places()
        
    def get_all_places(self):
        """get all restaurant and bar names from knowledge base"""
        query = "restaurant(Name, _, _, _, _, _, _, _, _, _, _)"
        results = list(self.prolog.query(query))
        return [r['Name'] for r in results]
    
    def filter_by_type(self, place_type):
        """filter remaining places by type (restaurant or bar)"""
        filtered = []
        for place in self.remaining:
            query = f"matches_type('{place}', {place_type})"
            if list(self.prolog.query(query)):
                filtered.append(place)
        self.remaining = filtered
        
    def filter_by_budget(self, budget):
        """filter by budget compatibility"""
        filtered = []
        for place in self.remaining:
            query = f"matches_budget('{place}', {budget})"
            if list(self.prolog.query(query)):
                filtered.append(place)
        self.remaining = filtered
    
    def filter_by_distance(self, max_dist):
        """filter by max distance in blocks"""
        filtered = []
        for place in self.remaining:
            query = f"matches_distance('{place}', {max_dist})"
            if list(self.prolog.query(query)):
                filtered.append(place)
        self.remaining = filtered
    
    def filter_by_meal(self, meal_type):
        """filter by meal type"""
        filtered = []
        for place in self.remaining:
            query = f"matches_meal('{place}', {meal_type})"
            if list(self.prolog.query(query)):
                filtered.append(place)
        self.remaining = filtered
    
    def filter_by_cuisine(self, cuisine):
        """filter by cuisine type"""
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
        """filter by vibe/atmosphere"""
        filtered = []
        for place in self.remaining:
            query = f"matches_vibe('{place}', {vibe})"
            if list(self.prolog.query(query)):
                filtered.append(place)
        self.remaining = filtered
    
    def filter_by_reservations(self, needs_res):
        """filter by reservation requirements"""
        filtered = []
        for place in self.remaining:
            query = f"matches_reservations('{place}', {needs_res})"
            if list(self.prolog.query(query)):
                filtered.append(place)
        self.remaining = filtered
    
    def filter_by_group_size(self, size):
        """filter by group size capacity"""
        filtered = []
        for place in self.remaining:
            query = f"matches_group_size('{place}', {size})"
            if list(self.prolog.query(query)):
                filtered.append(place)
        self.remaining = filtered
    
    def filter_by_wifi(self, needs_wifi):
        """filter by wifi availability"""
        filtered = []
        for place in self.remaining:
            query = f"matches_wifi('{place}', {needs_wifi})"
            if list(self.prolog.query(query)):
                filtered.append(place)
        self.remaining = filtered
    
    def filter_by_dietary(self, dietary):
        """filter by dietary restrictions"""
        filtered = []
        for place in self.remaining:
            query = f"matches_dietary('{place}', {dietary})"
            if list(self.prolog.query(query)):
                filtered.append(place)
        self.remaining = filtered
    
    def get_available_cuisines(self):
        """get cuisines available in remaining places"""
        if not self.remaining:
            return []
        places_str = '[' + ','.join([f"'{p}'" for p in self.remaining]) + ']'
        query = f"get_cuisines({places_str}, Cuisines)"
        results = list(self.prolog.query(query))
        if results:
            return results[0]['Cuisines']
        return []
    
    def get_available_vibes(self):
        """get vibes available in remaining places"""
        if not self.remaining:
            return []
        places_str = '[' + ','.join([f"'{p}'" for p in self.remaining]) + ']'
        query = f"get_vibes({places_str}, Vibes)"
        results = list(self.prolog.query(query))
        if results:
            return results[0]['Vibes']
        return []
    
    def get_available_meals(self):
        """get meal types available in remaining places"""
        if not self.remaining:
            return []
        places_str = '[' + ','.join([f"'{p}'" for p in self.remaining]) + ']'
        query = f"get_meal_types({places_str}, Meals)"
        results = list(self.prolog.query(query))
        if results:
            return results[0]['Meals']
        return []
    
    def get_available_types(self):
        """get types (restaurant/bar) available in remaining places"""
        if not self.remaining:
            return []
        places_str = '[' + ','.join([f"'{p}'" for p in self.remaining]) + ']'
        query = f"get_types({places_str}, Types)"
        results = list(self.prolog.query(query))
        if results:
            return results[0]['Types']
        return []


def ask_multiple_choice(prompt, options):
    """helper to ask multiple choice questions"""
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
    """main function to run the recommendation system"""
    print("=== restaurant recommendation system ===")
    print("finding the perfect place near esmeralda 920...\n")
    
    expert = RestaurantExpert()
    
    # keep asking questions until we narrow it down
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
        
        # ask about budget
        if len(expert.remaining) > 1:
            budget = ask_multiple_choice(
                "what's your budget?",
                ['cheap', 'medium', 'expensive']
            )
            expert.filter_by_budget(budget)
            if len(expert.remaining) <= 1:
                break
        
        # ask about distance
        if len(expert.remaining) > 1:
            distance = ask_multiple_choice(
                "max distance from esmeralda 920? (blocks)",
                ['2', '4', '6', '10']
            )
            expert.filter_by_distance(int(distance))
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
        
        # ask about wifi
        if len(expert.remaining) > 1:
            wifi = ask_multiple_choice(
                "need wifi?",
                ['yes', 'no']
            )
            expert.filter_by_wifi(wifi)
            if len(expert.remaining) <= 1:
                break
        
        # ask about reservations
        if len(expert.remaining) > 1:
            reservations = ask_multiple_choice(
                "need to make reservations?",
                ['yes', 'no']
            )
            expert.filter_by_reservations(reservations)
            if len(expert.remaining) <= 1:
                break
        
        # ask about group size
        if len(expert.remaining) > 1:
            size = ask_multiple_choice(
                "how many people?",
                ['1-2', '3-6', '7-10', '11+']
            )
            # convert to number
            size_map = {'1-2': 2, '3-6': 6, '7-10': 10, '11+': 15}
            expert.filter_by_group_size(size_map[size])
            if len(expert.remaining) <= 1:
                break
        
        # if we still have multiple, ask about dietary restrictions
        if len(expert.remaining) > 1:
            dietary = ask_multiple_choice(
                "any dietary restrictions?",
                ['any', 'vegetarian', 'vegan', 'gluten_free', 'halal']
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