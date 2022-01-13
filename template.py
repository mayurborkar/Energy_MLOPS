import os

dir = [
    os.path.join("data", "raw"),
    os.path.join("data", "processed"),
    "notebooks",
    "saved_model",
    "src"
]

for dir_ in dir:
    os.makedirs(dir_, exist_ok=True)
    with open(os.path.join(dir_, ".gitkeep"), "w") as f:
        pass

file = [
    os.path.join("src", "__init__.py"),
    "dvc.yaml",
    "params.yaml",
]

for file_ in file:
    with open(file_, "w") as f:
        pass