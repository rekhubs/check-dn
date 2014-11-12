import os, sys, time, traceback
import urllib2, urllib
import json
import re

# for x in xrange(1,10):
# 	print 'sg3-farm' + str(x) + '.staticflickr.com'

def getHostAddress(domainName):
	print '\n', 'Domain name: ', domainName
	url = 'http://api.statdns.com/' + domainName + '/a'

	try:
		req = urllib2.Request(url)
		content = urllib2.urlopen(req).read()
		# print 'statdns returns: ', content

		contentJson = json.loads(content)
		lastAnswerIdx = len( contentJson['answer'] ) - 1
		ip = contentJson['answer'][lastAnswerIdx]['rdata']
		print 'Parsed ip address:', ip

		# check ip simply
		if re.match(r'(\d{1,3}\.){3}\d{1,3}', ip).group() != ip:
			print 'Warning: Acquired invalid ip:', ip

		return ip		
	except Exception, e:
		print 'Error!', e
		print traceback.format_exc()


########## main ############
strs = []

# read file
try:
	file = open("dn.txt")
	for line in file:
		line = line.strip()
		# print 'find # in line = ', line.find('#')

		if line == '':
			# print 'blank line'
			nline = '\n'
		elif line.find('#') == 0:
			# print "this line is comments: ", line
			nline = line + '\n'
		else:
			ip = getHostAddress(line)
			nline = ip + ' ' + line + '\n'

		strs.append(nline)
except Exception, e:
	print 'Error!', e
	print traceback.format_exc()
	raw_input('Input anything to end...')
finally:
	file.close()

# print strs

# write results
filename = 'hosts-' + time.strftime('%Y%m%d-%H%M', time.localtime()) + '.txt'
file = open(filename, 'a+')
file.writelines(strs)
file.close()

# good bye
raw_input('Input anything to end...')

