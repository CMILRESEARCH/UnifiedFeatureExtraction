
import logging
from modules.pipelines import Pipeline
from modules.ftu import FTUStruct   # Gloms, Tubules, Arteriols

from modules.extraction_utils.process_mc_features import process_glom_features, process_tubules_features, process_arteriol_features
from modules.extraction_utils.layer_dict import NAMES_DICT

class FeatureBuilder:
    def __init__(self):
        pass
    def build_feature(self):
        pass
class FTUFtr(FeatureBuilder):
    def __init__(self, config, item, MOD, layerName):
        self.config = config
        self.item = item
        self.layerName = layerName
        self.MOD = MOD
        # self.mask_xml = item.mask
        # self.slide = item.slide
        
    def build_feature(self):
        
        try:
                self.ftu
        except:
            self.ftu = FTUStruct()
        
        # Select which layer should be used
        if NAMES_DICT[self.layerName] == 3 or NAMES_DICT[self.layerName] == 4:  #3: non_globally_sclerotic_glomeruli
            
            feature_names = ['x1','x2','y1','y2','Area','Mesangial Area','Mesangial Fraction']
            all_features = process_glom_features(self.item.mask, 
                                                        NAMES_DICT[self.layerName], 
                                                        self.MOD, self.item.slide, 
                                                        mpp=self.item.slide.properties['tiffslide.mpp-x'], 
                                                        h_threshold=self.config['h_threshold'], 
                                                        saturation_threshold=self.config['saturation_threshold']
                                                        )            
            
        
        elif NAMES_DICT[self.layerName] == 5:  #5: 'tubules'
            
            feature_names = ['x1','x2','y1','y2','Average TBM Thickness','Average Cell Thickness','Luminal Fraction']
            
            all_features = process_tubules_features(self.item.mask, 
                                                        NAMES_DICT[self.layerName], 
                                                        self.MOD, self.slide, 
                                                        mpp=self.slide.properties['tiffslide.mpp-x'], 
                                                        whitespace_threshold=self.config['whitespace_threshold']
                                                        )
        
        elif NAMES_DICT[self.layerName] == 6:  #6: 'arteries/arterioles'
            
            feature_names = ['x1','x2','y1','y2','Arterial Area']
        
            all_features = process_arteriol_features(self.item.mask, 
                                                        NAMES_DICT[self.layerName], 
                                                        self.MOD, self.slide, 
                                                        mpp=self.slide.properties['tiffslide.mpp-x'])
            
        
        else:
            ValueError("Layer name is incorrect! please use 3...6")           
        
        if len(all_features) == 0:
            return {}
        i = 0
        for feature in feature_names:
            self.ftu.add_feature(feature, all_features[i])
            i += 1
        
        return self.ftu.features

         
class SayatPipeline(Pipeline):
    def __init__(self, config, item, layerName, MOD):        
        self.pipeline = "SayatPipeline"
        self.config = config
        self.item = item
        self.layerName = layerName
        self.MOD = MOD    
    
    def run(self, ftus):
        logging.warning(f"Pipeline: {self.pipeline} is starting")
        ftuftr = FTUFtr(self.config, self.item, self.MOD, self.layerName)

        # Build features on selected layer
        ftus.append(ftuftr.build_feature())
        print("Inside run:", ftus)