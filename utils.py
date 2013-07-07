"""
This file contains a lot of utility functions, especially converting between
different color types. The vast majority of these functions were just stolen
from Wikipedia. I'm absolutely positive somebody has written exactly this file
before, but it's faster for me to copy-pasta from the Fount of All Knowledge
than to go searching.

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

from math import cos
from math import pi
from math import sin

def _hc2rgb1(h, c):
	"""
	Takes the hue and chroma and returns the helper rgb1.

	Parameters
	----------
	h	float	The hue in degrees
	c	float 	The chroma in [0, 1]
	"""
	try:
		h = float(h)
		c = float(c)
	except ValueError:
		raise ValueError("h (%s) and c (%s) must be (convertible to) floats" %
							(str(h), str(c)))

	if not (0 <= h < 360):
		raise ValueError("h (%f) must be in [0, 360)" % h)
	if not (0 <= c <= 1):
		raise ValueError("c (%f) must be in [0, 1]" % c)

	hprime = h / 60
	x = c * (1 - abs((hprime % 2) - 1))

	if 0 <= hprime < 1:
		return (c, x, 0)
	elif 1 <= hprime < 2:
		return (x, c, 0)
	elif 2 <= hprime < 3:
		return (0, c, x)
	elif 3 <= hprime < 4:
		return (0, x, c)
	elif 4 <= hprime < 5:
		return (x, 0, c)
	else:
		return (c, 0, x)

def _lab_transform(t):
	"""
	Returns the cube root tranformation function from xyz color space to
	lab color space.
	"""
	if t > 216. / 24389.:
		return t ** (1. / 3.)
	return 841. / 108. * t + 4. / 29.

def _lab_transform_inv(t):
	"""
	Returns the inverse of the cube root tranformation function from xyz color
	space to lab color space.
	"""
	if t > 6. / 29.:
		return t * t * t
	return 108. / 841. * (t - 4. / 29.)

def hsv2rgb(h, s, v):
	"""
	Convert from hsv to rgb.

	Parameters
	----------
	h	float	The hue in degrees
	s	float	The saturation in percent [0, 1]
	v	float	The value [0, 1]

	Returns
	-------
	rgb triple with r, g, b between 0 and 1
	"""
	try:
		h = float(h)
		s = float(s)
		v = float(v)
	except ValueError:
		raise ValueError(("h (%s), s (%s), and v (%v) must be (convertible to) "
							+ "floats") % (str(h), str(s), str(v)))
	if not (0 <= h < 360):
		raise ValueError("h (%f) must be in [0, 360)" % h)
	if not (0 <= s <= 1):
		raise ValueError("s (%f) must be in [0, 1]" % s)
	if not (0 <= v <= 1):
		raise ValueError("v (%f) must be in [0, 1]" % v)

	c = v * s
	rgb1 = _hc2rgb1(h, c)
	m = v - c
	return rgb1[0] + m, rgb1[1] + m, rgb1[2] + m

def _rgb2hsvli(r, g, b, which):
	"""
	Convert from rgb to one of hs[vli]

	This is a private function written basically just because the h and s
	components are the same, but the last parameter is not.

	Parameters
	----------
	r	float	The red in [0, 1]
	g	float	The green in [0, 1]
	b	flaot	The blue in [0, 1]
	which 	char	One of 'v', 'l', and 'i'

	Returns
	-------
	hs[vli] triple depending on which.
	"""
	try:
		r = float(r)
		g = float(g)
		b = float(b)
	except ValueError:
		raise ValueError(("r (%s), g (%s), and b (%s) must all be (convertible "
							"to) floats") % (str(r), str(g), str(b)))

	if not (0 <= r <= 1):
		raise ValueError("r (%f) must be in [0, 1])" % r)
	if not (0 <= g <= 1):
		raise ValueError("g (%f) must be in [0, 1])" % g)
	if not (0 <= b <= 1):
		raise ValueError("b (%f) must be in [0, 1])" % b)

	M = max(r, g, b)
	m = min(r, g, b)
	c = M - m

	if c == 0:
		hprime = 0
	elif M == r:
		hprime = (g - b) / c
	elif M == g:
		hprime = (b - r) / c + 2
	elif M == b:
		hprime = (r - g) / c + 4
	h = 60. * hprime

	if which == 'v':
		v = M
		s = c / v
		return h, s, v
	elif which == 'l':
		l = (r + g + b) / 3.
		s = c / (1 - abs(2 * l - 1))
		return h, s, l
	elif which == 'i':
		i = (M + m) / 2.
		s = 1 - m / i
		return h, s, i
	else:
		raise ValueError("which (%s) must be one of 'v', 's', and 'i'" % which)

def rgb2hsv(r, g, b):
	"""
	Convert from rgb to hsv.

	Parameters
	----------
	r	float	The red in [0, 1]
	g	float	The green in [0, 1]
	b	float	The blue in [0, 1]

	Returns
	-------
	An hsv triple with h in degrees [0, 360) and s and v in [0, 1]
	"""
	try:
		r = float(r)
		g = float(g)
		b = float(b)
	except ValueError:
		raise ValueError(("r (%s), g (%s), and b (%s) must all be (convertible "
							"to) floats") % (str(r), str(g), str(b)))

	if not (0 <= r <= 1):
		raise ValueError("r (%f) must be in [0, 1])" % r)
	if not (0 <= g <= 1):
		raise ValueError("g (%f) must be in [0, 1])" % g)
	if not (0 <= b <= 1):
		raise ValueError("b (%f) must be in [0, 1])" % b)

	return _rgb2hsvli(r, g, b, 'v')

def rgb2hsl(r, g, b):
	"""
	Convert from rgb to hsl.

	Parameters
	----------
	r	float	The red in [0, 1]
	g	float	The green in [0, 1]
	b	float	The blue in [0, 1]

	Returns
	-------
	An hsl triple with h in degrees [0, 360) and s and l in [0, 1]
	"""
	try:
		r = float(r)
		g = float(g)
		b = float(b)
	except ValueError:
		raise ValueError(("r (%s), g (%s), and b (%s) must all be (convertible "
							"to) floats") % (str(r), str(g), str(b)))

	if not (0 <= r <= 1):
		raise ValueError("r (%f) must be in [0, 1])" % r)
	if not (0 <= g <= 1):
		raise ValueError("g (%f) must be in [0, 1])" % g)
	if not (0 <= b <= 1):
		raise ValueError("b (%f) must be in [0, 1])" % b)

	return _rgb2hsvli(r, g, b, 'l')

def rgb2hsi(r, g, b):
	"""
	Convert from rgb to hsi.

	Parameters
	----------
	r	float	The red in [0, 1]
	g	float	The green in [0, 1]
	b	float	The blue in [0, 1]

	Returns
	-------
	An hsi triple with h in degrees [0, 360) and s and i in [0, 1]
	"""
	try:
		r = float(r)
		g = float(g)
		b = float(b)
	except ValueError:
		raise ValueError(("r (%s), g (%s), and b (%s) must all be (convertible "
							"to) floats") % (str(r), str(g), str(b)))

	if not (0 <= r <= 1):
		raise ValueError("r (%f) must be in [0, 1])" % r)
	if not (0 <= g <= 1):
		raise ValueError("g (%f) must be in [0, 1])" % g)
	if not (0 <= b <= 1):
		raise ValueError("b (%f) must be in [0, 1])" % b)

	return _rgb2hsvli(r, g, b, 'i')

def hsl2rgb(h, s, l):
	"""
	Convert from hsl to rgb.

	Parameters
	----------
	h	float	The hue in degrees
	s	float	The saturation in percent [0, 1]
	v	float	The value [0, 1]

	Returns
	-------
	rgb triple with r, g, b between 0 and 1
	"""
	c = (1 - abs(2 * l - 1)) * s
	rgb1 = _hc2rgb1(h, c)
	m = l - c / 2
	return rgb1[0] + m, rgb1[1] + m, rgb1[2] + m

def hcl2lab(h, c, l):
	"""
	Convert from hcl to lab. This was the original scale in which IWantHue was
	created.

	Parameters
	----------
	h	float	The hue in degrees
	c	float	The chroma
	l	float	The luma

	Returns
	-------
	Lab triple
	"""
	try:
		h = float(h)
		c = float(c)
		l = float(l)
	except ValueError:
		raise ValueError(("h (%s), c (%s), and l (%s) must be (convertible to) "
							+ "floats") % (str(h), str(c), str(l)))

	if not (0 <= h < 360):
		raise ValueError("h (%f) must be in [0, 360)" % h)

	h /= 360
	L = 0.61 * l + 0.09
	theta = pi / 3 - 2 * pi * h
	r = (0.311 * l + 0.125) * c
	a = sin(theta) * r
	b = cos(theta) * r
	return L, a, b

def lab2hcl(L, a, b):
	"""
	Convert from lab to hcl. This was the original scale in which IWantHue was
	created.

	Parameters
	----------
	L	float	The lightness
	a	float	The sine color-opponent
	b	float	The cosine color-opponent

	Returns
	-------
	hcl triple
	"""
	try:
		h = float(h)
		c = float(c)
		l = float(l)
	except ValueError:
		raise ValueError(("h (%s), c (%s), and l (%s) must be (convertible to) "
							+ "floats") % (str(h), str(c), str(l)))

	l = (L - 0.09) / 0.61
	r = sqrt(a * a + b * b)
	c = r / (l * 0.311 + 0.125)
	theta = atan2(a, b)
	h = 1. / 6. - theta / 2. / pi
	h %= 1
	h *= 360
	return h, c, l

def lab2xyz(l, a, b):
	"""
	Convert from l*a*b* to xyz color space.

	Parameters
	----------
	l	float	The lightness
	a	float	The sine color-opponent
	b	float	The cosine color-opponent

	Returns
	-------
	The xyz triple
	"""
	sl = (l + 0.16) / 1.16;
	# Standard white
	xn, yn, zn = (0.96421, 1.00000, 0.82519)
	y = yn * _lab_transform_inv(sl);
	x = xn * _lab_transform_inv(sl + (a / 5.0));
	z = zn * _lab_transform_inv(sl - (b / 2.0));
	return x, y, z;

def xyz2rgb(x, y, z):
	"""
	Convert from xyz color space to rgb.
	Ganked from http://en.wikipedia.org/wiki/Srgb

	Parameters
	----------
	x, y, z		all floats in the xyz color space

	Returns
	-------
	rgb triple with r, g, b between 0 and 1

	NB: If x, y, z is out of gamut, then we clip rgb to the [0, 1]^3 cube.
	"""
	try:
		x = float(x)
		y = float(y)
		z = float(z)
	except ValueError:
		raise ValueError(("x (%s), y (%s), and z (%s) must all be (convertible "
							+ "to) floats") % (str(x), str(y), str(z)))

	# The linear transformation to linear rgb
	rlin = 3.2406 * x - 1.5372 * y - 0.4986 * z
	glin = -0.9689 * x + 1.8758 * y + 0.0415 * z
	blin = 0.0557 * x - 0.2040 * y + 1.0570 * z

	# What if things are out of gamut?
	rlin = min(1., max(0., rlin))
	glin = min(1., max(0., glin))
	blin = min(1., max(0., blin))

	# Now for the correction
	def correction(c):
		if c <= 0.0031308:
			return 12.92 * c
		return 1.055 * c ** (1. / 2.4) - 0.055

	return correction(rlin), correction(glin), correction(blin)

def hcl2xyz(h, c, l):
	"""
	Convert from hcl to xyz. This was the original scale in which IWantHue was
	created.

	Parameters
	----------
	h	float	The hue in degrees
	c	float	The chroma in [0, 1]
	l	float	The luma. If in [0, 1], shouldn't go out of gamut.

	Returns
	-------
	xyz triple which is as in gamut as colorologists know how to make it
	"""
	try:
		h = float(h)
		c = float(c)
		l = float(l)
	except ValueError:
		raise ValueError(("h (%s), c (%s), and l (%s) must be (convertible to) "
							+ "floats") % (str(h), str(c), str(l)))
	return lab2xyz(*hcl2lab(h, c, l))

def hcl2rgb(h, c, l):
	"""
	Convert from hcl to rgb. This was the original scale in which IWantHue was
	created.

	Parameters
	----------
	h	float	The hue in degrees
	c	float	The chroma in [0, 1]
	l	float	The luma. If in [0, 1], shouldn't go out of gamut.

	Returns
	-------
	rgb triple with r, g, b in [0, 1]. Note that if in the conversion
	we hit out of gamut colors, we clip to the [0, 1]^3 cube in the end.
	"""
	try:
		h = float(h)
		c = float(c)
		l = float(l)
	except ValueError:
		raise ValueError(("h (%s), c (%s), and l (%s) must be (convertible to) "
							+ "floats") % (str(h), str(c), str(l)))

	return xyz2rgb(*lab2xyz(*hcl2lab(h, c, l)))

def is_valid_lab(l, a, b):
	"""
	Just make sure we're getting something reasonable here.
	"""
	rgb = lab2rgb(l, a, b)
	return all([x >= 0 for x in rgb]) and all([x < 1 for x in rgb])

