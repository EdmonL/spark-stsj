#!/usr/bin/env python

def parse_args():
  import argparse

  argparser = argparse.ArgumentParser(description='Cook SimpleGeos places datasets.')
  argparser.add_argument('inputs', metavar='<path>', nargs='*', help='input file(s)')
  argparser.add_argument('--print-header', '-p', action='store_true', help='print header')
  args = argparser.parse_args()
  return args


def make_tokenizer():
  import re

  nonalphanum = re.compile(r'[\W_]+', re.UNICODE)
  def tokenize(s):
    for t in re.sub(nonalphanum, ' ', s.lower()).split():
      yield t
  return tokenize


tokenize = make_tokenizer()


def gettext(o):
  t = list(o['tags']) if 'tags' in o else []
  if 'classifiers' in o: 
    for c in o['classifiers']:
      if 'category' in c:
        t.append(c['category'])
      if 'subcategory' in c:
        t.append(c['subcategory'])
  return sorted(set(tokenize(' '.join(t))))


if __name__ == '__main__':
  args = parse_args()

  from sys import stderr

  import json
  import fileinput

  minx = None
  maxx = None
  miny = None
  maxy = None
  nempty = 0
  total = 0
  totalsize = 0
  minsize = None
  maxsize = None
  if args.print_header:
    print 'ID,Longitude,Latitude,Text'
  for i, l in enumerate(fileinput.input(args.inputs)):
    try:
      o = json.loads(l)
      id = str(o['id']).strip()
      assert len(id) > 0
      assert o['geometry']['type'].lower() == 'point'
      loc = map(lambda n: float(n), o['geometry']['coordinates'])
      assert len(loc) == 2
      o = o['properties']
      text = gettext(o)
      if len(text) <= 0:
        nempty += 1
        continue
      total += 1
      minsize = len(text) if minsize == None else min(minsize, len(text))
      maxsize = len(text) if maxsize == None else max(maxsize, len(text))
      totalsize += len(text)
      minx = loc[0] if minx == None else min(minx, loc[0])
      maxx = loc[0] if maxx == None else max(maxx, loc[0])
      miny = loc[1] if miny == None else min(miny, loc[1])
      maxy = loc[1] if maxy == None else max(maxy, loc[1])
      print '{},{},{},{}'.format(id, loc[0], loc[1], ' '.join(text))
    except:
      stderr.write('Line {} is being processed\n'.format(i+1))
      raise
  fileinput.close()

  stderr.write('Empty/non-empty objects: {}/{}\n'.format(nempty, total))
  stderr.write('Spatial extents: ({}, {}) - ({}, {})\n'.format(minx, miny, maxx, maxy))
  stderr.write('Min size: {}\n'.format(minsize))
  stderr.write('Max size: {}\n'.format(maxsize))
  stderr.write('Average size of non-empty objects: {}\n'.format(float(totalsize) / total))


