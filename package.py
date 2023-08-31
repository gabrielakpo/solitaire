name = "solitaire"

version = "1.0.0"

requires = [
    "python",
    "PySide2"
]

def commands():
    global env
    env.PYTHONPATH.prepend("{root}/python")