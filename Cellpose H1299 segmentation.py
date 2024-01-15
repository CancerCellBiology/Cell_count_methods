# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 18:25:44 2023

@author: attac
"""

from cellpose import models, io
import glob
import os
import shutil
import tifffile

model = models.CellposeModel(gpu=True, model_type = 'cyto2')

channels = [0,0]
dir_name = 'F:\\Microscopy\\H1299 method drugs staining\\72h\\Corrected'
diam=35
files= glob.glob(os.path.join(dir_name, '*ch00merged.tiff'))
imgs = [io.imread(filename) for filename in files]
masks, flows, styles = model.eval(imgs, diameter=diam, flow_threshold=0.6, cellprob_threshold=-2, channels=channels)
for i, file in enumerate(files):
    filename = os.path.join(dir_name, file.split('\\')[-1].replace('ch00merged', 'masks'))
    tifffile.imwrite(filename, masks[i])
    
diam=150
files= glob.glob(os.path.join(dir_name, '*ch00merged.tiff'))
imgs = [io.imread(filename) for filename in files]
masks, flows, styles = model.eval(imgs, diameter=diam, flow_threshold=0.6, cellprob_threshold=-2, channels=channels)
for i, file in enumerate(files):
    filename = os.path.join(dir_name, file.split('\\')[-1].replace('ch00merged', 'masksbig'))
    tifffile.imwrite(filename, masks[i])
    
diam=50
files= glob.glob(os.path.join(dir_name, '*ch00.tiff'))
imgs = [io.imread(filename) for filename in files]
masks, flows, styles = model.eval(imgs, diameter=diam, flow_threshold=0.6, cellprob_threshold=-2, channels=channels)
for i, file in enumerate(files):
    filename = os.path.join(dir_name, file.split('\\')[-1].replace('ch00', 'masksmito'))
    tifffile.imwrite(filename, masks[i])

    
