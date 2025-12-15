% knowledge base for restaurants and bars near esmeralda 920

% restaurant(name, type, cuisine, budget, distance_blocks, meal_types, vibe, takes_reservations, max_group_size, has_wifi, dietary_options)

% restaurants
restaurant('santos_manjares', restaurant, parrilla, medium, 0.2, [lunch, dinner], casual, no, 40, yes, [vegetarian]).
restaurant('empas_world', restaurant, argentinian, cheap, 0.3, [breakfast, lunch, dinner, snack], casual, no, 15, yes, [vegetarian, vegan]).
restaurant('surry_hills', restaurant, australian, expensive, 6.3, [brunch, lunch, dinner], upscale, yes, 25, yes, [vegetarian, vegan, gluten_free]).
restaurant('parrilla_cero5', restaurant, argentinian, expensive, 0.2, [lunch, dinner], upscale, yes, 50, no, [vegetarian, gluten_free]).
restaurant('warren_cafe_brunch', restaurant, cafe, medium, 2.9, [breakfast, brunch, lunch, snack], study_friendly, no, 20, yes, [vegetarian, vegan, gluten_free]).
restaurant('sheikobs_bagels', restaurant, cafe, cheap, 5.5, [breakfast, brunch, lunch, snack], casual, no, 15, yes, [vegetarian, vegan]).
restaurant('la_reverde_parrillita_vegana', restaurant, vegan, medium, 2.2, [lunch, dinner], casual, no, 25, no, [vegan, vegetarian, gluten_free]).
restaurant('relicioso_comida_vegana', restaurant, vegan, medium, 2.0, [lunch, dinner, snack], casual, no, 20, yes, [vegan, vegetarian, gluten_free]).
restaurant('la_meca_shawarma', restaurant, halal, cheap, 2.2, [lunch, dinner, snack], casual, no, 30, no, [vegetarian, halal]).
restaurant('rifi_restaurante', restaurant, halal, medium, 3.9, [lunch, dinner], casual, no, 35, no, [vegetarian, vegan, halal]).
restaurant('sazon_mexica', restaurant, mexican, medium, 0.7, [lunch, dinner], casual, no, 25, no, [vegetarian, vegan]).
restaurant('la_despensa_de_graziano', restaurant, mexican, medium, 2.0, [lunch, dinner], casual, no, 40, yes, [vegetarian, gluten_free]).


% bars
restaurant('alvear_roof_bar', bar, international, expensive, 1.7, [snack, dinner], upscale, yes, 20, yes, [vegetarian, vegan, gluten_free]).
restaurant('on_tap_retiro', bar, international, medium, 0.1, [lunch, dinner, snack], social, no, 30, yes, [vegetarian]).
restaurant('backroom_bar', bar, international, cheap, 5.0, [dinner, snack], casual, no, 25, no, [vegetarian]).
restaurant('avant_garten', bar, international, medium, 5.5, [lunch, dinner, snack], social, no, 40, yes, [vegetarian, vegan]).
restaurant('bar_la_morenita', bar, international, cheap, 1.7, [dinner, snack], casual, no, 20, no, [vegetarian]).

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