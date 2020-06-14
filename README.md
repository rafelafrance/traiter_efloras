# The eFloras Traits Database Project [![Build Status](https://travis-ci.org/rafelafrance/traiter_efloras.svg?branch=master)](https://travis-ci.org/rafelafrance/traiter_efloras)

## All right, what's this all about then?
**Challenge**: Extract trait information from plant treatments. That is, if I'm given treatment text like:
 ```
 Shrubs or trees evergreen, monoecious, 1-3 m tall; trunk to 3 cm d.b.h.; bark
grayish. Branchlets and buds densely tomentose or pubescent. Petiole 0-1 cm,
pubescent to tomentose; leaf blade elliptic-obovate to cuneate-obovate,
1.5-7 × 0.5-3 cm, subleathery, abaxially densely golden glandular, adaxially
golden glandular when young, midvein pubescent, base cuneate, margin usually
serrate or serrate-crenate in apical 2/3, apex acute or obtuse. Male spikes
nearly simple, ascending, 1-2 cm; peduncle and rachis pubescent; bracts
overlapping, ciliate, densely golden glandular. Male flowers without bracteoles.
Stamens 2-6; anthers red(?), ellipsoid. Female spikes solitary in leaf axils or
inconspicuously branched at base, to 1.5 cm, 1-3-flowered; rachis pubescent;
bracts ciliate and densely golden glandular. Female flowers often with
2 bracteoles. Ovary velutinous in young fruit; stigmas 2, bright red. Drupe
usually 1 per infructescence, red or white, usually ellipsoid, papilliferous,
0.7-1 cm in diam. Fl. Oct-Nov, fr. Feb-May of following year.
 ```
I should be able to extract:
- anther_color: red
- bark_color: gray
- bract_color:
    - sex = male, golden
    - sex = female, golden
- bract_count: 2, sex = female
- fruit_color: red, white
- fruit_count: 1
- fruit_size :diameter_low = 0.7, diameter_high = 1.0, diameter_units = cm
- inflorescences_size: sex = male, length_low = 1.0, length_high = 2.0, length_units = cm
- leaf_color: golden
- leaf_shape:
    - elliptic-obovate
    - cuneate-obovate
    - cuneate
    - acute
    - obtuse
- leaf_size:
    - length_low = 1.5, length_high = 7.0, width_low = 0.5, width_high = 3.0, width_units: cm
    - sex = female, length_high = 1.5, length_units = cm
- petiole_size: length_high = 1.0, length_units = cm
- plant_reproduction: monoecious
- plant_seasonal: evergreen
- plant_size: height_low = 1.0, height_high = 3.0, height_units = m
- stamen_count: low = 2, high = 6
- stigma_color: red
- stigma_count: 2
- trunk_size: dbh_high = 3.0, dbh_units = cm
- etc.

## Parsing strategy
1. I first, split the text into sentences using a simple rule-based parser.
1. Next I label terms using Spacy's phrase and rule-based matchers.
1. Then I match terms using rule-based matchers repeatedly until I have built up a recognizable trait like: color, size, count, etc.
1. Finally, I associate traits with plant parts.

For example, given the sentence: `Petiole 1-2 cm. Leaf blade 2-4 cm.`:
- First I split this into two sentences: `Petiole 1-2 cm` and `Leaf blade 2-4 cm.`. Taking the first sentence I then do the following.
- I recognize the tokens in the sentence:
    - `Petiole` = plant part
    - `1` = number
    - `-` = dash
    - `2` = number
    - `cm` = units
- Then I group tokens. In this sentence I only group one set:
    - `1-2` = a range
- Next I recognize a size trait:
    - `1-2 cm` = a range with units.
- Finally, I associate the size with the plant part: `Petiole`

There are, of course, complications and subtleties not outlined above but you should get the gist of what is going on here.

## Install
You will need to have Python installed. You can install the requirements into your python environment like so:
```
git clone https://github.com/rafelafrance/traiter_efloras.git
cd traiter_efloras
optional: virtualenv -p python3 venv
optional: source venv/bin/activate
python3 -m pip install --requirement requirements.txt
python3 -m pip install git+https://github.com/rafelafrance/traiter.git@master#egg=traiter
python -m spacy download en
```

## Run
```
./extract.py ... TODO ...
```

## Tests
Having a test suite is absolutely critical. The strategy I use is every new trait gets its own test set. Any time there is a parser error I add the parts that caused the error to the test suite and correct the parser. I.e. I use the standard red/green testing methodology.

You can run the tests like so:
```
cd /my/path/to/eforas_traiter
python -m unittest discover
```
