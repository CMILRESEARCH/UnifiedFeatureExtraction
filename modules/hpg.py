import os
import random  
import string  
from tiffslide import TiffSlide
import xml.etree.ElementTree as ET

# from modules.extraction_utils.xml_to_json import convert_xml_json
from modules.extraction_utils.layer_dict import NAMES_DICT
from modules.extraction_utils.extract_ffpe_features import xml_to_mask

class HPG:
    def __init__(self, config):
        self.config = config
        

class HPGFolder(HPG):
    def __init__(self, config):
        super().__init__(config)
        self.items = self.getItemsInHpgFolder()
    
    def getItemsInHpgFolder(self):
        
        image_files = os.listdir(self.config['input_dir'])
        image_names = [os.path.join(self.config['input_dir'], f.split('.')[0]) for f in image_files]
        
        # each item in items is a tuple of (images, annotations)
        items = [(f + self.config['ext'], f + '.xml') for f in image_names]
        
        return items
    
class HPGItem(HPG):
    def __init__(self, config, svsfile, xmlfile, layerNames):
        super().__init__(config)
        self.svsfile = svsfile
        self.xmlfile = xmlfile   
        self.layerNames = layerNames       
        self.slide = self.getSlide()
        self.mask = self.getMask()
        self.ftus = []
    
    def convert_xml_json(self, names=['cortical_interstitium', 
                                      'medullary_interstitium',
                                      'non_globally_sclerotic_glomeruli',
                                      'globally_sclerotic_glomeruli',
                                      'tubules',
                                      'arteries/arterioles'],
                         colorList=None, alpha=0.4):
        
        root = ET.parse(self.xmlfile)#.getroot()
        
        if colorList == None:
            colorList = ["rgb(0, 255, 128)", "rgb(0, 255, 255)", "rgb(255, 255, 0)", "rgb(255, 128, 0)", "rgb(0, 128, 255)",
                        "rgb(0, 0, 255)", "rgb(0, 102, 0)", "rgb(153, 0, 0)", "rgb(0, 153, 0)", "rgb(102, 0, 204)",
                        "rgb(76, 216, 23)", "rgb(102, 51, 0)", "rgb(128, 128, 128)", "rgb(0, 153, 153)", "rgb(0, 0, 0)"]
            
        anns = root.findall('Annotation')
        
        assert len(anns) <= len(names)

        data = []
        for n, child in enumerate(anns):
            dataDict = dict()
            name = names[n]
            # create a random if (mimic file_id)            
            letter_count = 10
            digit_count = 5
            str1 = ''.join((random.choice(string.ascii_letters) for x in range(letter_count)))  
            str1 += ''.join((random.choice(string.digits) for x in range(digit_count)))  
        
            sam_list = list(str1) # it converts the string to list.  
            random.shuffle(sam_list) # It uses a random.shuffle() function to shuffle the string.  
            id = ''.join(sam_list)
            
            _ = os.system("printf 'Building JSON layer: [{}]\n'".format(name))
            element = []
            reg = child.find('Regions')
            for i in reg.findall('Region'):
                eleDict = dict()
                eleDict["closed"] = True

                lineColor = colorList[n % len(colorList)]
                eleDict["lineColor"] = lineColor

                fillColor = lineColor[:3]+'a'+lineColor[3:-1] + f', {alpha})'
                eleDict["fillColor"] = fillColor

                eleDict["lineWidth"] = 2
                points = []
                ver = i.find('Vertices')
                Verts = ver.findall('Vertex')
                if len(Verts) <= 1:
                    continue # skip if only 1 vertex points
                for j in Verts:
                    eachPoint = []
                    eachPoint.append(float(j.get('X')))
                    eachPoint.append(float(j.get('Y')))
                    eachPoint.append(float(j.get('Z')))
                    points.append(eachPoint)
                eleDict["points"] = points
                eleDict["type"] = "polyline"
                eleDict["id"] = id
                element.append(eleDict)
                
            dataDict["elements"] = element
            dataDict["name"] = name
            
            data.append({"annotation": dataDict})

        return data
    
    def getAnnotations(self):
                        
        annotations = self.convert_xml_json()
            
        annotations_filtered = [annot for annot in annotations if annot['annotation']['name'] in self.layerNames]
        
        print(len(annotations_filtered))

        return annotations_filtered
    def getSlide(self):
        slide = TiffSlide(self.svsfile)
        self.slidedim = slide.dimensions
        return slide
    
    def getMask(self):
        return xml_to_mask(self.getAnnotations(),
                           (0,0), 
                           self.slidedim,
                           downsample_factor=self.config['downsample_factor'],
                           verbose=1
                        )