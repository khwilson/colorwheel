"""
The methods contained herein produce generators which return nicely 
differentiated colors; as many as you want in the ranges that you want.

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

from utils import is_valid_lab
from utils import lab2rgb

from itertools import product
from sklearn.cluster import KMeans

def make_palette(num_colors=8,
				filter_func=None,
				estimator=None):
	"""
	Chooses colors from lab color space via k-means. Returns rgb tuples with
	r, g, b in [0, 1).

	You may set up the filter function howsoever you desire. The major suggested
	way is to use the utils class to set up rectilinear boundaries in some
	color space (xyz, lab, hcl, whatever) and then pass this function in.

	Parameters
	----------
	num_colors	int			The total number of colors to return
	filter_func	function	Defines a color space from which to draw
	estimator	KMeans		You may set up your own sklearn.cluster.KMeans and
							pass it in. If none, then a default one is used
							with n_clusters set to num_colors.
							NB: If estimator is set, num_colors is useless.
	"""
	if filter_func is None:
		filter_func = is_valid_lab
	else:
		filter_func = lambda l, a, b: (is_valid_lab(l, a, b) and 
										filter_func(l, a, b))

	potentials = [lab for lab in 
					product((0.05 * i for i in xrange(21)),
							(0.1 * i - 1.0 for i in xrange(21),
							(0.1 * i - 1.0 for i in xrange(21)) 
					if filter_func(*lab)]
	if estimator is None:
		estimator = KMeans(n_clusters=num_colors,
						max_iter=50, n_init=10, init='k-means++')
		estimator.fit(potentials)

	output = []
	for centroid in estimator.cluster_centers_:
		if filter_func(*centroid):
			output.append(centroid)
		else:
			# Get closest valid potential color
			output.append(min([(potential, _l2dist(potential, centroid))
								for potential in potentials],
							key=lambda x: x[1])[0])

	return map(lab2rgb, output)

def make_wheel(num_colors):
	"""
	Same as default, but just loops around the same num_colors colors in a
	circle.
	"""
	colors = list(default(num_colors))
	i = 0
	while True:
		if i >= len(colors):
			i = 0
		yield color[i]
		i += 1
	return

def iwanthue_light_background(l, a, b):
	"""
	This is an example filter function where the space is defined according to
	IWantHue's fancy light background suggestions.
	"""
	hcl = utils.lab2hcl(l, a, b)
	return (0.4 <= hcl[1] <= 1.2) and (1.0 <= hcl[2] <= 1.5)
