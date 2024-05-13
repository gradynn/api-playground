import requests
import pandas as pd

URL = "https://pokeapi.co/api/v2/pokemon/"

# List of original 150 pokemon
o150_pokemon = pd.read_csv('./pokemon.csv').columns

def append_row_to_df(pokemon_info, pokemon_details):
    stats_to_append = {}
    
    # Collect name
    stats_to_append["Name"] = pokemon_details["name"].capitalize()

    # Collect stats
    stats = pokemon_details["stats"]
    for stat in stats:
        stats_to_append[stat["stat"]["name"].capitalize()] = stat["base_stat"]

    # Collect types into string
    types = pokemon_details["types"]
    type_str = types[0]["type"]["name"].capitalize()
    for i in range(1, len(types)):
        type_str = type_str + f'|{types[i]["type"]["name"].capitalize()}'
    stats_to_append["Type"] = type_str

    # Collect weight
    weight = pokemon_details["weight"]
    stats_to_append["Weight"] = weight

    df = pd.DataFrame([stats_to_append])
    return pd.concat([pokemon_info, df], ignore_index=True)

# collect/transform data for all pokemon
pokemon_info = pd.DataFrame(columns=["Name", "Type", "Weight", "HP", "Attack", "Defense", "Special-attack", "Special-defense", "Speed"])

for pokemon in o150_pokemon:
    pokemon = pokemon.lower()

    print(f'Fetching {pokemon}')
    try:
        r = requests.get(URL + pokemon)
        r_json = r.json()
        pokemon_info = append_row_to_df(pokemon_info, r_json)
    except Exception as e:
        print(f'Error occured fetching {pokemon}, exception {e}')

pokemon_info.to_csv('./pokedex.csv')