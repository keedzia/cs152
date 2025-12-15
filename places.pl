% knowledge base for restaurants and bars near esmeralda 920

% restaurant(name, type, cuisine, budget, distance_blocks, meal_types, vibe, takes_reservations, max_group_size, has_wifi, dietary_options)

% restaurants
restaurant('santos_manjares', restaurant, parrilla, medium, 0.2, [lunch, dinner], casual, no, 8, yes, [vegetarian]).
restaurant('empas_world', restaurant, argentinian, cheap, 0.3, [breakfast, lunch, dinner, snack], casual, no, 3, yes, [vegetarian, vegan]).
restaurant('surry_hills', restaurant, australian, expensive, 6.3, [brunch, lunch, dinner], upscale, yes, 8, yes, [vegetarian, vegan, gluten_free]).
restaurant('parrilla_cero5', restaurant, argentinian, expensive, 0.2, [lunch, dinner], upscale, yes, 6, no, [vegetarian, gluten_free]).
restaurant('warren_cafe_brunch', restaurant, cafe, medium, 2.9, [breakfast, brunch, lunch, snack], study_friendly, no, 3, yes, [vegetarian, vegan, gluten_free]).
restaurant('sheikobs_bagels', restaurant, cafe, cheap, 5.5, [breakfast, brunch, lunch, snack], casual, no, 4, yes, [vegetarian, vegan]).
restaurant('la_reverde_parrillita_vegana', restaurant, vegan, medium, 2.2, [lunch, dinner], casual, no, 4, no, [vegan, vegetarian, gluten_free]).
restaurant('relicioso_comida_vegana', restaurant, vegan, medium, 2.0, [lunch, dinner, snack], casual, no, 6, yes, [vegan, vegetarian, gluten_free]).
restaurant('la_meca_shawarma', restaurant, halal, cheap, 2.2, [lunch, dinner, snack], casual, no, 6, no, [vegetarian, halal]).
restaurant('rifi_restaurante', restaurant, halal, medium, 3.9, [lunch, dinner], casual, no, 6, no, [vegetarian, vegan, halal]).
restaurant('sazon_mexica', restaurant, mexican, medium, 0.7, [lunch, dinner], casual, no, 6, no, [vegetarian, vegan]).
restaurant('la_despensa_de_graziano', restaurant, mexican, medium, 2.0, [lunch, dinner], casual, no, 8, yes, [vegetarian, gluten_free]).
restaurant('delhi_mahal', restaurant, indian, expensive, 0.6, [lunch, dinner], upscale, no, 4, yes, [halal, vegan, vegetarian]).
restaurant('pandok', restaurant, armenian, medium, 1, [lunch, dinner], casual, no, 6, yes, [vegetarian]).
restaurant('presencia', restaurant, french, expensive, 1.5, [dinner], upscale, yes, 4, yes, [vegetarian, gluten_free]).
restaurant('rapanui', restaurant, argentinian, cheap, 0.3, [snack], casual, no, 4, yes, [vegetarian, gluten_free, halal]).
restaurant('kefi', restaurant, greek, medium, 9.2, [lunch, dinner], casual, no, 4, yes, [vegetarian, gluten_free, vegan, halal]).
restaurant('empanairo', restaurant, argentinian, cheap, 0.3, [breakfast, snack], casual, no, 3, no, [vegetarian, halal]).
restaurant('lupita', restaurant, mexican, expensive, 3.2, [lunch, dinner], casual, no, 6, yes, [vegetarian]).

% bars
restaurant('alvear_roof_bar', bar, international, expensive, 1.7, [snack, dinner], upscale, yes, 6, yes, [vegetarian, vegan, gluten_free]).
restaurant('on_tap_retiro', bar, international, medium, 0.1, [lunch, dinner, snack], social, no, 6, yes, [vegetarian]).
restaurant('backroom_bar', bar, international, cheap, 5.0, [dinner, snack], casual, no, 6, no, [vegetarian]).
restaurant('avant_garten', bar, international, medium, 5.5, [lunch, dinner, snack], social, no, 10, yes, [vegetarian, vegan]).
restaurant('bar_la_morenita', bar, international, cheap, 1.7, [dinner, snack], casual, no, 8, no, [vegetarian]).

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

get_budgets(Places, Budgets) :-
    findall(B, (member(P, Places), restaurant(P, _, _, B, _, _, _, _, _, _, _)), AllBudgets),
    list_to_set(AllBudgets, Budgets).

get_max_distance(Places, MaxDist) :-
    findall(D, (member(P, Places), restaurant(P, _, _, _, D, _, _, _, _, _, _)), Dists),
    max_list(Dists, MaxDist).

get_min_distance(Places, MinDist) :-
    findall(D, (member(P, Places), restaurant(P, _, _, _, D, _, _, _, _, _, _)), Dists),
    min_list(Dists, MinDist).

has_wifi_available(Places) :-
    member(P, Places),
    restaurant(P, _, _, _, _, _, _, _, _, yes, _), !.

has_no_wifi_available(Places) :-
    member(P, Places),
    restaurant(P, _, _, _, _, _, _, _, _, no, _), !.

has_reservations_available(Places) :-
    member(P, Places),
    restaurant(P, _, _, _, _, _, _, yes, _, _, _), !.

has_no_reservations_available(Places) :-
    member(P, Places),
    restaurant(P, _, _, _, _, _, _, no, _, _, _), !.

get_max_group_size(Places, MaxSize) :-
    findall(S, (member(P, Places), restaurant(P, _, _, _, _, _, _, _, S, _, _)), Sizes),
    max_list(Sizes, MaxSize).

get_min_group_size(Places, MinSize) :-
    findall(S, (member(P, Places), restaurant(P, _, _, _, _, _, _, _, S, _, _)), Sizes),
    min_list(Sizes, MinSize).

get_dietary_options(Places, Options) :-
    findall(O, (member(P, Places), restaurant(P, _, _, _, _, _, _, _, _, _, Opts), member(O, Opts)), AllOptions),
    list_to_set(AllOptions, Options).