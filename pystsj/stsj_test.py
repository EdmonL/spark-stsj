#!/usr/bin/env python

def parse_args():
  import argparse

  argparser = argparse.ArgumentParser(description='Test spatio-textual similarity join.')
  argparser.add_argument('--theta', '-t', metavar='<theta>', type=float, required=True, help='textual similarity threshold in (0, 1]')
  argparser.add_argument('--epsilon', '-e', metavar='<epsilon>', type=float, required=True, help='spatial distance threshold (> 0)')
  argparser.add_argument('--scale-epsilon', '-s', action='store_true', help='take epsilon as a ratio to the max spatial extent')
  argparser.add_argument('--normalize-output', '-n', action='store_true', help='normalize output into a specific ordering')
  argparser.add_argument('--grouping', '-g', action='store_true', help='grouping objects by length and prefix')
  argparser.add_argument('--filter-cellgroups', '-f', action='store_true', help='filter cell groups')
  argparser.add_argument('--reverse-probing', '-r', action='store_true', help='probe in reverse order')
  argparser.add_argument('--cprefix', '-p', action='store_true', help='use cprefix')
  argparser.add_argument('--hamming', '-i', action='store_true', help='use hamming filter')
  argparser.add_argument('inputs', metavar='<path>', nargs='*', help='input file(s)')
  args = argparser.parse_args()
  if args.epsilon <= 0:
    raise RuntimeError('The spatial distance threshold (epsilon) should be greater than 0')
  if args.theta <= 0 or args.theta > 1:
    raise RuntimeError('The textual similarity threshold (theta) should be greater than 0 and no greater than 1')
  return args


if __name__ == '__main__':
  args = parse_args()

  import ppj
  import probe
  import verify

  if args.reverse_probing:
    if args.hamming:
      ppj_join = ppj.join_grouping_reverseprobing_hamming if args.grouping else ppj.join_reverseprobing_hamming
    else:
      ppj_join = ppj.join_grouping_reverseprobing if args.grouping else ppj.join_reverseprobing
  elif args.hamming:
    ppj_join = ppj.join_grouping_hamming if args.grouping else ppj.join_hamming
  else:
    ppj_join = ppj.join_grouping if args.grouping else ppj.join

  from itertools import groupby
  from operator import itemgetter
  from sys import stderr

  import util
  import fileinput
  import sys

  minx = None
  maxx = None
  miny = None
  maxy = None
  dic = {}

  def preprocess(l):
    global minx, maxx, miny, maxy
    l = l.strip().split(',')
    id = l[0]
    loc = map(lambda n: float(n), l[1:3])
    text = l[3].split()
    minx = loc[0] if minx == None else min(minx, loc[0])
    maxx = loc[0] if maxx == None else max(maxx, loc[0])
    miny = loc[1] if miny == None else min(miny, loc[1])
    maxy = loc[1] if maxy == None else max(maxy, loc[1])
    for t in text:
      dic[t] = dic.get(t, 0) + 1
    return (id, loc, text)

  data = map(preprocess, fileinput.input(args.inputs))
  stderr.write('Total objects: {}\n'.format(len(data)))

  dic = dict((p[0], i) for i, p in enumerate(sorted(dic.iteritems(), key=itemgetter(1))))
  if not dic:
    stderr.write('Empty input data')
    sys.exit(0)
  stderr.write('Total terms: {}\n'.format(len(dic)))

  stderr.write('Spatial extents: ({}, {}) - ({}, {})\n'.format(minx, miny, maxx, maxy))
  maxx -= minx
  maxy -= miny
  maxExtent = max(maxx, maxy)
  stderr.write('Max extent: {}\n'.format(maxExtent))
  epsilon = args.epsilon
  if args.scale_epsilon:
    epsilon *= maxExtent
  del maxExtent
  stderr.write('Epsilon: {}\n'.format(epsilon))
  ncellx =  int((maxx + epsilon) / epsilon)
  ncelly =  int((maxy + epsilon) / epsilon)
  del maxx, maxy
  stderr.write('Number of cells: {}x{}={}\n'.format(ncellx, ncelly, ncellx * ncelly))

  data = map(util.make_canonicalizer(dic, minx, miny, ncellx, epsilon), data)
  del dic, minx, miny

  if args.cprefix:
    cprefixes = map(util.make_cellcollector(args.theta), data)
    cprefixes.sort(key=itemgetter(0))
    cprefixes = dict((cid, reduce(util.updateset, map(itemgetter(1), cells), set())) for cid, cells in groupby(cprefixes, key=itemgetter(0)))
    expand_with_cellgroup = util.make_cprefix_cellgroup_expander(ncellx, ncelly, args.theta, cprefixes)
    del cprefixes
  else:
    expand_with_cellgroup = util.make_cellgroup_expander(ncellx, ncelly)
  data = list(g for o in data for g in expand_with_cellgroup(o))
  del expand_with_cellgroup, ncellx, ncelly

  data.sort(key=itemgetter(0))
  data = map(lambda gi: (gi[0], map(lambda g: g[1], gi[1])), groupby(data, key=itemgetter(0)))
  if not args.cprefix and args.filter_cellgroups:
    data = list(g for g in data if util.isgroupjoinable(g))

  if args.grouping:
    data = map(util.make_grouping_maker(args.theta), data)
  else:
    data = map(lambda g: sorted(g[1], key=lambda o: len(o[3])), data)

  verify_counter = util.SimpleCounter()
  join = util.make_joiner(ppj_join, args.theta, epsilon, verify_counter)
  del epsilon

  noutput = 0
  if args.normalize_output:
    for s in sorted((p[0]+' '+p[1] if p[0] <= p[1] else p[1]+' '+p[0]) for g in data for p in join(g)):
      print s
      noutput += 1
  else:
    for g in data:
      for p in join(g):
        print p[0], p[1]
        noutput += 1

  stderr.write('{} candidates were verified\n'.format(verify_counter.value))
  stderr.write('{} pair(s) in total\n'.format(noutput))


