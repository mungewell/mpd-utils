from cx_Freeze import setup, Executable

base = None    

executables = [Executable("mpd218_pad2keys.py", base=base)]

packages = ["idna", "mido", "rtmidi_python", "keyboard", "sys"]
options = {
    'build_exe': {    
        'packages':packages,
        'excludes':["pygame", "numpy"],
    },    
}

setup(
    name = "mpd218_pad2keys.py",
    options = options,
    version = "0.1.0.0",
    description = 'Work around for the lack of proper MPD218 driver in MPC Essentials',
    executables = executables
)
