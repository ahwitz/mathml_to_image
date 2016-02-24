# Author: Andrew Horwitz (ahwitz@gmail.com || github.com/ahwitz)
# Requires: conTeXt (http://wiki.contextgarden.net/ConTeXt_Standalone)
# Requires: ImageMagick
# ----Requires: GhostScript for PDF conversion in ImageMagick
# Requires: Pillow/PIL

import subprocess
import sys
import os
import os.path

from PIL import Image

# change the bash environment so context can be accessed
SETUPTEX_LOCATION = "/Applications/context/tex/setuptex" # recommended Mac install location
if not os.path.isfile(SETUPTEX_LOCATION):
	print("SETUPTEX_LOCATION in mathml2jpg.py is not a valid location. Please change.")
	sys.exit()

# all these will be overwritten
TEMPFILE_ROOT = "tmp/tempfile"
TEMPFILE_LOCATION = TEMPFILE_ROOT + ".tmp" 
TEMPFILE_PDF_LOCATION = TEMPFILE_ROOT + ".pdf"
TEMPFILE_JPG_LOCATION = TEMPFILE_ROOT + ".jpg"

"""
mathml_to_jpg: converts .mml at source_location to ImageMagick's interpretation of output_location's extension

Parameters:
	source_location: location of source .mml file
	output_location: location of output image file
	verbose=False (optional): print debug/progress statements
	overwrite=False (optional): overwrite output_location if it exists already
	newHeight=0 (optional): rescales output to newHeight if newHeight < height
	newWidth=0 (optional): rescales output to newWidth if newWidth < width

Returns: string error message if error, 0 if everything worked

"""
def mathml_to_jpg(source_location, output_location, verbose=False, overwrite=False, newHeight=0, newWidth=0):
	# check validity of source/output location
	if not os.path.isfile(source_location):
		return "Source location is not a file."
	if source_location[-3:] != "mml":
		return "Source location does not end in 'mml'."
	if not overwrite and os.path.isfile(output_location):
		return "Output location exists already."

	# load MathML
	mml_text = ""
	with open(source_location) as sf:
		mml_text = sf.read()

	# write the TeX wrapper
	with open(TEMPFILE_LOCATION, "w") as tf:
		tf.write("\\usemodule[mathml]\n")
		tf.write("\\setuppagenumbering[state=stop]\n") # surpresses page numbering
		tf.write("\\setuppapersize[letter,landscape]\n"); # landscape page, just in case we overdo it
		tf.write("\\starttext\n")
		tf.write("\\xmlprocessdata{}{\n")
		tf.write(mml_text)
		tf.write("}{}")
		tf.write("\\stoptext")


	if (verbose):
		print("Converting", source_location, "to pdf...")
	FNULL = open(os.devnull, 'w') # tell TeX to shut up
	# convert to pdf, requires source call to put "context" in the PATH
	context_status = subprocess.check_call(["bash", "-c", "source " + SETUPTEX_LOCATION + " && context " + TEMPFILE_LOCATION + " --purgeall --result=" + TEMPFILE_PDF_LOCATION], stdout=FNULL, stderr=subprocess.STDOUT)

	if (verbose):
		print("Converting", source_location, "to jpg...")
	# convert to jpg, density 400 is to make it look slightly purdier
	convert_status = subprocess.check_call(["convert", "-density", "400", TEMPFILE_PDF_LOCATION, TEMPFILE_JPG_LOCATION])

	if (verbose):
		print("Resizing", source_location)
	tmp_img = Image.open(TEMPFILE_JPG_LOCATION)

	def check_pixel(curX, curY):
		pixValue = tmp_img.getpixel((curX, curY))
		if pixValue < 10: # if it's black
			return True
		return False

	height = tmp_img.height
	width = tmp_img.width
	
	left = 0
	right = width
	upper = 0
	lower = height

	# TODO: optimize

	# check left
	if (verbose):
		print("Left...")
	check = False
	for left in range(0, width):
		for curY in range(0, height, 2):
			if check_pixel(left, curY):
				check = True
				break
		if check:
			break

	# check right
	if (verbose):
		print("...is", str(left), "and right...")
	check = False
	for curX in range(0, width):
		right = width - curX - 1
		for curY in range(0, height, 2):
			if check_pixel(right, curY):
				check = True
				break
		if check:
			break

	# check upper
	if (verbose):
		print("...is", str(right), "Upper...")
	check = False
	for upper in range(0, height):
		for curX in range(0, width, 2):
			if check_pixel(curX, upper):
				check = True
				break
		if check:
			break

	# check lower
	if (verbose):
		print("...is", str(upper), "Lower...")
	check = False
	for curY in range(0, height):
		lower = height - curY - 1
		for curX in range(0, width, 2):
			if check_pixel(curX, lower):
				check = True
				break
		if check:
			break

	if (verbose):
		print("...is", str(lower))

	tmp_img = tmp_img.crop((left, upper, right, lower))
	# TODO: add resize to newHeight/newWidth if smaller; if one is smaller, scale

	tmp_img.save(output_location)

	# TODO: remove temp PDF and JPGs

	return 0
