## mathml2jpg.py
Author: Andrew Horwitz (ahwitz@gmail.com || github.com/ahwitz)

Requirements:
- conTeXt (http://wiki.contextgarden.net/ConTeXt_Standalone)
- ImageMagick
-- GhostScript for PDF conversion in ImageMagick

TODO after requirement installation:
- Set SETUPTEX_LOCATION in mathml2jpg.py to installation location of context/bin/setuptex from conTeXt installation
- Change TMPFILE_ROOT location as needed

Parameters:
- source_location: location of source .mml file
- output_location: location of output image file
- verbose=False (optional): print debug/progress statements
- overwrite=False (optional): overwrite output_location if it exists already
- new_size=None (optional): new size, as parameter to convert -resize

Returns: string error message if error, 0 if everything worked
