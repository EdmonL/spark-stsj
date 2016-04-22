#!/usr/bin/env python

def parse_args():
  import argparse

  argparser = argparse.ArgumentParser(description='Validate spatio-textual similarity join input.')
  argparser.add_argument('inputs', metavar='<path>', nargs='*', help='input file(s)')
  args = argparser.parse_args()
  return args


if __name__ == '__main__':
  args = parse_args()

  import fileinput
  import re

  nonalphanum = re.compile(r'[^ \w]|_', re.UNICODE)

  minx = None
  maxx = None
  miny = None
  maxy = None
  dic = set()
  total = 0
  totalsize = 0
  minsize = None
  maxsize = None
  for l in fileinput.input(args.inputs):
    total += 1
    l = l.strip().split(',')
    try:
      assert len(l) == 4 and len(l[0]) == len(l[0].strip()) and len(l[0].strip()) > 0
      loc = map(lambda n: float(n), l[1:3])
      assert l[3] == l[3].lower()
      text = l[3].split()
      assert len(text) > 0, 'Empty text'
      assert len(' '.join(set(text))) == len(l[3]) and re.search(nonalphanum, l[3]) == None
      minsize = len(text) if minsize == None else min(minsize, len(text))
      maxsize = len(text) if maxsize == None else max(maxsize, len(text))
      totalsize += len(text)
      minx = loc[0] if minx == None else min(minx, loc[0])
      maxx = loc[0] if maxx == None else max(maxx, loc[0])
      miny = loc[1] if miny == None else min(miny, loc[1])
      maxy = loc[1] if maxy == None else max(maxy, loc[1])
      for t in text:
        dic.add(t)
    except:
      print 'Line {} is being processed'.format(total)
      raise
  fileinput.close()

  print 'Total objects: {}'.format(total)
  print 'Total terms: {}'.format(len(dic))
  print 'Spatial extents: ({}, {}) - ({}, {})'.format(minx, miny, maxx, maxy)
  print 'Min size: {}'.format(minsize)
  print 'Max size: {}'.format(maxsize)
  print 'Average size of objects: {}'.format(float(totalsize) / total)


