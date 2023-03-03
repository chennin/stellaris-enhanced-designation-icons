#!/usr/bin/env python3
from PIL import DdsImagePlugin, Image, ImageFilter, ImageEnhance
import os, sys

GAME_FILES = os.path.expanduser( os.path.expandvars( "~/stellaris-game" ) )
MOD_BASE = os.path.expanduser( os.path.expandvars( "~/stellaris-mod/designationicons" ) )
GAME_PATH = "gfx/interface/planetview"
FILE_NAME = "colony_type.dds"
ICON_WIDTH = 30
ICON_HEIGHT = 30
MISSING_ICON = f"{GAME_FILES}/gfx/interface/icons/missing_resources.dds"
ICON_ORDER = [
  "urban", # 0
  "mining",
  "agri",
  "generator",
  "forge",
  "factory",
  "refinery",
  "tech",
  "fortress", # 8
  "capital",
  "colony",
  "habitat", # 11
  "rural",
  "resort",
  "penal", # 14
  "primitive",
  "infested",
  "thrall",
  "habitat_generator",
  "habitat_leisure",
  "habitat_urban",
  "habitat_tech",
  "habitat_mining",
  "habitat_fortress",
  "habitat_forge",
  "habitat_factory",
  "habitat_refinery",
  "unification",
  "type_picker",
  "fringe",
  "industrial", # 30
  "habitat_industrial",
  "habitat_unification",
  "habitat_agri",
  "crucible",
]
REPLACEMENTS = {
  "urban": "gfx/interface/icons/resources/trade_value_large.dds",
  "mining": "gfx/interface/icons/resources/mineral_market_large.dds",
  "agri": "gfx/interface/icons/resources/food_market_large.dds",
  "generator": "gfx/interface/icons/resources/energy_market_large.dds",
  "forge": "gfx/interface/icons/resources/alloys_large.dds",
  "factory": "gfx/interface/icons/resources/consumer_goods_large.dds",
#  "refinery": "gfx/interface/icons/resources/exotic_gases_large.dds",
  "refinery": "gfx/interface/icons/menu_icon_strategic_resource.dds",
  "tech": "gfx/interface/icons/resources/engineering_research.dds",
#  "tech": "gfx/interface/icons/resources/physics_research.dds",
#  "tech": "gfx/interface/icons/text_icons/text_icon_science_ship.dds",

  "unification": "gfx/interface/icons/resources/unity.dds",
  # leisure desigs only exist on habitats
  "leisure": "gfx/interface/icons/planet_amenities.dds"
}

game_desig_file = Image.open(f"{GAME_FILES}/{GAME_PATH}/{FILE_NAME}")
game_desig_w, game_desig_h = game_desig_file.size

# Enhance some default icons for both regular and habitats
ENH_DEF = {
  "habitat": game_desig_file.crop( (ICON_ORDER.index("habitat") * ICON_WIDTH, 0, (ICON_ORDER.index("habitat") + 1) * ICON_WIDTH, ICON_HEIGHT) ),
  "fortress": game_desig_file.crop( (ICON_ORDER.index("fortress") * ICON_WIDTH, 0, (ICON_ORDER.index("fortress") + 1) * ICON_WIDTH, ICON_HEIGHT) ).filter(ImageFilter.EDGE_ENHANCE),
  "industrial": game_desig_file.crop( (ICON_ORDER.index("industrial") * ICON_WIDTH, 0, (ICON_ORDER.index("industrial") + 1) * ICON_WIDTH, ICON_HEIGHT) ).filter(ImageFilter.EDGE_ENHANCE_MORE).filter(ImageFilter.SMOOTH),
  "penal": game_desig_file.crop( (ICON_ORDER.index("penal") * ICON_WIDTH, 0, (ICON_ORDER.index("penal") + 1) * ICON_WIDTH, ICON_HEIGHT) ).filter(ImageFilter.EDGE_ENHANCE_MORE).filter(ImageFilter.SMOOTH),
  "resort": game_desig_file.crop( (ICON_ORDER.index("resort") * ICON_WIDTH, 0, (ICON_ORDER.index("resort") + 1) * ICON_WIDTH, ICON_HEIGHT) ).filter(ImageFilter.EDGE_ENHANCE).filter(ImageFilter.SMOOTH),
}

for i in range(0, int(game_desig_w / ICON_WIDTH), 1):
  box = (i*ICON_WIDTH, 0, (i+1)*ICON_WIDTH, ICON_HEIGHT)
  icon_name = ICON_ORDER[i]

  if icon_name in REPLACEMENTS:
    replacement = f"{GAME_FILES}/{REPLACEMENTS[icon_name]}"
    if not os.path.isfile(replacement):
      replacement = MISSING_ICON
    new_icon = Image.open(replacement)
    new_icon = new_icon.resize((ICON_WIDTH, ICON_HEIGHT))
    game_desig_file.paste(new_icon, (i*ICON_WIDTH, 0))

  # Combine and sometimes modify habitat icon with resource icon
  elif icon_name.startswith("habitat_"):
    resource_name = icon_name.split("_")[1]
    replacement = ""
    res_icon = None
    if resource_name in REPLACEMENTS:
      replacement = f"{GAME_FILES}/{REPLACEMENTS[resource_name]}"
      if not os.path.isfile(replacement):
        replacement = MISSING_ICON
      res_icon = Image.open(replacement)

      BRIGHTEN_FACTOR = 1.5
      # Enhance some just for habitats
      if resource_name in [ "leisure" ] and replacement in [ f"{GAME_FILES}/gfx/interface/icons/planet_amenities.dds", ]:
        res_icon = res_icon.filter(ImageFilter.EDGE_ENHANCE).filter(ImageFilter.SMOOTH)
      elif resource_name in [ "urban" ] and replacement in [ f"{GAME_FILES}/gfx/interface/icons/resources/trade_value_large.dds", ]:
        enhancer = ImageEnhance.Brightness(res_icon)
        res_icon = enhancer.enhance(BRIGHTEN_FACTOR)
    elif resource_name in ENH_DEF:
      res_icon = ENH_DEF[resource_name]

    if res_icon:
      tmp_habitat_icon = ENH_DEF["habitat"].copy()
      DIV_FACTOR = 1.5
      res_w = int(ICON_WIDTH / DIV_FACTOR)
      res_h = int(ICON_HEIGHT / DIV_FACTOR)
      res_icon = res_icon.resize( (res_w, res_h) )
      paste_pos = ( ICON_WIDTH - res_w, 0 ) 
      tmp_habitat_icon.paste(res_icon, paste_pos, res_icon) # 3rd arg is mask which handles pasting with transparency
      game_desig_file.paste(tmp_habitat_icon, (i*ICON_WIDTH, 0))

  elif icon_name in ENH_DEF:
    game_desig_file.paste(ENH_DEF[icon_name], (i*ICON_WIDTH, 0))

game_desig_file.save(fp = f"{MOD_BASE}/{GAME_PATH}/{FILE_NAME}")
