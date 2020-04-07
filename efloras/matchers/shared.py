"""Shared plant rule logic."""

# from traiter.new.rules.literals import Literals
# from traiter.new.rules.regexp import Regexp


# DASH = Regexp(regexp=r'\p{Pd}')

# (?<! to \s )
SHARED_TERMS = {
    'PLANT_PART': """
        androecia androecium anther anthers
        blade blades
        calyces calyx carpel carpels corolla corollas
        flower flowers
        gynoecia gynoecium
        hair hairs hypanthia hypanthium
        leaf leaflet leaves :lobe lobes
        petal petals petiole petioles petiolule petiolules
        pistil pistils peduncle peduncles
        ovary ovaries ovule ovules
        raceme racemes
        sepal sepals stamen stamens stigma stigmas stipule stipules
        style styles
        """.split(),
    }
