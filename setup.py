from distutils.core import setup
import py2exe, os, pygame
origIsSystemDLL = py2exe.build_exe.isSystemDLL
def isSystemDLL(pathname):
    if os.path.basename(pathname).lower() in ["sdl_ttf.dll"]:
        return 0
    return origIsSystemDLL(pathname)
py2exe.build_exe.isSystemDLL = isSystemDLL
pygamedir = os.path.split(pygame.base.__file__)[0]
os.path.join(pygamedir, pygame.font.get_default_font()),
os.path.join(pygamedir, 'SDL.dll'),
os.path.join(pygamedir, 'SDL_ttf.dll')

setup(
        console=["pick_a_number.py"],
        options={
                "py2exe":{
                        "packages": ["pygame"]
                }
        }
)
