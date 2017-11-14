import urllib2
import re


dict = {'Canceling Units': 'http://www.purplemath.com/modules/units.htm', 'Distance Formula': 'http://www.purplemath.com/modules/distform.htm', 'Engineering Notation': 'http://www.purplemath.com/modules/exponent4.htm',
		'Evaluation': 'http://www.purplemath.com/modules/evaluate.htm','Intercepts': 'http://www.purplemath.com/modules/intrcept.htm',
		'Midpoint Formula': 'http://www.purplemath.com/modules/midpoint.htm','Order of Operations': 'http://www.purplemath.com/modules/orderops.htm',
		'Polynomials':'http://www.purplemath.com/modules/polydefs.htm','Simplifying with ':'http://www.purplemath.com/modules/simpexpo.htm',
		'Parentheses':'http://www.purplemath.com/modules/simparen.htm','Slope of a straight line':'http://www.purplemath.com/modules/slope.htm',
		'Slope and Graphing': 'http://www.purplemath.com/modules/slopgrph.htm','Slope and y-intercept':'http://www.purplemath.com/modules/slopyint.htm',
		'Solving Absolute Value':'http://www.purplemath.com/modules/solveabs.htm','Equations':'http://www.purplemath.com/modules/solveabs.htm',
		'Solving Linear Equations':'http://www.purplemath.com/modules/solvelin.htm',
		'Straight-line equations':'http://www.purplemath.com/modules/strtlneq.htm','Variables':'http://www.purplemath.com/modules/variable.htm',
		'Solving Radical Equations':'http://www.purplemath.com/modules/solverad.htm'
		}

dataAndTitle = []		
for index in dict:    
	url = 'http://www.purplemath.com/modules/units.htm'#dict[index]
	req = urllib2.Request(url)
	f = urllib2.urlopen(req)
	html = f.read()
	titles = re.findall(r'<title>(.*?)</title>',html)
	paragraph = re.findall(r'<p class="text">(.*?)</p>',html)
	case = { titles[0] : paragraph}
	dataAndTitle.append(case)
	print dataAndTitle
	
	
