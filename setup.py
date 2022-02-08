import os
import glob
import requests
from shutil import copytree, rmtree, move

from cython_setuptools import cythonized_setup


def download(url, save_path):
    r = requests.get(url)
    with open(save_path , 'wb') as file:
        file.write(r.content)


source_dir = "app"
build_dir = "app_build"

if os.path.isdir(build_dir):
    rmtree(build_dir)
copytree(source_dir, build_dir)
# rmtree(os.path.join(build_dir, "SaigeAnomalyDetection/core/SaigeToolkit"))  # NOTE: exclude saige toolkit
cythonized_setup(build_dir)
rmtree("./build")
rmtree(source_dir)

backbones = {
    # f"{build_dir}/checkpoints/base.backbone": "https://download.pytorch.org/models/resnet18-5c106cde.pth",
}

for save_path, url in backbones.items():
    if not os.path.isfile(save_path):
        download(url, save_path)

keep = (
    "/__init__.py",
    ".so",
    f"{build_dir}/streamlit_app.py",
   *backbones.keys(),
    "/streamlit_pages/train/comments.yml",
    "/streamlit_pages/inspect/comments.yml",
)

# NOTE: remove scripts in package root (train, test, ..)
remove_list = (
    glob.glob(f"{build_dir}/*.so")
    + glob.glob(f"{build_dir}/SaigeAnomalyDetection/*.so")
    + glob.glob(f"{build_dir}/SaigeAnomalyDetection/internal_apps/*.so")
)
command = "tree ."
print(os.system(command))
file_list = []
for directory, sub_directories, fnames in os.walk(build_dir, followlinks=True):
    file_list += [os.path.join(directory, fname) for fname in fnames]
for file_path in file_list:
    if not file_path.endswith(keep) or file_path in remove_list:
        os.remove(file_path)
print(os.system(command))

move(build_dir, source_dir)
print(os.system(command))