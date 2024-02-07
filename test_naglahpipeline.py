import cv2
import os
from modules.naglahpipeline import NaglahPipeline, Tubule, Segmnt, EpmFtr, LmnFtr, TbmFtr

def getPatchMask(impath):
    
    def splitIm(im):
        if len(im.shape)==3:
            _, w, _ = im.shape
            patch = im[:, :w//2, :]
            mask = im[:, w//2:, :]
        else:
            _, w = im.shape
            patch = im[:, :w//2]
            mask = im[:, w//2:]
        return patch, mask
    
    im = cv2.imread(impath, 3)
    patch, mask = splitIm(im)

    return patch, mask

if __name__=="__main__":

    config = {
        'svsBase' : "/blue/pinaki.sarder/nlucarelli/kpmp_new",
        'name' : 'S-1904-007292_PAS_2of2.svs',
        'fid' : "65947419bd96faac30b20352",
        'fg_annotationLayer': 'tubules',
        'outputdir': '/orange/pinaki.sarder/ahmed.naglah/data/kpmp_project',
        'outputfile': '007292_PAS_2of2_updates_optics.csv',
        'dsa_anno_name': 'morpho_epithelium_clusters_optics'
    }

    ftrs = {}
    all_tubules = [{'tid': 122}]

    for i in range(len(all_tubules)):
        
        tid = all_tubules[i]['tid']

        impath = '/orange/pinaki.sarder/ahmed.naglah/data/kpmp_project/testPatchImageEpithelium.png' 
        
        patch, mask = getPatchMask(impath)
        
        tubule = Tubule(config, patch, mask)

        segment = Segmnt()
        extract_epm = EpmFtr()
        extract_lmn = LmnFtr()
        extract_tbm = TbmFtr()

        pipeline = NaglahPipeline(config, [segment,
                                extract_epm, 
                                extract_lmn, 
                                extract_tbm])

        pipeline.run(tubule)
        
        ftrs[tid] = tubule.features

        print("Tubule: ", tubule.features)
        
    print(ftrs)