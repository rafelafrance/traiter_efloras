"""Parse the trait."""
from spacy.matcher import PhraseMatcher

from .base import Base
from .shared import SHARED_TERMS
from ..pylib.trait import Trait

SHAPE_TERMS = {
    'SHAPE': r"""
        acicular actinomorphic acuminate acute
        apiculate aristate attenuate auriculate
        bilabiate bilateral bilaterally bowlshaped
        calceolate campanulate caudate circular convex cordate coronate
        crateriform cruciform cuneate cupshaped cupulate cyanthiform
        cylindric cylindrical cymbiform
        deltate deltoid dentate depressed digitate
        elliptic elongate emarginate ensate ensiform
        falcate fenestrate filiform flabellate flabelliorm funnelform
        galeate globose
        hastate hemispheric
        incised infundibular irregular irregularly
        keeled
        labiate laciniate lanceolate ligulate liguliform linear lorate lyrate
        monosymmetric monosymmetrical mucronate multifid
        navicular
        obconic obcordate oblanceolate oblique oblong obovate obtriangular
        obtuse orbicular orbiculate orbicular ovate
        palmatifid palmatipartite palmatisect pandurate
        papilionaceous peltate pentagonal pentangular perfoliate
        perforate petiolate pinnate pinnately pinnatifid pinnatipartite
        pinnatisect plicate polygonal
        radially rectangular regular reniform retuse rhombic rhomboid
        rhomboidal rosette rosettes rotate rotund round rounded roundish
        saccate sagittate salverform saucerlike saucershaped semiterete
        septagonal sinuate spatulate spearshaped spheric stellate
        subcylindric ubcylindrical subobtuse suborbicular suborbiculate
        subpeltate subreniform subterete subulate symmetric
        terete triangular trullate truncate tubular turbinate
        undulate unifoliate urceolate
        zygomorphic zygomorphous
        """.split(),
    'NSHAPE': """ angular angulate """.split(),
    'PREFIX': """ semi sub elongate """.split(),
    }

# LEAF_POLYGONAL = fr"""
#     ( ( orbicular | angulate ) -? )?
#     ( \b (\d-)? angular | \b (\d-)? angulate
#         | pentagonal | pentangular | septagonal )
#     ( -? ( orbicular | (\d-)? angulate ) )?
#     """.split()

RENAME = {
    'actinomorphic': 'radially symmetric',
    'angular-orbiculate': 'polygonal',
    'bilateral': 'bilaterally symmetric',
    'bowl-shaped': 'saucerlike',
    'bowlshaped': 'saucerlike',
    'crateriform': 'saucerlike',
    'cupulate': 'cup-shaped',
    'cyanthiform': 'saucerlike',
    'deltate': 'deltoid',
    'ensiform': 'linear',
    'flabelliorm': 'flabellate',
    'globose': 'spheric',
    'irregular': 'bilaterally symmetric',
    'irregularly': 'bilaterally symmetric',
    'keeled': 'cymbiform',
    'labiate': 'bilabiate',
    'liguliform': 'ligulate',
    'lorate': 'linear',
    'monosymmetric': 'bilaterally symmetric',
    'monosymmetrical': 'bilaterally symmetric',
    'navicular': 'cymbiform',
    'oblong-terete': 'oblong',
    'palmately': 'palmate',
    'pedately': 'pedate',
    'rectangular': 'rhomboid',
    'regular': 'radially symmetric',
    'rhombic': 'rhomboic',
    'saucer-shaped': 'saucerlike',
    'saucershaped': 'saucerlike',
    'subcylindric': 'cylindrical',
    'subcylindrical': 'cylindrical',
    'subreniform': 'reniform',
    'zygomorphic': 'bilaterally symmetric',
    'zygomorphous': 'bilaterally symmetric',
    'circular': 'orbicular',
    'orbiculate': 'orbicular',
    'rotund': 'orbicular',
    'round': 'orbicular',
    'rounded': 'orbicular',
    'roundish': 'orbicular',
    'suborbicular': 'orbicular',
    'suborbiculate': 'orbicular',
    }


class PlantShape(Base):
    """Parse plant colors."""

    def __init__(self):
        super().__init__()
        self.matcher = PhraseMatcher(self.nlp.vocab, attr='LOWER')

        terms = {**SHARED_TERMS, **SHAPE_TERMS}
        for label, values in terms.items():
            patterns = [self.nlp.make_doc(x) for x in values]
            self.matcher.add(label, None, *patterns)

    def parse(self, text):
        """Parse the traits."""
        traits = []
        trait = Trait()
        traits.append(trait)
        return traits


PLANT_SHAPE = PlantShape()
