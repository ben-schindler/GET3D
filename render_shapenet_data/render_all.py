# Copyright (c) 2022, NVIDIA CORPORATION & AFFILIATES.  All rights reserved.
#
# NVIDIA CORPORATION & AFFILIATES and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION & AFFILIATES is strictly prohibited.

import os
import argparse

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

args = parser.parse_args()

save_folder = args.save_folder
dataset_folder = args.dataset_folder
blender_root = args.blender_root

synset_list = [
    '02958343',  # Car
    '03001627',  # Chair
    '03790512'  # Motorbike
    # 'reliefs'  # Reliefs
]
scale_list = [
    0.9,
    0.7,
    0.9
]
for synset, obj_scale in zip(synset_list, scale_list):
    file_list = sorted(os.listdir(os.path.join(dataset_folder, synset)))
    for idx, file in enumerate(file_list):
        render_cmd = '"%s" -b -P render_shapenet.py -- --output %s %s  --scale %f --views 24 --resolution 1024 --use_von_mises_camera %s --kappa %s --polar_loc %s >> tmp.out' % (
            blender_root, save_folder, os.path.join(dataset_folder, synset, file, 'model.obj'), obj_scale,
            args.use_von_mises_camera, " ".join(str(x) for x in args.kappa), " ".join(str(x) for x in args.polar_loc)
        )
        os.system(render_cmd)
