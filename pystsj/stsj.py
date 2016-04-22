#!/usr/bin/env python

def parse_args():
  import argparse

  argparser = argparse.ArgumentParser(description='Perform spatio-textual similarity join.')
  argparser.add_argument('--theta', '-t', metavar='<theta>', type=float, required=True, help='textual similarity threshold in (0, 1]')
  argparser.add_argument('--epsilon', '-e', metavar='<epsilon>', type=float, required=True, help='spatial distance threshold (> 0)')
  argparser.add_argument('--scale-epsilon', '-s', action='store_true', help='take epsilon as a ratio to the max spatial extent')
  argparser.add_argument('--normalize-output', '-n', action='store_true', help='normalize output into a specific ordering')
  argparser.add_argument('--grouping', '-g', action='store_true', help='grouping objects by length and prefix')
  argparser.add_argument('--filter-cellgroups', '-f', action='store_true', help='filter cell groups')
  argparser.add_argument('--min-partitions', '-m', metavar='<N>', type=int, help='a hint for the minimal partitions')
  argparser.add_argument('--reverse-probing', '-r', action='store_true', help='probe in reverse order')
  argparser.add_argument('--cprefix', '-p', action='store_true', help='use cprefix')
  argparser.add_argument('--hamming', '-i', action='store_true', help='use hamming filter')
  argparser.add_argument('inputs', metavar='<paths>', help='input file(s): directories, wildcards and comma-separated list are allowed')
  outputgroup = argparser.add_mutually_exclusive_group(required=True)
  outputgroup.add_argument('--output', '-o', metavar='<path>', help='output path')
  outputgroup.add_argument('--count-only', '-c', action='store_true', help='count joined pairs instead of outputting them')
  args = argparser.parse_args()
  if args.epsilon <= 0:
    raise RuntimeError('The spatial distance threshold (epsilon) should be greater than 0')
  if args.theta <= 0 or args.theta > 1:
    raise RuntimeError('The textual similarity threshold (theta) should be greater than 0 and no greater than 1')
  if args.min_partitions <= 0:
    args.min_partitions = None
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
  from operator import add
  from operator import itemgetter
  from pyspark import SparkContext
  from pyspark import SparkConf

  import util
  import sputil
  import sys

  sc = SparkContext(conf=SparkConf().setAppName('Spatio-textual Similarity Join'))

  minx = sc.accumulator(None, sputil.MinAccumParam())
  maxx = sc.accumulator(None, sputil.MaxAccumParam())
  miny = sc.accumulator(None, sputil.MinAccumParam())
  maxy = sc.accumulator(None, sputil.MaxAccumParam())

  def preprocess(l):
    l = l.strip().split(',')
    id = l[0]
    loc = map(lambda n: float(n), l[1:3])
    text = l[3].split()
    minx.add(loc[0])
    maxx.add(loc[0])
    miny.add(loc[1])
    maxy.add(loc[1])
    return (id, loc, text)

  data = sc.textFile(args.inputs, args.min_partitions).map(preprocess).cache()
  # Global Token Ordering
  dic = dict((t, i) for i, t in enumerate(data.flatMap(lambda o: o[2]).map(lambda t: (t, 1)).foldByKey(0, add).map(lambda t: (t[1], t[0])).sortByKey().map(itemgetter(1)).collect()))
  if not dic:
    print 'Empty input data'
    sys.exit(0)
  print 'Total terms: {}'.format(len(dic))

  minx = minx.value
  maxx = maxx.value
  miny = miny.value
  maxy = maxy.value
  print 'Spatial extents: ({}, {}) - ({}, {})'.format(minx, miny, maxx, maxy)
  maxx -= minx
  maxy -= miny
  maxExtent = max(maxx, maxy)
  print 'Max extent: {}'.format(maxExtent)
  epsilon = args.epsilon
  if args.scale_epsilon:
    epsilon *= maxExtent
  del maxExtent
  print 'Epsilon: {}'.format(epsilon)
  ncellx =  int((maxx + epsilon) / epsilon)
  ncelly =  int((maxy + epsilon) / epsilon)
  del maxx, maxy
  print 'Number of cells: {}x{}={}'.format(ncellx, ncelly, ncellx * ncelly)

  data = data.map(util.make_canonicalizer(dic, minx, miny, ncellx, epsilon))
  del dic, minx, miny

  if args.cprefix:
    data = data.cache()
    cprefixes = dict(data.map(util.make_cellcollector(args.theta)).combineByKey(lambda v: set(v), util.updateset, util.updateset).collect())
    data = data.flatMap(util.make_cprefix_cellgroup_expander(ncellx, ncelly, args.theta, cprefixes))
    del cprefixes
  else:
    data = data.flatMap(util.make_cellgroup_expander(ncellx, ncelly))
  del ncellx, ncelly

  data = data.groupByKey()
  if not args.cprefix and args.filter_cellgroups:
    data = data.filter(util.isgroupjoinable)

  if args.grouping:
    data = data.map(util.make_grouping_maker(args.theta))
  else:
    data = data.map(lambda g: sorted(g[1], key=lambda o: len(o[3])))

  verify_counter = sc.accumulator(0)
  data = data.flatMap(util.make_joiner(ppj_join, args.theta, epsilon, verify_counter))
  del epsilon

  if args.count_only:
    noutput = data.count()
  else:
    noutput = sc.accumulator(0)

    def pair_string(p):
      noutput.add(1)
      return p[0]+' '+p[1]

    def sorted_pair_string(p):
      noutput.add(1)
      return p[0]+' '+p[1] if p[0] <= p[1] else p[1]+' '+p[0]

    if args.normalize_output:
      data = data.map(sorted_pair_string).sortBy(lambda x: x)
    else:
      data = data.map(pair_string)
    data.saveAsTextFile(args.output)
    noutput = noutput.value

  print '{} candidates verified'.format(verify_counter.value)
  print '{} pair(s) in total'.format(noutput)


