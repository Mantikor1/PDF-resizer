from setuptools import setup

APP = ["PDF_Resize.py"]
DATA_FILES = []
OPTIONS = {
    "argv_emulation": True,
    "iconfile": "icon.icns",  # optional
    "packages": [],
    "codesign_identity": None,
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)
