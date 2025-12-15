% knowledge base for restaurants and bars near esmeralda 920

% restaurant(name, type, cuisine, budget, distance_blocks, meal_types, vibe, takes_reservations, max_group_size, has_wifi, dietary_options)

% restaurants
restaurant('la mezquita', restaurant, 'comida arabe', cheap, 3, [breakfast, lunch, dinner], casual, no, 8, yes, [vegetarian, vegan]).
restaurant('taco express', restaurant, mexican, cheap, 2, [lunch, dinner, snack], casual, no, 6, no, [vegetarian]).
restaurant('el griego', restaurant, greek, medium, 5, [breakfast, brunch, lunch, dinner], relaxed, yes, 12, yes, [vegetarian, vegan, gluten_free]).
restaurant('istanbul cafe', restaurant, turkish, medium, 4, [breakfast, brunch, lunch], cozy, no, 10, yes, [vegetarian, halal]).
restaurant('pasta palazzo', restaurant, italian, expensive, 7, [lunch, dinner], upscale, yes, 20, yes, [vegetarian, gluten_free]).
restaurant('sushi spot', restaurant, japanese, expensive, 6, [lunch, dinner], modern, yes, 8, yes, [gluten_free]).

% bars
restaurant('cerveza y mas', bar, mexican, cheap, 3, [snack, dinner], lively, no, 15, no, [vegetarian]).
restaurant('wine corner', bar, international, expensive, 8, [snack], sophisticated, yes, 10, yes, [vegetarian, vegan, gluten_free]).
restaurant('local pub', bar, american, medium, 2, [lunch, dinner, snack], casual, no, 20, yes, [vegetarian]).

% helper predicates
matches_budget(Place, Budget) :-
    restaurant(Place, _, _, PlaceBudget, _, _, _, _, _, _, _),
    budget_compatible(Budget, PlaceBudget).

budget_compatible(cheap, cheap).
budget_compatible(medium, cheap).
budget_compatible(medium, medium).
budget_compatible(expensive, cheap).
budget_compatible(expensive, medium).
budget_compatible(expensive, expensive).

matches_distance(Place, MaxDist) :-
    restaurant(Place, _, _, _, Dist, _, _, _, _, _, _),
    Dist =< MaxDist.

matches_meal(Place, Meal) :-
    restaurant(Place, _, _, _, _, Meals, _, _, _, _, _),
    member(Meal, Meals).

matches_cuisine(Place, Cuisine) :-
    restaurant(Place, _, Cuisine, _, _, _, _, _, _, _, _).

matches_vibe(Place, Vibe) :-
    restaurant(Place, _, _, _, _, _, Vibe, _, _, _, _).

matches_reservations(Place, NeedsRes) :-
    restaurant(Place, _, _, _, _, _, _, TakesRes, _, _, _),
    (NeedsRes = yes -> TakesRes = yes ; true).

matches_group_size(Place, Size) :-
    restaurant(Place, _, _, _, _, _, _, _, MaxSize, _, _),
    Size =< MaxSize.

matches_wifi(Place, NeedsWifi) :-
    restaurant(Place, _, _, _, _, _, _, _, _, HasWifi, _),
    (NeedsWifi = yes -> HasWifi = yes ; true).

matches_type(Place, Type) :-
    restaurant(Place, Type, _, _, _, _, _, _, _, _, _).

matches_dietary(Place, Dietary) :-
    restaurant(Place, _, _, _, _, _, _, _, _, _, DietaryOptions),
    (Dietary = any -> true ; member(Dietary, DietaryOptions)).

% get all possible values for a given attribute from remaining places
get_cuisines(Places, Cuisines) :-
    findall(C, (member(P, Places), restaurant(P, _, C, _, _, _, _, _, _, _, _)), AllCuisines),
    list_to_set(AllCuisines, Cuisines).

get_vibes(Places, Vibes) :-
    findall(V, (member(P, Places), restaurant(P, _, _, _, _, _, V, _, _, _, _)), AllVibes),
    list_to_set(AllVibes, Vibes).

get_meal_types(Places, Meals) :-
    findall(M, (member(P, Places), restaurant(P, _, _, _, _, Ms, _, _, _, _, _), member(M, Ms)), AllMeals),
    list_to_set(AllMeals, Meals).

get_types(Places, Types) :-
    findall(T, (member(P, Places), restaurant(P, T, _, _, _, _, _, _, _, _, _)), AllTypes),
    list_to_set(AllTypes, Types).