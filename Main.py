import sys

from pass_one import first_pass
from pass_two import second_pass

try:
	first_pass()
	second_pass()

except Exception as e:
	print(e)