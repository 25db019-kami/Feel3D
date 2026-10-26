import sys
import os
import pickle
import inspect

# chumpy互換パッチ
if not hasattr(inspect, "getargspec"):
    inspect.getargspec = inspect.getfullargspec

import torch
import smplx
import trimesh
import numpy as np

# 1. モデルの読み込み設定
model_path = 'P:/コンテスト/models'
gender = 'neutral'

# smplxのモデル読み込み
model = smplx.create(
    model_path=model_path, 
    model_type='smpl', 
    gender=gender
)

weight = float(sys.argv[1])

print("体重:", weight)
print("SMPLモデルを読み込んでいます...")

betas = torch.zeros([1, 10], dtype=torch.float32)

weight = float(sys.argv[1])
height = float(sys.argv[2])
chest = float(sys.argv[3])
waist = float(sys.argv[4])
hip = float(sys.argv[5])

betas = torch.zeros([1, 10], dtype=torch.float32)

# 体重
betas[0,0] = (weight - 55) / 10

# 身長
betas[0,1] = (height - 160) / 20

# 胸囲
betas[0,2] = (chest - 85) / 10

# ウエスト
betas[0,3] = (waist - 70) / 10

# ヒップ
betas[0,4] = (hip - 90) / 10

zero_pose = torch.zeros([1, 69], dtype=torch.float32)

base_output = model(
    betas=betas,
    body_pose=zero_pose,
    return_verts=True
)
base_verts = base_output.vertices.detach().cpu().numpy()[0]
faces = model.faces

# 3. Trimeshの構築
mesh = trimesh.Trimesh(vertices=base_verts, faces=faces, process=False)

# 5. OBJ書き出し

output_obj_path = (
    f'P:/コンテスト/'
    f'smpl_{int(weight)}kg_'
    f'{int(chest)}c_'
    f'{int(waist)}w_'
    f'{int(hip)}h.obj'
)

mesh.export(output_obj_path)

print(f"✅ OBJ出力成功: {output_obj_path}")