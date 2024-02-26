import os
import numpy as np
import pandas as pd
from argparse import ArgumentParser
# from modules.ftu import FTU
from modules.hpg import HPGFolder, HPGItem
from modules.sayatpipeline import SayatPipeline

MODx=np.zeros((3,))
MODy=np.zeros((3,))
MODz=np.zeros((3,))
MODx[0]= 0.644211
MODy[0]= 0.716556
MODz[0]= 0.266844

MODx[1]= 0.175411
MODy[1]= 0.972178
MODz[1]= 0.154589

MODx[2]= 0.0
MODy[2]= 0.0
MODz[2]= 0.0
MOD=[MODx,MODy,MODz]
NAMES = ['non_globally_sclerotic_glomeruli','globally_sclerotic_glomeruli','tubules','arteries/arterioles']
# NAMES = [3, 4, 5, 6]
compart_names = ['gloms','s_gloms','tubs','arts']

def main():
    
    parser = ArgumentParser(description="Input file")
    
    parser.add_argument("--input_dir", type=str, default='/blue/pinaki.sarder/f.afsari/1_SKorea_Project/imageData/MCD/', help="base dir")
    parser.add_argument("--output_dir", type=str, default='/blue/pinaki.sarder/f.afsari/1_SKorea_Project/Features/', help="output dir")
    parser.add_argument("--downsample_factor", type=float, default=1.0, help="downsample factor")    
    parser.add_argument("--h_threshold", type=float, default=160, help="h threshold")
    parser.add_argument("--whitespace_threshold", type=float, default=0.88, help="whitespace threshold")
    parser.add_argument("--saturation_threshold", type=float, default=0.3, help="saturation threshold")
    parser.add_argument("--ext", type=str, default='.svs', help="WSI type")
    
    args = parser.parse_args()
    
    config = vars(args)
    
    outdir = config['output_dir']
    
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    
    dataFolder = HPGFolder(config)
    items = dataFolder.items
    
    for i in range(len(items)):
        
        svsfile, xmlfile = items[i]        
        
        item = HPGItem(config, svsfile, xmlfile, NAMES)
        
        all_comparts = []
        for layerName in NAMES:
            
            pipeline = SayatPipeline(config, item, layerName, MOD)
            print("Before run:", item.ftus)
            pipeline.run(item.ftus)
            print("After run:", item.ftus)
            all_comparts.extend(item.ftus)
            
        # write each layer's feature in a seperate sheet of the output Excel file
        output_filename = os.path.join(args.output_dir, os.path.basename(svsfile).split('.')[0] + '.xlsx')
        print("printf '\tWriting Excel file: [{}]\n'".format(output_filename))
        with pd.ExcelWriter(output_filename) as writer:
            for _, compart in enumerate(all_comparts):
                df = pd.DataFrame(compart)
                df.to_excel(writer, index=False, sheet_name=layerName)
        print("All Layers Done!")
        
if __name__ == "__main__":
    main()