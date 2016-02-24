# Author: Andrew Horwitz (ahwitz@gmail.com || github.com/ahwitz)
# Requires: conTeXt (http://wiki.contextgarden.net/ConTeXt_Standalone)
# Requires: ImageMagick
# ----Requires: GhostScript for PDF conversion in ImageMagick

import subprocess
import sys
import os
import os.path

# change the bash environment so context can be accessed
SETUPTEX_LOCATION = "/Applications/context/tex/setuptex" # recommended Mac install location
if not os.path.isfile(SETUPTEX_LOCATION):
	print("SETUPTEX_LOCATION in mathml2jpg.py is not a valid location. Please change.")
	sys.exit()

# all these will be overwritten
TEMPFILE_ROOT = "tmp/tempfile"
TEMPFILE_LOCATION = TEMPFILE_ROOT + ".tmp" 
TEMPFILE_PDF_LOCATION = TEMPFILE_ROOT + ".pdf"

"""
mathml_to_jpg: converts .mml at source_location
 returns string error message if error, 0 if everything worked

"""
def mathml_to_jpg(source_location, output_location, verbose=False, overwrite=False, newSize=""):
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
	convert_status = subprocess.check_call(["convert", "-density", "400", TEMPFILE_PDF_LOCATION, output_location]) # TODO: add resize to newSize

	#TODO: PIL

	return 0
