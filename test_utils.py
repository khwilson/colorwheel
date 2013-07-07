"""
Tests for utils.py

Copyright (c) 2013 Kevin Wilson

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from utils import *
from utils import _hc2rgb1
from utils import _lab_transform
from utils import _lab_transform_inv

from unittest import main
from unittest import TestCase

class UtilsTest(TestCase):
	def assertAlmostEqual(self, a, b, eps):
		"""
		Asserts if abs(a - b) < eps.
		"""
		if abs(a - b) > eps:
			raise AssertionError("\n\tExpected: %f\n\tActual: %f" % (a, b))

	def test__hc2rgb1(self):
		# Check the preconditions
		with self.assertRaises(ValueError):
			_hc2rgb1('asdf', 0.1)
		with self.assertRaises(ValueError):
			_hc2rgb1(3., 'fdsa')
		with self.assertRaises(ValueError):
			_hc2rgb1(361, 0.1)
		with self.assertRaises(ValueError):
			_hc2rgb1(3, 10)

		c = 0.1
		x = 0.05
		self.assertEquals((0.1, 0.05, 0), _hc2rgb1(30, 0.1))
		self.assertEquals((x, c, 0), _hc2rgb1(90, 0.1))
		self.assertEquals((0, c, x), _hc2rgb1(150, 0.1))
		self.assertEquals((0, x, c), _hc2rgb1(210, 0.1))
		self.assertEquals((x, 0, c), _hc2rgb1(270, 0.1))
		self.assertEquals((c, 0, x), _hc2rgb1(330, 0.1))

	def test__lab_transform(self):
		EPSILON = 1e-7
		self.assertAlmostEqual(1., _lab_transform(1.), EPSILON)
		self.assertAlmostEqual(2., _lab_transform(8.), EPSILON)
		self.assertAlmostEqual(0.14571807152, _lab_transform(0.001), EPSILON)

	def test__lab_transform_inv(self):
		EPSILON = 1e-7
		self.assertAlmostEqual(1., _lab_transform_inv(1.), EPSILON)
		self.assertAlmostEqual(8., _lab_transform_inv(2.), EPSILON)
		self.assertAlmostEqual(0.001, _lab_transform_inv(0.14571807152), EPSILON)

	def test_hsv2rgb(self):
		EPSILON = 1e-3
		expected = (64./256., 48./256., 32./256.)
		actual = hsv2rgb(30, 0.5, 0.25)
		for e, a in zip(expected, actual):
			self.assertAlmostEqual(e, a, EPSILON)

	def test_hsl2rgb(self):
		EPSILON = 1e-3
		expected = (96./256., 64./256., 32./256.)
		actual = hsl2rgb(30, 0.5, 0.25)
		for e, a in zip(expected, actual):
			self.assertAlmostEqual(e, a, EPSILON)

	def test_rgb2hsv(self):
		EPSILON = 1e-3
		rgb = (64./256., 48./256., 32./256.)
		expected = (30., 0.5, 0.25)
		actual = rgb2hsv(*rgb)
		for e, a in zip(expected, actual):
			self.assertAlmostEqual(e, a, EPSILON)

	def test_rgb2hsl(self):
		EPSILON = 1e-3
		rgb = (96./256., 64./256., 32./256.)
		expected = (30., 0.5, 0.25)
		actual = rgb2hsl(*rgb)
		for e, a in zip(expected, actual):
			self.assertAlmostEqual(e, a, EPSILON)

	def test_rgb2hsi(self):
		EPSILON = 1e-3
		rgb = (95.625/256., 63.75/256., 31.875/256.)
		expected = (30., 0.5, 0.25)
		actual = rgb2hsi(*rgb)
		for e, a in zip(expected, actual):
			self.assertAlmostEqual(e, a, EPSILON)

	def test_hcl2lab(self):
		EPSILON = 1e-6
		expected = (0.2425, 0.0506875, 0.08779332530864747)
		actual = hcl2lab(30, 0.5, 0.25)
		for e, a in zip(expected, actual):
			self.assertAlmostEqual(e, a, EPSILON)
		
	def test_lab2xyz(self):
		EPSILON = 1e-6
		expected = (0.04391522311973724, 0.041775695257723774, 0.0229748136370925)
		actual = lab2xyz(0.2425, 0.0506875, 0.08779332530864747)
		for e, a in zip(expected, actual):
			self.assertAlmostEqual(e, a, EPSILON)
	
	def test_hcl2xyz(self):
		EPSILON = 1e-6
		expected = (0.04391522311973724, 0.041775695257723774, 0.0229748136370925)
		actual = hcl2xyz(30, 0.5, 0.25)
		for e, a in zip(expected, actual):
			self.assertAlmostEqual(e, a, EPSILON)

	def test_xyz2rgb(self):
		EPSILON = 1e-6
		expected = (0.286302, 0.211395, 0.143776)
		xyz = (0.04391522311973724, 0.041775695257723774, 0.0229748136370925)
		actual = xyz2rgb(*xyz)
		for e, a in zip(expected, actual):
			self.assertAlmostEqual(e, a, EPSILON)
			

if __name__ == '__main__':
	main()
