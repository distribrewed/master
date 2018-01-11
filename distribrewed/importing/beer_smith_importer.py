#!/usr/bin python
import html
import logging

from importing.brew_importer import BrewImporter
from importing.beer_smith_parser import *
from brew.models import Recipe, RecipeSection, RecipeStep

log = logging.getLogger(__name__)

units = ["mg", "g", "oz", "lb", "kg", "ml", "tsp", "tbsp", "cup", "pt", "qt", "l", "gal", "items"]
use = ["boil", "mash", "primary", "secondary", "bottling"]
Hop = 'Hop'
Misc = 'Misc'
HopUnit = "Grams"
MashType = "mash"
BoilType = "boil"
FermentationType = "fermentation"


def convert_f2c(s):
    """(str): float

    Converts a Fahrenheit temperature represented as a string
    to a Celsius temperature.
    """
    fahrenheit = float(s)
    celsius = round((fahrenheit - 32) * 5 / 9, 1)
    return str(celsius)

def convert_o2g(s):
    """(str): float

    Converts a Ounces represented as a string
    to grams.
    """
    ounce = float(s)
    grams = round(ounce / 0.035274, 1)
    return str(grams)

class BeerSmithImporter(BrewImporter):
    def __init__(self):
        BrewImporter.__init__(self)
        self.display_name = 'Beer Smith Importer'
        self.recipe_file = ''
        self.counter = 0

    def do_import(self, uri):
        try:
            if uri is None:
                return 0
            self.recipe_file = uri
            log.debug('Loading recipe file {0}...'.format(self.recipe_file))
            beer = BeerParser()
            recipe_data = beer.get_recipes(self.recipe_file)
            self.counter = 0
            for item in recipe_data:
                name = lookup_brew_name(item).strip()
                if name is not None:
                    # Save to database
                    brew, sections, stepslist = _create_recipe_model(item)
                    brew.save()
                    self.counter += 1
                    s_count = m_count = b_count = f_count = 0
                    for section, steps in sections, stepslist:
                        s_count += 1
                        s = _create_recipe_section(section, brew, s_count)
                        s.save()
                        for step in steps:
                            step.save()
            log.debug('...done loading recipe file {0}'.format(self.recipe_file))
        except Exception as e:
            log.error('Failed to load recipes {0} ({1})'.format(self.recipe_file, e.args[0]))
        return self.counter


BREW_NAME_NODE = "F_R_NAME"
BREW_BREWER_NODE = "F_R_BREWER"
BREW_STYLE_NODE = "F_R_STYLE"
BREW_STYLE_NAME_NODE = "F_S_NAME"
BREW_STYLE_CATEGORY_NODE = "F_S_CATEGORY"
BREW_STYLE_DESCRIPTION_NODE = "F_S_DESCRIPTION"
BREW_STYLE_PROFILE_NODE = "F_S_PROFILE"
BREW_STYLE_INGREDIENTS_NODE = "F_S_INGREDIENTS"
BREW_STYLE_WEB_NODE = "F_S_WEB_LINK"


def _create_recipe_model(data):
    brew = Recipe()
    brew.name = lookup_brew_name(data)
    brew.brewer = lookup_brew_info(data, BREW_BREWER_NODE)
    brew.style = lookup_brewstyle_info(data, BREW_STYLE_NAME_NODE)
    brew.category = lookup_brewstyle_info(data, BREW_STYLE_CATEGORY_NODE)
    brew.description = lookup_brewstyle_info(data, BREW_STYLE_DESCRIPTION_NODE)
    brew.profile = lookup_brewstyle_info(data, BREW_STYLE_PROFILE_NODE)
    brew.ingredients = lookup_brewstyle_info(data, BREW_STYLE_INGREDIENTS_NODE)
    brew.web_link = lookup_brewstyle_info(data, BREW_STYLE_WEB_NODE)
    mash, mashsteps = _generate_mash_section(data)
    boil, boilsteps = _generate_boil_section(data)
    ferment, fermentsteps = _generate_fermentation_section(data)
    sections = [mash, boil, ferment]
    steps = [mashsteps, boilsteps, fermentsteps]
    return brew, sections, steps


def _generate_mash_section(recipe):
    # Mash Schedule extracted
    # self.name = html.unescape(recipe.data["F_R_NAME"])
    mash = RecipeSection()
    mash.name = "Mash"
    mash.type = MashType
    mashsteps = []
    index = 0
    for mashItem in recipe.children["F_R_MASH"].children["steps"].subdata:
        if mashItem.name == "MashStep":
            index += 1
            name = html.unescape(mashItem.data["F_MS_NAME"])
            temp = convert_f2c(mashItem.data["F_MS_STEP_TEMP"])
            min = mashItem.data["F_MS_STEP_TIME"][:-8]
            mashstep = _create_mash_step(mash, index, name, temp, min)
            mashsteps.append(mashstep)
    return mash, mashsteps

def _generate_boil_section(recipe):
    # Boil Schedule extracted
    # self.name = html.unescape(recipe.data["F_R_NAME"])
    # Hops
    boil = RecipeSection()
    boil.name = "Boil"
    boil.type = BoilType
    boilsteps = []
    index = 0
    for ingredient in recipe.children["Ingredients"].subdata:
        if ingredient.name == "Hops" and int(ingredient.data["F_H_DRY_HOP_TIME"][-9]) == 0:
            index += 1
            name = html.unescape(ingredient.data["F_H_NAME"])
            unit = HopUnit
            amount = convert_o2g(ingredient.data["F_H_AMOUNT"])
            min = ingredient.data["F_H_BOIL_TIME"][:-8]
            boilstep = _create_boil_step(boil, index, name, unit, amount, min)
            boilsteps.append(boilstep)
    # Misc ingredients
    for ingredient in recipe.children["Ingredients"].subdata:
        if ingredient.name == "Misc":
            name = html.unescape(ingredient.data["F_M_NAME"])
            unit = units[int(ingredient.data["F_M_UNITS"])]
            amount = ingredient.data["F_M_AMOUNT"]
            min = ingredient.data["F_M_TIME"][:-8]
            boilstep = _create_boil_step(boil, index, name, unit, amount, min)
            boilsteps.append(boilstep)
    return boil, boilsteps

def _generate_fermentation_section(recipe):
    # Fermentation Schedule extracted
    # self.name = html.unescape(recipe.data["F_R_NAME"])
    fermentation = RecipeSection()
    fermentation.name = "Fermentation"
    fermentation.type = FermentationType
    fermentationsteps = []
    # Primary step
    start_temp = convert_f2c(recipe.children["F_R_AGE"].data["F_A_PRIM_TEMP"])
    end_temp = convert_f2c(recipe.children["F_R_AGE"].data["F_A_PRIM_END_TEMP"])
    days = recipe.children["F_R_AGE"].data["F_A_PRIM_DAYS"][:-8]
    fermentationstep = _create_fermentation_step(fermentation, 1, start_temp, days)
    fermentationsteps.append(fermentationstep)
    # Secondary step
    start_temp = convert_f2c(recipe.children["F_R_AGE"].data["F_A_SEC_TEMP"])
    end_temp = convert_f2c(recipe.children["F_R_AGE"].data["F_A_SEC_END_TEMP"])
    days = recipe.children["F_R_AGE"].data["F_A_SEC_DAYS"][:-8]
    fermentationstep = _create_fermentation_step(fermentation, 2, start_temp, days)
    fermentationsteps.append(fermentationstep)
    # Tertiary step
    start_temp = convert_f2c(recipe.children["F_R_AGE"].data["F_A_TERT_TEMP"])
    end_temp = convert_f2c(recipe.children["F_R_AGE"].data["F_A_TERT_END_TEMP"])
    days = recipe.children["F_R_AGE"].data["F_A_TERT_DAYS"][:-8]
    fermentationstep = _create_fermentation_step(fermentation, 3, start_temp, days)
    fermentationsteps.append(fermentationstep)
    # Age step
    start_temp = convert_f2c(recipe.children["F_R_AGE"].data["F_A_AGE_TEMP"])
    end_temp = convert_f2c(recipe.children["F_R_AGE"].data["F_A_END_AGE_TEMP"])
    days = recipe.children["F_R_AGE"].data["F_A_AGE"][:-8]
    fermentationstep = _create_fermentation_step(fermentation, 4, start_temp, days)
    fermentationsteps.append(fermentationstep)
    return fermentation, fermentationsteps

def _create_recipe_section(brew, index, name, type):
    section = RecipeSection()
    section.index = index
    section.recipe = brew
    section.name = name
    section.worker_type = type
    return section


def _create_mash_step(section, index, name, temp, min):
    brew_step = RecipeStep()
    brew_step.recipe_section = section
    brew_step.index = index
    brew_step.name = name
    brew_step.unit = ''
    brew_step.target = temp
    brew_step.hold_time = min
    brew_step.unit = RecipeStep.MINUTES
    return brew_step


def _create_boil_step(section, index, name, unit, amount, min):
    brew_step = RecipeStep()
    brew_step.recipe_section = section
    brew_step.index = index
    brew_step.name = name
    brew_step.unit = unit
    brew_step.target = amount
    brew_step.hold_time = min
    brew_step.time_unit_seconds = RecipeStep.MINUTES
    return brew_step


def _create_fermentation_step(section, index, start_temp, days):
    brew_step = RecipeStep()
    brew_step.recipe_section = section
    brew_step.index = index
    brew_step.name = section.name
    brew_step.unit = ''
    brew_step.target = start_temp
    brew_step.hold_time = days
    brew_step.time_unit_seconds = RecipeStep.DAYS
    return brew_step


def lookup_brew_info(data, key):
    if data.data.__contains__(key):
        return html.unescape(data.data[key])
    return ""


def lookup_brew_name(data):
    return lookup_brew_info(data, BREW_NAME_NODE)


def lookup_brewstyle_info(data, key):
    if not data.children.__contains__(BREW_STYLE_NODE):
        return ""
    style = data.children[BREW_STYLE_NODE]
    if style.data.__contains__(key):
        return html.unescape(style.data[key])
    return ""