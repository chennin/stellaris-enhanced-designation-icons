# Enhanced Designation Icons [![Get it from the Workshop](https://img.shields.io/badge/steam-%23000000.svg?style=for-the-badge&logo=steam&logoColor=white)](https://steamcommunity.com/sharedfiles/filedetails/?id=2941285632)

This mod replaces planetary designation icons with their vanilla resource icons, and enhances some to make them stand out more.

* Generator, urban, unification, etc icons are replaced with their resource
* Vanilla prison, fortress, etc icons are given a more prominent edge and/or brightened
* Habitat resource icons are bigger

No art was done during the making of this mod.

# Building

## Requirements

* Python 3
* Pillow (python3-pil) 8.3+
* The game files (this mod uses only game assets to make its graphics). If you're running this, replace the paths at the top of `designationicons.py`.

Run:

`./designationicons.py`

# Uploading

```
STEAMUSER=
podman run -v $PWD:/code:ro -v steamcmd-data:/data -v steamcmd-root:/root/.local/share/Steam -it steamcmd/steamcmd:debian-12 \
  +login $STEAMUSER +workshop_build_item /code/steamcmd.txt +quit
```

# Copyright

Art is Copyright © 2014 Paradox Interactive AB. www.paradoxplaza.com.

Python code is copyright me and licensed under the MIT License.
