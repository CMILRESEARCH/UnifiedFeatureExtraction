import os
import logging
from modules.ftu import Tubule
from modules.dsa import DSAFolder, DSAItem
from modules.naglahpipeline import NaglahPipeline, Segmnt, EpmFtr, LmnFtr, TbmFtr

import pandas as pd
import argparse

parser = argparse.ArgumentParser(
                    prog='DSA FTU Annotations to Patches',
                    description='Extract DSA FTU Annotations to Patches',
                    epilog='Text at the bottom of help')

parser.add_argument('--svsBase', help='/blue/pinaki.sarder/...')     
parser.add_argument('--fid', help='659eb008bd96faac30b68fff')     
parser.add_argument('--layerName', help='tubules')         
parser.add_argument('--outputdir', help='/orange/pinaki.sarder/ahmed.naglah/...')     
parser.add_argument('--username', help='username')     
parser.add_argument('--password', help='password')     
parser.add_argument('--apiUrl', help='https://athena.rc.ufl.edu/api/v1')   
parser.add_argument('--name', help='a name for the pipeline', default='defaultNaglahPipeline')     

args = parser.parse_args()

config = vars(args)

outdir = config['outputdir']

if not os.path.exists(outdir):
    os.mkdir(outdir)

dsaFolder = DSAFolder(config)
items = dsaFolder.items

for i in range(len(items)):

    fid, svsname = items[i]
    try:

        item = DSAItem(config, fid, svsname)

        tubules = item.getTubules()

        out = []

        for j in range(len(tubules)):
            try:

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

                out_ = tubule.features.copy()
                out_['ftu_id'] = j
                out_['slide_id'] = i
                out_['slide_name'] = svsname
                out_['x'] = int(tubule.bb['x'])
                out_['y'] = int(tubule.bb['y'])
                out_['w'] = int(tubule.bb['w'])
                out_['h'] = int(tubule.bb['h'])

                out.append(out_)
            except:
                logging.warning(f"error in ftu #{j} in item #{i} fid {svsname} svsname {svsname}")

        df = pd.DataFrame(out)
        df.to_csv(f"{outdir}/{svsname.replace('.svs', '.csv')}", header=True)
    except:
        logging.warning(f"error in item #{i} fid {svsname} svsname {svsname}")

    
if __name__=="__main__":
    config = {
        'svsBase' : "/blue/pinaki.sarder/",
        'fid' : "659eb008bd96faac30b68fff",
        'layerName': 'tubules',
        'outputdir': '/orange/pinaki.sarder/ahmed.naglah/data/unified/out1',
        'username': '',
        'password': '',
        'apiUrl': 'https://athena.rc.ufl.edu/api/v1',
        'name': 'tubulePipeline'
    }

    outdir = config['outputdir']

    if not os.path.exists(outdir):
        os.mkdir(outdir)

    dsaFolder = DSAFolder(config)
    items = dsaFolder.items

    for i in range(len(items)):

        fid, svsname = items[i]
        try:

            item = DSAItem(config, fid, svsname)

            tubules = item.getTubules()

            out = []

            for j in range(len(tubules)):
                try:

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

                    out_ = tubule.features.copy()
                    out_['ftu_id'] = j
                    out_['slide_id'] = i
                    out_['slide_name'] = svsname
                    out_['x'] = int(tubule.bb['x'])
                    out_['y'] = int(tubule.bb['y'])
                    out_['w'] = int(tubule.bb['w'])
                    out_['h'] = int(tubule.bb['h'])

                    out.append(out_)
                except:
                    logging.warning(f"error in ftu #{j} in item #{i} fid {svsname} svsname {svsname}")

            df = pd.DataFrame(out)
            df.to_csv(f"{outdir}/{svsname.replace('.svs', '.csv')}", header=True)
        except:
            logging.warning(f"error in item #{i} fid {svsname} svsname {svsname}")