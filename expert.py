from pyswip import Prolog
import os

class RestaurantExpert:
    def __init__(self):
        self.prolog = Prolog()
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        places_path = os.path.join(script_dir, "places.pl")
        
        self.prolog.consult(places_path)
        self.remaining = self.get_all_places()
        
    def get_all_places(self):
        query = "restaurant(Name, _, _, _, _, _, _, _, _, _, _)"
        results = list(self.prolog.query(query))
        return [r['Name'] for r in results]
    
    # FILTERING FUNCTIONS (ASKABLES)
    def filter_by_type(self, place_type):
        filtered = []
        for place in self.remaining:
            query = f"matches_type('{place}', {place_type})"
            if list(self.prolog.query(query)):
                filtered.append(place)
        self.remaining = filtered
        
    def filter_by_budget(self, budget):
        filtered = []
        for place in self.remaining:
            query = f"matches_budget('{place}', {budget})"
            if list(self.prolog.query(query)):
                filtered.append(place)
        self.remaining = filtered
    
    def filter_by_distance(self, max_dist):
        filtered = []
        for place in self.remaining:
            query = f"matches_distance('{place}', {max_dist})"
            if list(self.prolog.query(query)):
                filtered.append(place)
        self.remaining = filtered
    
    def filter_by_meal(self, meal_type):
        filtered = []
        for place in self.remaining:
            query = f"matches_meal('{place}', {meal_type})"
            if list(self.prolog.query(query)):
                filtered.append(place)
        self.remaining = filtered
    
    def filter_by_cuisine(self, cuisine):
        filtered = []
        for place in self.remaining:
            query = f"matches_cuisine('{place}', {cuisine})"
            if list(self.prolog.query(query)):
                filtered.append(place)
        self.remaining = filtered
    
    def filter_by_vibe(self, vibe):
        filtered = []
        for place in self.remaining:
            query = f"matches_vibe('{place}', {vibe})"
            if list(self.prolog.query(query)):
                filtered.append(place)
        self.remaining = filtered
    
    def filter_by_reservations(self, needs_res):
        filtered = []
        for place in self.remaining:
            query = f"matches_reservations('{place}', {needs_res})"
            if list(self.prolog.query(query)):
                filtered.append(place)
        self.remaining = filtered
    
    def filter_by_group_size(self, size):
        filtered = []
        for place in self.remaining:
            query = f"matches_group_size('{place}', {size})"
            if list(self.prolog.query(query)):
                filtered.append(place)
        self.remaining = filtered
    
    def filter_by_wifi(self, needs_wifi):
        filtered = []
        for place in self.remaining:
            query = f"matches_wifi('{place}', {needs_wifi})"
            if list(self.prolog.query(query)):
                filtered.append(place)
        self.remaining = filtered
    
    def filter_by_dietary(self, dietary):
        filtered = []
        for place in self.remaining:
            query = f"matches_dietary('{place}', {dietary})"
            if list(self.prolog.query(query)):
                filtered.append(place)
        self.remaining = filtered
    
    # METHODS TO GET AVAILABLE OPTIONS
    def get_available_cuisines(self):
        if not self.remaining:
            return []
        places_str = '[' + ','.join([f"'{p}'" for p in self.remaining]) + ']'
        query = f"get_cuisines({places_str}, Cuisines)"
        results = list(self.prolog.query(query))
        if results:
            cuisines = results[0]['Cuisines']
            # remove duplicates while preserving order
            seen = set()
            unique_cuisines = []
            for c in cuisines:
                if c not in seen:
                    seen.add(c)
                    unique_cuisines.append(c)
            return unique_cuisines
        return []
    
    def get_available_vibes(self):
        if not self.remaining:
            return []
        places_str = '[' + ','.join([f"'{p}'" for p in self.remaining]) + ']'
        query = f"get_vibes({places_str}, Vibes)"
        results = list(self.prolog.query(query))
        if results:
            return results[0]['Vibes']
        return []
    
    def get_available_meals(self):
        if not self.remaining:
            return []
        places_str = '[' + ','.join([f"'{p}'" for p in self.remaining]) + ']'
        query = f"get_meal_types({places_str}, Meals)"
        results = list(self.prolog.query(query))
        if results:
            return results[0]['Meals']
        return []
    
    def get_available_types(self):
        if not self.remaining:
            return []
        places_str = '[' + ','.join([f"'{p}'" for p in self.remaining]) + ']'
        query = f"get_types({places_str}, Types)"
        results = list(self.prolog.query(query))
        if results:
            return results[0]['Types']
        return []
    
    def get_available_budgets(self):
        if not self.remaining:
            return []
        places_str = '[' + ','.join([f"'{p}'" for p in self.remaining]) + ']'
        query = f"get_budgets({places_str}, Budgets)"
        results = list(self.prolog.query(query))
        if results:
            return results[0]['Budgets']
        return []
    
    def get_distance_range(self):
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
        if not self.remaining:
            return False, False
        places_str = '[' + ','.join([f"'{p}'" for p in self.remaining]) + ']'
        
        has_wifi = bool(list(self.prolog.query(f"has_wifi_available({places_str})")))
        has_no_wifi = bool(list(self.prolog.query(f"has_no_wifi_available({places_str})")))
        
        return has_wifi, has_no_wifi
    
    def check_reservation_options(self):
        if not self.remaining:
            return False, False
        places_str = '[' + ','.join([f"'{p}'" for p in self.remaining]) + ']'
        
        has_res = bool(list(self.prolog.query(f"has_reservations_available({places_str})")))
        has_no_res = bool(list(self.prolog.query(f"has_no_reservations_available({places_str})")))
        
        return has_res, has_no_res
    
    def get_group_size_range(self):
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
        if not self.remaining:
            return []
        places_str = '[' + ','.join([f"'{p}'" for p in self.remaining]) + ']'
        query = f"get_dietary_options({places_str}, Options)"
        results = list(self.prolog.query(query))
        if results:
            return results[0]['Options']
        return []


def ask_multiple_choice(prompt, options):
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
    print(f"\ncurrent matches: {len(expert.remaining)}")
    
    # Q1: type
    if len(expert.remaining) > 1:
        available_types = expert.get_available_types()
        if len(available_types) > 1:
            place_type = ask_multiple_choice(
                "what type of place?",
                available_types
            )
            expert.filter_by_type(place_type)
            print(f"current matches: {len(expert.remaining)}")
            if len(expert.remaining) <= 1:
                show_results(expert)
                return
    
    # Q2: wifi (SECOND QUESTION)
    if len(expert.remaining) > 1:
        has_wifi, has_no_wifi = expert.check_wifi_options()
        if has_wifi and has_no_wifi:
            wifi = ask_multiple_choice(
                "is wifi important for you?",
                ['yes', "doesn't matter"]
            )
            if wifi == 'yes':
                expert.filter_by_wifi('yes')
                print(f"current matches: {len(expert.remaining)}")
                if len(expert.remaining) <= 1:
                    show_results(expert)
                    return
    
    # Q3: meal
    if len(expert.remaining) > 1:
        available_meals = expert.get_available_meals()
        if len(available_meals) > 1:
            meal = ask_multiple_choice(
                "what meal?",
                available_meals
            )
            expert.filter_by_meal(meal)
            print(f"current matches: {len(expert.remaining)}")
            if len(expert.remaining) <= 1:
                show_results(expert)
                return
    
    # Q4: cuisine
    if len(expert.remaining) > 1:
        available_cuisines = expert.get_available_cuisines()
        if len(available_cuisines) > 1:
            cuisine = ask_multiple_choice(
                "what cuisine?",
                available_cuisines
            )
            expert.filter_by_cuisine(cuisine)
            print(f"current matches: {len(expert.remaining)}")
            if len(expert.remaining) <= 1:
                show_results(expert)
                return
    
    # Q5: budget
    if len(expert.remaining) > 1:
        available_budgets = expert.get_available_budgets()
        if len(available_budgets) > 1:
            budget = ask_multiple_choice(
                "what's your budget?",
                available_budgets
            )
            expert.filter_by_budget(budget)
            print(f"current matches: {len(expert.remaining)}")
            if len(expert.remaining) <= 1:
                show_results(expert)
                return
    
    # Q6: distance
    if len(expert.remaining) > 1:
        min_dist, max_dist = expert.get_distance_range()
        
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
        else:
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
            print(f"current matches: {len(expert.remaining)}")
            if len(expert.remaining) <= 1:
                show_results(expert)
                return
    
    # Q7: vibe
    if len(expert.remaining) > 1:
        available_vibes = expert.get_available_vibes()
        if len(available_vibes) > 1:
            vibe = ask_multiple_choice(
                "what vibe are you looking for?",
                available_vibes
            )
            expert.filter_by_vibe(vibe)
            print(f"current matches: {len(expert.remaining)}")
            if len(expert.remaining) <= 1:
                show_results(expert)
                return
    
    # Q8: reservations
    if len(expert.remaining) > 1:
        has_res, has_no_res = expert.check_reservation_options()
        if has_res and has_no_res:
            reservations = ask_multiple_choice(
                "do you need to make reservations?",
                ['yes', "doesn't matter"]
            )
            if reservations == 'yes':
                expert.filter_by_reservations('yes')
                print(f"current matches: {len(expert.remaining)}")
                if len(expert.remaining) <= 1:
                    show_results(expert)
                    return
    
    # Q9: group size
    if len(expert.remaining) > 1:
        min_size, max_size = expert.get_group_size_range()
        
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
            print(f"current matches: {len(expert.remaining)}")
            if len(expert.remaining) <= 1:
                show_results(expert)
                return
    
    # Q10: dietary
    if len(expert.remaining) > 1:
        available_dietary = expert.get_available_dietary()
        if available_dietary:
            options = ['any'] + available_dietary
            dietary = ask_multiple_choice(
                "any dietary restrictions?",
                options
            )
            expert.filter_by_dietary(dietary)
            print(f"current matches: {len(expert.remaining)}")
            if len(expert.remaining) <= 1:
                show_results(expert)
                return
    
    show_results(expert)


def show_results(expert):
    print("\n" + "="*40)
    if len(expert.remaining) == 0:
        print("sorry, no places match your criteria :(")
    elif len(expert.remaining) == 1:
        print(f"recommendation: {expert.remaining[0]}")
    else:
        print(f"here are your {len(expert.remaining)} options:")
        for place in expert.remaining:
            print(f"  - {place}")


if __name__ == "__main__":
    run_expert_system()