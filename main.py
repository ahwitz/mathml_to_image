# Author: Andrew Horwitz (ahwitz@gmail.com || github.com/ahwitz)
# Import/run example for mathml2jpg.py

from mathml2jpg import mathml_to_jpg

res = mathml_to_jpg("examples/Orgel 484_945.mml", "testout.jpg", overwrite=True, verbose=True)
if res != 0:
	print(res)