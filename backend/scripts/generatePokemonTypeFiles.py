from interfaces import PokemonType, PokemonTypeResponseInterface
import requests
from jinja2 import Template

def generatePokemonTypeFiles():
    '''Generates JSON files for each Pokemon type by fetching data from the PokeAPI.'''
    requestUrl = "https://pokeapi.co/api/v2/type/"

    pokemonTypeTemplateFile = open("templates/pokemonTypeTemplate.j2", "r")
    content = pokemonTypeTemplateFile.read()
    pokemonTypeTemplateFile.close()

    # get the template for pokemon types
    template = Template(content)

    for pokemonType in PokemonType:
        typeUrl = f"{requestUrl}{pokemonType.value}/"
        # Make API request and process the response
        response = requests.get(typeUrl)

        if response.status_code == 200:
            data: PokemonTypeResponseInterface = response.json()

            # Render the template with the data
            documentText = template.render(
                pokemonType=data["name"],
                doubleDamageFrom=[resource["name"] for resource in data["damage_relations"]["double_damage_from"]],
                doubleDamageTo=[resource["name"] for resource in data["damage_relations"]["double_damage_to"]],
                noDamageFrom=[resource["name"] for resource in data["damage_relations"]["no_damage_from"]],
                noDamageTo=[resource["name"] for resource in data["damage_relations"]["no_damage_to"]]
            )

            # Save the generated text to a text file
            with open(f"data/pokemonTypes/{pokemonType.value}.txt", "w") as f:
                f.write(documentText)
