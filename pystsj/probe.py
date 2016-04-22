from math import ceil
from util import distsquare

def baseline(term, ri, theta, esquare, xloc, xlen, posx, lenfilter, overlapx):
  for y, posy in ri.get(term, []):
    ytext = y[3]
    ylen = len(ytext)
    if ylen < lenfilter or distsquare(xloc, y[2]) > esquare:
      continue
    yid = y[1]
    o = overlapx.get(yid, (ytext, 0))
    if o == None:
      continue
    o = o[1]
    alpha = int(ceil(theta*float(xlen+ylen)/(1+theta)))
    ubound = min(xlen-posx, ylen-posy)
    overlapx[yid] = (ytext, o+1) if o + ubound >= alpha else None


def baseline_hamming(term, ri, theta, esquare, xloc, xlen, posx, lenfilter, overlapx):
  for y, posy in ri.get(term, []):
    ytext = y[3]
    ylen = len(ytext)
    if ylen < lenfilter or distsquare(xloc, y[2]) > esquare:
      continue
    yid = y[1]
    o = overlapx.get(yid, (ytext, 0))
    if o == None:
      continue
    o = o[1]
    alpha = int(ceil(theta*float(xlen+ylen)/(1+theta)))
    ubound = min(xlen-posx, ylen-posy)
    if o + ubound < alpha:
      overlapx[yid] = None
      continue
    hmax = xlen + ylen - 2*alpha
    if (posx-o) + (posy-o) + abs((xlen-posx) - (ylen-posy)) > hmax:
      overlapx[yid] = None
      continue
    overlapx[yid] = (ytext, o+1)


def baseline_reverse(term, ri, theta, esquare, xloc, xlen, posx, lenfilter, overlapx):
  postings = ri.get(term)
  if postings == None:
    return
  for y, posy in reversed(postings):
    ytext = y[3]
    ylen = len(ytext)
    if ylen < lenfilter:
      return
    if distsquare(xloc, y[2]) > esquare:
      continue
    yid = y[1]
    o = overlapx.get(yid, (ytext, 0))
    if o == None:
      continue
    o = o[1]
    alpha = int(ceil(theta*float(xlen+ylen)/(1+theta)))
    ubound = min(xlen-posx, ylen-posy)
    overlapx[yid] = (ytext, o+1) if o + ubound >= alpha else None


def baseline_reverse_hamming(term, ri, theta, esquare, xloc, xlen, posx, lenfilter, overlapx):
  postings = ri.get(term)
  if postings == None:
    return
  for y, posy in reversed(postings):
    ytext = y[3]
    ylen = len(ytext)
    if ylen < lenfilter:
      return
    if distsquare(xloc, y[2]) > esquare:
      continue
    yid = y[1]
    o = overlapx.get(yid, (ytext, 0))
    if o == None:
      continue
    o = o[1]
    alpha = int(ceil(theta*float(xlen+ylen)/(1+theta)))
    ubound = min(xlen-posx, ylen-posy)
    if o + ubound < alpha:
      overlapx[yid] = None
      continue
    hmax = xlen + ylen - 2*alpha
    if (posx-o) + (posy-o) + abs((xlen-posx) - (ylen-posy)) > hmax:
      overlapx[yid] = None
      continue
    overlapx[yid] = (ytext, o+1)


def extra_pos(term, ri, theta, esquare, xloc, xlen, posx, lenfilter, overlapx):
  for y, posy in ri.get(term, []):
    ytext = y[3]
    ylen = len(ytext)
    if ylen < lenfilter or distsquare(xloc, y[2]) > esquare:
      continue
    yid = y[1]
    o = overlapx.get(yid, (ytext, 0, posx, posy))
    if o == None:
      continue
    o = o[1]
    alpha = int(ceil(theta*float(xlen+ylen)/(1+theta)))
    ubound = min(xlen-posx, ylen-posy)
    overlapx[yid] = (ytext, o+1, posx, posy) if o + ubound >= alpha else None


def grouping(term, ri, theta, xlen, posx, lenfilter, overlapx):
  for y, posy in ri.get(term, []):
    ylen = y[0][0]
    if ylen < lenfilter:
      continue
    yid = y[1]
    o = overlapx.get(yid, (y, 0))
    if o == None:
      continue
    o = o[1]
    alpha = int(ceil(theta*float(xlen+ylen)/(1+theta)))
    ubound = min(xlen-posx, ylen-posy)
    overlapx[yid] = (y, o+1) if o + ubound >= alpha else None


def grouping_reverse(term, ri, theta, xlen, posx, lenfilter, overlapx):
  postings = ri.get(term)
  if postings == None:
    return
  for y, posy in reversed(postings):
    ylen = y[0][0]
    if ylen < lenfilter:
      return
    yid = y[1]
    o = overlapx.get(yid, (y, 0))
    if o == None:
      continue
    o = o[1]
    alpha = int(ceil(theta*float(xlen+ylen)/(1+theta)))
    ubound = min(xlen-posx, ylen-posy)
    overlapx[yid] = (y, o+1) if o + ubound >= alpha else None


def grouping_hamming(term, ri, theta, xlen, posx, lenfilter, overlapx):
  for y, posy in ri.get(term, []):
    ylen = y[0][0]
    if ylen < lenfilter:
      continue
    yid = y[1]
    o = overlapx.get(yid, (y, 0))
    if o == None:
      continue
    o = o[1]
    alpha = int(ceil(theta*float(xlen+ylen)/(1+theta)))
    ubound = min(xlen-posx, ylen-posy)
    if o + ubound < alpha:
      overlapx[yid] = None
      continue
    hmax = xlen + ylen - 2*alpha
    if (posx-o) + (posy-o) + abs((xlen-posx) - (ylen-posy)) > hmax:
      overlapx[yid] = None
      continue
    overlapx[yid] = (y, o+1)


def grouping_reverse_hamming(term, ri, theta, xlen, posx, lenfilter, overlapx):
  postings = ri.get(term)
  if postings == None:
    return
  for y, posy in reversed(postings):
    ylen = y[0][0]
    if ylen < lenfilter:
      return
    yid = y[1]
    o = overlapx.get(yid, (y, 0))
    if o == None:
      continue
    o = o[1]
    alpha = int(ceil(theta*float(xlen+ylen)/(1+theta)))
    ubound = min(xlen-posx, ylen-posy)
    if o + ubound < alpha:
      overlapx[yid] = None
      continue
    hmax = xlen + ylen - 2*alpha
    if (posx-o) + (posy-o) + abs((xlen-posx) - (ylen-posy)) > hmax:
      overlapx[yid] = None
      continue
    overlapx[yid] = (y, o+1)


