# Author: Andrew Horwitz (ahwitz@gmail.com || github.com/ahwitz)
# Requires: conTeXt (http://wiki.contextgarden.net/ConTeXt_Standalone)
# Requires: ImageMagick
# ----Requires: GhostScript for PDF conversion in ImageMagick
# Requires: Pillow/PIL

import subprocess
import sys
import os
import os.path
import time

# change the bash environment so context can be accessed
SETUPTEX_LOCATION = "/Applications/context/tex/setuptex" # recommended Mac install location
if not os.path.isfile(SETUPTEX_LOCATION):
	print("SETUPTEX_LOCATION in mathml2jpg.py is not a valid location. Please change.")
	sys.exit()

# location to drop all temp files. No terminal slash.
TEMPDIR_LOCATION = "tmp"

"""
mathml_to_jpg: converts .mml at source_location to ImageMagick's interpretation of output_location's extension

Parameters:
	source_location: location of source .mml file. Should be absolute.
	output_location: location of output image file. Should be absolute.
	verbose=False (optional): print debug/progress statements
	overwrite=False (optional): overwrite output_location if it exists already
	new_size=None (optional): new size, as parameter to convert -resize

Returns: string error message if error, 0 if everything worked

"""
def mathml_to_jpg(source_location, output_location, verbose=False, overwrite=False, new_size=None):
	# check validity of source/output location
	if not os.path.isfile(source_location):
		return "Source location is not a file."
	if source_location[-3:] != "mml":
		return "Source location does not end in 'mml'."
	if not overwrite and os.path.isfile(output_location):
		return "Output location exists already."

	# temp locations
	TEMPFILE_ROOT = "tempfile-" + str(int(time.time() * 1000000))
	TEMPFILE_LOCATION = TEMPFILE_ROOT + ".tex" 
	TEMPFILE_LOCATION_WDIR = TEMPDIR_LOCATION + "/" + TEMPFILE_LOCATION
	TEMPFILE_PDF_LOCATION = TEMPFILE_ROOT + ".pdf"
	TEMPFILE_PDF_LOCATION_WDIR = TEMPDIR_LOCATION + "/" + TEMPFILE_PDF_LOCATION

	# load MathML
	mml_text = ""
	with open(source_location) as sf:
		mml_text = sf.read()

	# write the TeX wrapper
	with open(TEMPFILE_LOCATION_WDIR, "w") as tf:
		tf.write("\\usemodule[mathml]\n")
		tf.write("\\setuppagenumbering[state=stop]\n") # surpresses page numbering
		tf.write("\\setuppapersize[letter,landscape]\n"); # landscape page, just in case we overdo it
		tf.write("\\starttext\n")
		tf.write("\\xmlprocessdata{}{\n")
		tf.write(mml_text)
		tf.write("}{}")
		tf.write("\\stoptext")

	# change working dir to dump conTeXt temp files in a safer place
	origdir = os.getcwd()
	os.chdir(TEMPDIR_LOCATION)
	if (verbose):
		print("Converting", source_location, "to pdf...")
	FNULL = open(os.devnull, 'w') # tell TeX to shut up
	# convert to pdf, requires source call to put "context" in the PATH
	try:
		subprocess.check_call(["bash", "-c", "source " + SETUPTEX_LOCATION + " && context " + TEMPFILE_LOCATION + " --purgeall --result=" + TEMPFILE_PDF_LOCATION], stdout=FNULL, stderr=subprocess.STDOUT)
	except subprocess.CalledProcessError:
		return "Call to conTeXt failed."
	os.chdir(origdir)

	if (verbose):
		print("Converting", source_location, "to jpg...")

	# convert to jpg, density 400 is to make it look slightly purdier
	convert_list = ["convert", "-density", "400", "-trim", "-alpha", "remove"]
	if (new_size != None):
		convert_list += ["-resize", new_size]
	convert_list += [TEMPFILE_PDF_LOCATION_WDIR, output_location]
	try:
		subprocess.check_call(convert_list)
	except subprocess.CalledProcessError:
		return "Call to convert failed."

	# remove temp files
	os.remove(TEMPFILE_PDF_LOCATION_WDIR)
	os.remove(TEMPFILE_LOCATION_WDIR)

	return 0
