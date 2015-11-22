import sys
import os, fnmatch
import re
import xml.etree.ElementTree

masterdict = {}
partial = ''
verbose = False

def find_files(directory, pattern):
	for root, dirs, files in os.walk(directory):
		for basename in files:
			if fnmatch.fnmatch(basename, pattern):
				filename = os.path.join(root, basename)
				yield filename

# Build the R map
for file in find_files(sys.argv[1], '*.xml'):
	if file.endswith('/public.xml'):
		print "Processing: " + file
		e = xml.etree.ElementTree.parse(file).getroot()
		for atype in e.findall('public'):
			idx = int(atype.get('id'), 0)
			if (idx > 100000):
				masterdict[idx]="R."+atype.get('type') +"."+ atype.get('name')

if verbose: print repr(masterdict)

replacements = 0
files = 0

# Go through all the java files and make replacements
for file in find_files(sys.argv[1], '*.java'):
	if file.endswith('/R.java'):
		continue
	f = open(file, 'r')
	content = f.read();
	f.close()
	matches = re.finditer('\d\d\d\d\d\d*', content)
	was_match = False
	for match in matches:
		key = int(match.group())
		val = masterdict.get(key)
		if val:
			was_match = True
			replacements += content.count(str(key))
			content = content.replace(str(key), val)
			if verbose:
				print str(file) + " : " + str(key) + "->" + val
	if was_match:
		files += 1
		f = open(file, 'w')
		f.write(content)
		f.close()

print "Reassociated %s R.* references in %s files" % (replacements, files)