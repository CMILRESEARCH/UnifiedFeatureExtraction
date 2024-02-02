import os

from modules.dsa import DSA
from modules.slide import Slide

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





    