import os
import unittest
import problems

tests = []
dirname = os.path.dirname(os.path.realpath(__file__))
for f in os.listdir(dirname):
	if os.path.isdir(os.path.join(dirname, f)):
		try:
			__import__('problems.%s' % f)
			exec('tests.append(problems.%s.tests())' % f)
		except:
			pass

def suite():
	return unittest.TestSuite(tests)
