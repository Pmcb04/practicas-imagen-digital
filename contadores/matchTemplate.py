import cv2
import numpy as np
import os
from matplotlib import pyplot as plt
import MTM
import pandas as pd


class MatchTemplate:

    templates = []

    def __init__(self):

        self.templates.clear()
        
        image_folder = "./templates"
        for filename in os.listdir(image_folder):
            template_img = cv2.imread(os.path.join(image_folder, filename))
            template_img = cv2.cvtColor(template_img, cv2.COLOR_BGR2GRAY)
            self.templates.append((filename.split('.')[0], template_img))

        # for template in self.templates:
        #     print(template[0])

        # print("---------------------------")

    def doMatch(self, input_img):

        import MTM
        from MTM import matchTemplates
        hits = matchTemplates(
                            self.templates,
                            input_img,
                            score_threshold=0.5,
                            searchBox=(0, 0, 3000, 750),
                            method=cv2.TM_CCOEFF_NORMED,
                            maxOverlap=0.1)
                
        
        return str(hits.get("TemplateName").values[0])

