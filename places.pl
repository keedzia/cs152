% knowledge base for restaurants and bars near esmeralda 920

% restaurant(name, type, cuisine, budget, distance_blocks, meal_types, vibe, takes_reservations, max_group_size, has_wifi, dietary_options)

% restaurants
restaurant('santos_manjares', restaurant, parrilla, medium, walking, [lunch, dinner], casual, no, 40, yes, [vegetarian]).
restaurant('empas_world', restaurant, international, cheap, walking, [breakfast, lunch, dinner, snack], casual, no, 15, yes, [vegetarian, vegan]).
restaurant('surry_hills', restaurant, international, expensive, short_ride, [brunch, lunch, dinner], upscale, yes, 25, yes, [vegetarian, vegan, gluten_free]).
restaurant('parrilla_cero5', restaurant, parrilla, expensive, short_ride, [lunch, dinner], upscale, yes, 50, no, [vegetarian, gluten_free]).
restaurant('warren_cafe_brunch', restaurant, cafe, medium, walking, [breakfast, brunch, lunch, snack], study_friendly, no, 20, yes, [vegetarian, vegan, gluten_free]).
restaurant('sheikobs_bagels', restaurant, cafe, cheap, short_ride, [breakfast, brunch, lunch, snack], casual, no, 15, yes, [vegetarian, vegan]).
restaurant('la_reverde_parrillita_vegana', restaurant, vegan, medium, walking, [lunch, dinner], casual, no, 25, no, [vegan, vegetarian, gluten_free]).
restaurant('relicioso_comida_vegana', restaurant, vegan, medium, walking, [lunch, dinner, snack], casual, no, 20, yes, [vegan, vegetarian, gluten_free]).
restaurant('la_meca_shawarma', restaurant, 'comida_arabe', cheap, walking, [lunch, dinner, snack], casual, no, 30, no, [vegetarian, halal]).
restaurant('rifi_restaurante', restaurant, 'comida_arabe', medium, short_ride, [lunch, dinner], casual, no, 35, no, [vegetarian, vegan, halal]).
restaurant('sazon_mexica', restaurant, mexican, medium, walking, [lunch, dinner], casual, no, 25, no, [vegetarian, vegan]).
restaurant('la_despensa_de_graziano', restaurant, international, medium, short_ride, [lunch, dinner], casual, no, 40, yes, [vegetarian, gluten_free]).


% bars
restaurant('alvear_roof_bar', bar, international, expensive, short_ride, [snack, dinner], upscale, yes, 20, yes, [vegetarian, vegan, gluten_free]).
restaurant('on_tap_retiro', bar, international, medium, walking, [lunch, dinner, snack], social, no, 30, yes, [vegetarian]).
restaurant('backroom_bar', bar, international, cheap, walking, [dinner, snack], casual, no, 25, no, [vegetarian]).
restaurant('avant_garten', bar, international, medium, short_ride, [lunch, dinner, snack], social, no, 40, yes, [vegetarian, vegan]).
restaurant('the_little_bar_canitas', bar, international, cheap, far, [dinner, snack], casual, no, 20, no, [vegetarian]).

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