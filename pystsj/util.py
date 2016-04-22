from itertools import groupby
from math import floor
from math import ceil
from operator import itemgetter

class SimpleCounter:

  def __init__(self):
    self.value = 0

  def add(self, n):
    self.value += n


def distsquare(p1, p2):
  return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2


def isgroupjoinable(g):
  return any(o[0] > 0 for o in g[1])

 
def updateset(s, c):
  s.update(c)
  return s


def make_canonicalizer(dic, minx, miny, ncellx, epsilon):
  def canonicalize(o):
    loc = tuple(o[1])
    text = map(lambda t: dic[t], o[2])
    text.sort()
    cid = int(floor((loc[1] - miny) / epsilon)) * ncellx + int(floor((loc[0] - minx) / epsilon))
    return (cid, o[0], loc, tuple(text))

  return canonicalize


def getprefix(text, theta):
  textlen = len(text)
  prefixlen = textlen - int(ceil(theta*float(textlen))) + 1
  return text[0:prefixlen]


def make_cellcollector(theta):
  def collect_cell(o):
    return (o[0], getprefix(o[3], theta))

  return collect_cell


def make_grouping_maker(theta):
  def make_grouping(g):
    r = []
    for o in g[1]:
      r.append(((len(o[3]), o[0], getprefix(o[3], theta)), (o[1], o[2], o[3])))
    r.sort(key=itemgetter(0))
    return tuple((gi[0], i, map(lambda po: po[1], gi[1])) for i, gi in enumerate(groupby(r, key=itemgetter(0))))

  return make_grouping


def getgids(cid, ncellx, ncelly):
  yield cid
  nx = cid % ncellx
  ny = cid / ncellx
  hasprev = nx > 0
  hasnext = nx < ncellx - 1
  if hasnext:
    yield cid + 1
  if ny < ncelly - 1:
    cid += ncellx
    yield cid
    if hasprev:
      yield cid - 1
    if hasnext:
      yield cid + 1


def make_cprefix_cellgroup_expander(ncellx, ncelly, theta, cprefixes):
  def expand_with_cellgroup(o):
    cid = o[0]
    o = (0, o[1], o[2], o[3])
    oprefix = getprefix(o[3], theta)
    for gid in getgids(cid, ncellx, ncelly):
      if cid == gid:
        yield (gid, (1, o[1], o[2], o[3]))
      else:
        cprefix = cprefixes.get(gid)
        if cprefix != None and not cprefix.isdisjoint(oprefix):
          yield (gid, o)

  return expand_with_cellgroup


def make_cellgroup_expander(ncellx, ncelly):
  def expand_with_cellgroup(o):
    cid = o[0]
    o = (0, o[1], o[2], o[3])
    for gid in getgids(cid, ncellx, ncelly):
      if cid == gid:
        yield (gid, (1, o[1], o[2], o[3]))
      else:
        yield (gid, o)

  return expand_with_cellgroup


def make_joiner(ppj_join, theta, epsilson, verify_counter):
  esquare = epsilson ** 2

  def join(g):
    return ppj_join(g, theta, esquare, verify_counter)

  return join
    

