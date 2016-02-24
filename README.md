## mathml2jpg.py
Author: Andrew Horwitz (ahwitz@gmail.com || github.com/ahwitz)

Requirements:
- conTeXt (http://wiki.contextgarden.net/ConTeXt_Standalone)
- ImageMagick
-- GhostScript for PDF conversion in ImageMagick
- Pillow/PIL

TODO after requirement installation:
- Set SETUPTEX_LOCATION in mathml2jpg.py to installation location of context/bin/setuptex from conTeXt installation
- Change TMPFILE_ROOT location as needed

Parameters:
- source_location: location of source .mml file
- output_location: location of output image file
- verbose=False (optional): print debug/progress statements
- overwrite=False (optional): overwrite output_location if it exists already
- newHeight=0 (optional): rescales output to newHeight if newHeight < height
- newWidth=0 (optional): rescales output to newWidth if newWidth < width

Returns: string error message if error, 0 if everything worked
