from enum import Enum
from typing import TypedDict

class PokemonType(Enum):
    '''
    Enum representing the different Pokemon types.
    '''
    NORMAL = "normal"
    FIGHTING = "fighting"
    FLYING = "flying"
    POSION = "poison"
    GROUND = "ground"
    ROCK = "rock"
    BUG = "bug"
    GHOST = "ghost"
    STEEL = "steel"
    FIRE = "fire"
    WATER = "water"
    GRASS = "grass"
    ELECTRIC = "electric"
    PSYCHIC = "psychic"
    ICE = "ice"
    DRAGON = "dragon"
    DARK = "dark"
    FAIRY = "fairy"

class ResourseInterface(TypedDict):
    name: str
    url: str

class DamageRelationsInterface(TypedDict):
    double_damage_from: list[ResourseInterface]
    double_damage_to: list[ResourseInterface]
    half_damage_from: list[ResourseInterface]
    half_damage_to: list[ResourseInterface]
    no_damage_from: list[ResourseInterface]
    no_damage_to: list[ResourseInterface]


class PokemonTypeResponseInterface(TypedDict):
    damage_relations: DamageRelationsInterface
    name: str