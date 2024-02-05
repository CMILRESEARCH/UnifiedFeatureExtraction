import os

from modules.dsa import DSA
from modules.slide import Slide

import argparse

parser = argparse.ArgumentParser(
                    prog='DSA FTU Annotations to Patches',
                    description='Extract DSA FTU Annotations to Patches',
                    epilog='Text at the bottom of help')

parser.add_argument('--svsDir', help='/blue/pinaki.sarder/...')     
parser.add_argument('--annoDir', help='/blue/pinaki.sarder/...')     
parser.add_argument('--layer', help='non_globally_sclerotic_glomeruli')     
parser.add_argument('--pipeline', help='nick; sam; ahmed; sayat; hovernet;')     
parser.add_argument('--annoSource', help='hpg or athena')     

parser.add_argument('--fid', help='659eb008bd96faac30b68fff')     
parser.add_argument('--layerName', help='non_globally_sclerotic_glomeruli')     
parser.add_argument('--outputdir', help='/orange/pinaki.sarder/ahmed.naglah/...')     
parser.add_argument('--username', help='username')     
parser.add_argument('--password', help='password')     
parser.add_argument('--apiUrl', help='https://athena.rc.ufl.edu/api/v1')     
parser.add_argument('--masked', help='Apply ftu mask on patch')     
parser.add_argument('--fixedSize', help='Extract fixed sized with max w and h')     

args = parser.parse_args()

if __name__=='__main__':
    config = {
    }

    dsa = DSA(config)

    slides = []

    for i in range(len(slides)):

        slide = slides[i]

        s = Slide(config, slide)

        s.extractFTUs()

        s.runFeatureExtraction(config)

        s.exportFeatures(config)