from cx_Freeze import setup, Executable

base = None    

executables = [Executable("main.py", base=base)]

packages = ["sys", "tkinter", "pygame"]
options = {
    'build_exe': {
        'packages':packages
    }
}

setup(
    name = "Arkarealis",
    options = options,
    version = "0.0.1",
    description = 'Arkarealis, a video game project',
    executables = executables
)
