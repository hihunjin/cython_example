import os
from distutils.core import setup
from distutils.extension import Extension

from Cython.Build import cythonize


def scan_subdir(dir):
    """should be recursive if there are submodules inside modules"""
    subdirs = []
    for f in os.listdir(dir):
        if "ipynb_checkpoints" in f:
            continue
        p = os.path.join(dir, f)
        if f is not None and os.path.isdir(p) and not f.startswith(".") and not f.startswith("__"):
            subdirs.append(p.replace(os.path.sep, "."))
    return subdirs


def scandir(dir, files=[]):
    for f in os.listdir(dir):
        if f == "__init__.py" or "ipynb_checkpoints" in f:
            continue
        p = os.path.join(dir, f)
        if os.path.isfile(p) and p.endswith(".py"):
            files.append(p.replace(os.path.sep, ".")[:-3])
        elif os.path.isdir(p):
            scandir(p, files)
    return files


def make_extension(extension_name):
    extension_pat = extension_name.replace(".", os.path.sep) + ".py"
    return Extension(
        extension_name,
        [extension_pat],
        include_dirs=["."],
    )


def cythonized_setup(package):
    subdirs = scan_subdir(package)
    print("=======")
    print('\n'.join(subdirs))
    extension_names = scandir(package)
    extensions = [make_extension(name) for name in extension_names]
    print("=======")
    print('\n'.join([e.sources[0] for e in extensions]))

    setup(
        name=package,
        packages=subdirs,
        ext_modules=cythonize(
            extensions,
            compiler_directives={"language_level" : "3"},
        ),
    )


if __name__ == "__main__":
    package = "util"
    cythonized_setup(package)
