import os
import logging
from modules.ftu import Tubule
from modules.dsa import DSAFolder, DSAItem
from modules.naglahpipeline import NaglahPipeline, Segmnt, EpmFtr, LmnFtr, TbmFtr

if __name__=="__main__":
    config = {
        'svsBase' : "/blue/pinaki.sarder/nlucarelli/kpmp_new",
        'fid' : "659eb008bd96faac30b68fff",
        'layerName': 'tubules',
        'outputdir': '/orange/pinaki.sarder/ahmed.naglah/data/unified',
        'username': 'ahmednaglah',
        'password': '',
        'apiUrl': 'https://athena.rc.ufl.edu/api/v1',
        'masked': True,
        'fixedSize': True,
        'name': 'tubulePipeline'
    }

    dsaFolder = DSAFolder(config)
    items = dsaFolder.items

    for i in range(len(items)):
        fid, svsname = items[i]
        item = DSAItem(config, fid, svsname)

        tubules = item.getTubules()

        for j in range(len(tubules)):
            tubule = tubules[j]

            segment = Segmnt()
            extract_epm = EpmFtr()
            extract_lmn = LmnFtr()
            extract_tbm = TbmFtr()

            pipeline = NaglahPipeline(config, [segment,
                                    extract_epm, 
                                    extract_lmn, 
                                    extract_tbm])

            pipeline.run(tubule)
            print("here...")