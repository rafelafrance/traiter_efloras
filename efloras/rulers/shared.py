"""Shared plant rule logic."""

from traiter.new.rules.literals import Literals
from traiter.new.rules.regexp import Regexp


DASH = Regexp(regexp=r'\p{Pd}')

# (?<! to \s )
ALL_PLANT_PARTS = Literals(aux='plant part', literals=[[p] for p in """
    androecia androecium anther anthers
    blade blades
    calyces calyx carpel carpels corolla corollas
    flower flowers
    gynoecia gynoecium
    hair hairs hypanthia hypanthium
    leaf leaflet leaves lobe lobes
    petal petals petiole petioles petiolule petiolules
    pistil pistils peduncle peduncles
    ovary ovaries ovule ovules
    raceme racemes
    sepal sepals stamen stamens stigma stigmas stipule stipules style styles
    """.split()])

PLANT_PART = {
    'anther': Literals(aux='anther part', literals=[['anther'], ['anthers']]),
    'calyx': Literals(aux='calyx part', literals=[['calyx'], ['calyces']]),
    'hairs': Literals(aux='hairs part', literals=[['hair'], ['hairs']]),
    'petal': Literals(aux='petal part', literals=[['petal'], ['petals']]),
    'sepal': Literals(aux='sepal part', literals=[['sepal'], ['sepals']]),
    'stamen': Literals(aux='stamen part', literals=[['stamen'], ['stamens']]),
    'stigma': Literals(aux='stigma part', literals=[['stigma'], ['stigmas']]),
    'style': Literals(aux='style part', literals=[['style'], ['styles']]),
    'corolla': Literals(aux='corolla part', literals=[
        ['corolla'], ['corollas']]),
    'flower': Literals(aux='flower part', literals=[
        ['pistillate', 'flower'], ['pistillate', 'flowers'],
        ['staminate', 'flower'], ['staminate', 'flowers'],
        ['flower'], ['flowers']]),
    'hypanthium': Literals(aux='hypanthium part', literals=[
        ['hypanthia'], 'hypanthium']),
    'leaf': Literals(aux='leaf part', literals=[
        ['leaf', 'blade'], ['leaf', 'blades'],
        ['leaflet'], ['leaves'], ['blade'], ['blades']]),
    'lobes': Literals(aux='lobes part', literals=[
        ['leaf', 'lobe'], ['leaf', 'lobed'], ['leaf', 'lobes'],
        ['lobe'], ['lobed'], ['lobes'], ['unlobed']]),
    # (?<! to \s )
    'petiole': Literals(aux='petiole part', literals=[
        ['petiole'], ['petioles'], ['petiolule'], ['petiolules']]),
    }
