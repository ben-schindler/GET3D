# Copyright (c) 2022, NVIDIA CORPORATION & AFFILIATES.  All rights reserved.
#
# NVIDIA CORPORATION & AFFILIATES and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION & AFFILIATES is strictly prohibited.

import os
import argparse
from multiprocessing.pool import ThreadPool

def blender_job(blender_root, save_folder, dataset_folder, synset, file, obj_scale, views):
    render_cmd = '%s -b -P render_shapenet.py -- --output %s %s  --scale %f --views %d --resolution 1024 >> tmp.out' % (
        blender_root, 
        save_folder, 
        os.path.join(dataset_folder, synset, file, 'model.obj'), 
        obj_scale, 
        views)
    os.system(render_cmd)

synset_list = [
    'Version1'  # Gray_Checkerboard
]
scale_list = [
    0.8
]
parser = argparse.ArgumentParser(description='Renders given obj file by rotation a camera around it.')
parser.add_argument(
    '--save_folder', type=str, default='./tmp',
    help='path for saving rendered image')
parser.add_argument(
    '--dataset_folder', type=str, default='./tmp',
    help='path for downloaded 3d dataset folder')
parser.add_argument(
    '--blender_root', type=str, default='./tmp',
    help='path for blender')
parser.add_argument(
    '--views', type=int, default=24,
    help='number of views')
parser.add_argument(
    '--worker', type=int, default=1,
    help='number of blender-workers')
args = parser.parse_args()

save_folder = args.save_folder
dataset_folder = args.dataset_folder
blender_root = args.blender_root
views = args.views

tp = ThreadPool(args.worker)
for synset, obj_scale in zip(synset_list, scale_list):
    file_list = sorted(os.listdir(os.path.join(dataset_folder, synset)))
    for idx, file in enumerate(file_list):
        tp.apply_async(blender_job, (blender_root, save_folder, dataset_folder, synset, file, obj_scale, views))

tp.close()
tp.join()