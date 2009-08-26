import unittest
from problems.example_library import problem1, problem2, problem3

class TestCase(unittest.TestCase):
	def testProblem1(self):
		p = problem1.Problem()
		
		self.failUnless(p.a in xrange(1, 11))
		self.failUnless(p.b in xrange(1, 11))
		self.failUnlessEqual(p.sum, p.a + p.b)
		self.failUnlessEqual(p.f, "%s + %s = %s" % (p.a, p.b, p.sum))
		self.failUnless(p.is_correct({'action': 'sum',
		                              'arg1': str(p.a),
		                              'arg2': str(p.b),
		                              'comparison': 'equal',
		                              'answer': str(p.sum)}))
	
	def testProblem2(self):
		p = problem2.Problem()
		a = p.fraction.p
		b = p.fraction.q
		
		c = p.denom / b
		
		self.failUnless((a) in xrange(2, 8), "a is %s" % a)
		self.failUnless((b) in xrange(4, 10), "b is %s" % b)
		self.failUnlessEqual(a, p.num / c, "a is %s, p.num is %s, c is %s" % (a, p.num, c))
		self.failUnlessEqual(b, p.denom / c, "b is %s, p.denom is %s, c is %s" % (b, p.denom, c))
		self.failUnless(p.is_correct({'answer': str(a * c)}))
	
	def testProblem3(self):
		p = problem3.Problem()

def suite():
	tests = ['testProblem1', 'testProblem2', 'testProblem3']
	return unittest.TestSuite(map(TestCase, tests))
