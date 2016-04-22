from math import ceil
from util import distsquare

def overlap(x, i, xlen, y, j, ylen):
  o = 0
  while i < xlen and j < ylen:
    if x[i] == y[j]:
      o += 1
      i += 1
      j += 1
    elif x[i] < y[j]:
      i += 1
    else:
      j += 1
  return o


def verify1(theta, xid, xtext, xlen, px, overlapx, counter):
  wx = xtext[px-1]
  for yid, o in overlapx.iteritems():
    if o == None:
      continue
    ytext = o[0]
    o = o[1]
    ylen = len(ytext)
    py = theta * float(ylen)
    py = ylen + 1 - max(int(ceil(py)), int(ceil(2*py/(theta+1))))
    alpha = int(ceil(theta*float(xlen+ylen)/(1+theta)))
    wy = ytext[py-1]
    if wx < wy:
      ubound = o + xlen - px
      py = o
    elif wx > wy:
      ubound = o + ylen - py
      px = o
    else:
      ubound = o + min(xlen-px, ylen-py)
    if ubound < alpha:
      continue
    counter.add(1)
    if o + overlap(xtext, px, xlen, ytext, py, ylen) >= alpha:
      yield (xid, yid)


def verify11(theta, xid, xtext, xlen, px, overlapx, counter):
  wx = xtext[px-1]
  for yid, o in overlapx.iteritems():
    if o == None:
      continue
    ytext = o[0]
    posx = o[2]
    posy = o[3]
    o = o[1]
    ylen = len(ytext)
    py = theta * float(ylen)
    py = ylen + 1 - max(int(ceil(py)), int(ceil(2*py/(theta+1))))
    alpha = int(ceil(theta*float(xlen+ylen)/(1+theta)))
    wy = ytext[py-1]
    if wx < wy:
      ubound = o + xlen - px
      py = posy + 1
    elif wx > wy:
      ubound = o + ylen - py
      px = posx + 1
    else:
      ubound = o + min(xlen-px, ylen-py)
    if ubound < alpha:
      continue
    counter.add(1)
    if o + overlap(xtext, px, xlen, ytext, py, ylen) >= alpha:
      yield (xid, yid)


def grouping(theta, esquare, xlen, xprefix, xobjs, overlapx, counter):
  px = len(xprefix)
  wx = xprefix[-1]
  for o in overlapx.itervalues():
    if o == None:
      continue
    y = o[0]
    o = o[1]
    ylen = y[0][0]
    alpha = int(ceil(theta*float(xlen+ylen)/(1+theta)))
    yprefix = y[0][2]
    py = min(len(yprefix), ylen - int(ceil(2*theta*float(ylen)/(theta+1))) + 1)
    wy = yprefix[py-1]
    y = y[2]
    if wx < wy:
      ubound = o + xlen - px
      py = o
    elif wx > wy:
      ubound = o + ylen - py
      px = o
    else:
      ubound = o + min(xlen-px, ylen-py)
    if ubound < alpha:
      continue
    for xo in xobjs:
      for yo in y:
        if distsquare(xo[1], yo[1]) > esquare:
          continue
        counter.add(1)
        if o + overlap(xo[2], px, xlen, yo[2], py, ylen) >= alpha:
          yield (xo[0], yo[0])


def grouping_self(theta, esquare, xlen, xprefixlen, xobjs, counter):
    if len(xobjs) <= 1:
      return
    alpha = int(ceil(theta*float(2*xlen)/(1+theta)))
    for i in xrange(0, len(xobjs) - 1):
      xo = xobjs[i]
      for j in xrange(i+1, len(xobjs)):
        yo = xobjs[j]
        if distsquare(xo[1], yo[1]) > esquare:
          continue
        counter.add(1)
        if xprefixlen + overlap(xo[2], xprefixlen, xlen, yo[2], xprefixlen, xlen) >= alpha:
          yield (xo[0], yo[0])


