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
import warnings


def blender_job(blender_root, save_folder, dataset_folder, synset, file, obj_scale, views, kappa, polar_loc):
    render_cmd = '"%s" -b -P render_shapenet.py -- --output %s %s  --scale %f --views 24 --resolution 1024 --use_von_mises_camera %s --kappa %s --polar_loc %s >> tmp.out' % (
        blender_root,
        save_folder,
        os.path.join(dataset_folder, synset, file, 'model.obj'),
        obj_scale,
        views,
        args.use_von_mises_camera,
        " ".join(str(x) for x in kappa),
        " ".join(str(x) for x in polar_loc)
    )
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
    '--data_subfolder', type=str, default=None,
    help='path for synset subfolder')
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

###### Added for reliefs
parser.add_argument(
    '--use_von_mises_camera', type=bool, default=False,
    help='Whether we are using the special relief camera')
parser.add_argument(
    '--kappa', nargs=2, type=float, default=(1.0, 1.0),
    help='If we are using reliefs, the concentrations of the von mises distributions')
parser.add_argument(
    '--polar_loc', nargs=2, type=float, default=(1.0, 0.0),
    help='If we are using reliefs, the centers of the von mises distributions')

save_folder = args.save_folder
dataset_folder = args.dataset_folder
blender_root = args.blender_root
views = args.views
data_subfolder = args.data_subfolder 

#overwrite synset if subfolder is given:
if data_subfolder is not None:
    synset_list = [data_subfolder]
    scale_list = [0.8]    

tp = ThreadPool(args.worker)
for synset, obj_scale in zip(synset_list, scale_list):
    file_list = sorted(os.listdir(os.path.join(dataset_folder, synset)))
    for idx, file in enumerate(file_list):
        #check if already rendered:
        check_path = os.path.join(save_folder, "img", synset, file, 'transforms.json')
        if not os.path.exists(check_path):
            tp.apply_async(blender_job, (blender_root, save_folder, dataset_folder, synset, file, obj_scale, views))
        else:
            print(check_path + " skipped, because it already exists", flush=True)

tp.close()
tp.join()