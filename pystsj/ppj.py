from collections import deque
from math import ceil

import verify
import probe

def join(g, theta, esquare, verify_counter): # group, theta and epsilon square
  if len(g) <= 1:
    return
  ric = {} # inverted index for the current cell
  rio = {} # inverted index for other cells
  for x in g:
    xtext = x[3]
    xlen = len(xtext)
    xloc = x[2]
    lenfilter = theta * float(xlen)
    iprefix_len = xlen - int(ceil(2*lenfilter/(theta+1))) + 1
    lenfilter = int(ceil(lenfilter))
    xprefixlen = xlen - lenfilter + 1
    overlapx = {}
    for posx in xrange(0, xprefixlen):
      term = xtext[posx]
      probe.baseline(term, ric, theta, esquare, xloc, xlen, posx, lenfilter, overlapx)
      if x[0] <= 0:
        if posx < iprefix_len:
          postings = rio.get(term)
          if postings == None:
            postings = [(x, posx)]
          else:
            postings.append((x, posx))
          rio[term] = postings
        continue
      if posx < iprefix_len:
        postings = ric.get(term)
        if postings == None:
          postings = [(x, posx)]
        else:
          postings.append((x, posx))
        ric[term] = postings
      probe.baseline(term, rio, theta, esquare, xloc, xlen, posx, lenfilter, overlapx)
    for p in verify.verify1(theta, x[1], xtext, xlen, xprefixlen, overlapx, verify_counter):
      yield p


def join_grouping(g, theta, esquare, verify_counter): # group, theta and epsilon square
  ric = {} # inverted index for the current cell
  rio = {} # inverted index for other cells
  for x in g:
    xlen = x[0][0]
    xprefix = x[0][2]
    lenfilter = theta * float(xlen)
    iprefix_len = xlen - int(ceil(2*lenfilter/(theta+1))) + 1
    lenfilter = int(ceil(lenfilter))
    overlapx = {}
    for posx in xrange(0, len(xprefix)):
      term = xprefix[posx]
      probe.grouping(term, ric, theta, xlen, posx, lenfilter, overlapx)
      if x[0][1] <= 0:
        if posx < iprefix_len:
          postings = rio.get(term)
          if postings == None:
            postings = [(x, posx)]
          else:
            postings.append((x, posx))
          rio[term] = postings
        continue
      if posx < iprefix_len:
        postings = ric.get(term)
        if postings == None:
          postings = [(x, posx)]
        else:
          postings.append((x, posx))
        ric[term] = postings
      probe.grouping(term, rio, theta, xlen, posx, lenfilter, overlapx)
    for p in verify.grouping(theta, esquare, xlen, xprefix, x[2], overlapx, verify_counter):
      yield p
    del overlapx
    if x[0][1] > 0:
      for p in verify.grouping_self(theta, esquare, xlen, len(xprefix), x[2], verify_counter):
        yield p


def join_reverseprobing(g, theta, esquare, verify_counter): # group, theta and epsilon square
  if len(g) <= 1:
    return
  ric = {} # inverted index for the current cell
  rio = {} # inverted index for other cells
  for x in g:
    xtext = x[3]
    xlen = len(xtext)
    xloc = x[2]
    lenfilter = theta * float(xlen)
    iprefix_len = xlen - int(ceil(2*lenfilter/(theta+1))) + 1
    lenfilter = int(ceil(lenfilter))
    xprefixlen = xlen - lenfilter + 1
    overlapx = {}
    for posx in xrange(0, xprefixlen):
      term = xtext[posx]
      probe.baseline_reverse(term, ric, theta, esquare, xloc, xlen, posx, lenfilter, overlapx)
      if x[0] <= 0:
        if posx < iprefix_len:
          postings = rio.get(term)
          if postings == None:
            postings = [(x, posx)]
          else:
            postings.append((x, posx))
          rio[term] = postings
        continue
      if posx < iprefix_len:
        postings = ric.get(term)
        if postings == None:
          postings = [(x, posx)]
        else:
          postings.append((x, posx))
        ric[term] = postings
      probe.baseline_reverse(term, rio, theta, esquare, xloc, xlen, posx, lenfilter, overlapx)
    for p in verify.verify1(theta, x[1], xtext, xlen, xprefixlen, overlapx, verify_counter):
      yield p


def join_grouping_reverseprobing(g, theta, esquare, verify_counter): # group, theta and epsilon square
  ric = {} # inverted index for the current cell
  rio = {} # inverted index for other cells
  for x in g:
    xlen = x[0][0]
    xprefix = x[0][2]
    lenfilter = theta * float(xlen)
    iprefix_len = xlen - int(ceil(2*lenfilter/(theta+1))) + 1
    lenfilter = int(ceil(lenfilter))
    overlapx = {}
    for posx in xrange(0, len(xprefix)):
      term = xprefix[posx]
      probe.grouping_reverse(term, ric, theta, xlen, posx, lenfilter, overlapx)
      if x[0][1] <= 0:
        if posx < iprefix_len:
          postings = rio.get(term)
          if postings == None:
            postings = [(x, posx)]
          else:
            postings.append((x, posx))
          rio[term] = postings
        continue
      if posx < iprefix_len:
        postings = ric.get(term)
        if postings == None:
          postings = [(x, posx)]
        else:
          postings.append((x, posx))
        ric[term] = postings
      probe.grouping_reverse(term, rio, theta, xlen, posx, lenfilter, overlapx)
    for p in verify.grouping(theta, esquare, xlen, xprefix, x[2], overlapx, verify_counter):
      yield p
    del overlapx
    if x[0][1] > 0:
      for p in verify.grouping_self(theta, esquare, xlen, len(xprefix), x[2], verify_counter):
        yield p


def join_hamming(g, theta, esquare, verify_counter): # group, theta and epsilon square
  if len(g) <= 1:
    return
  ric = {} # inverted index for the current cell
  rio = {} # inverted index for other cells
  for x in g:
    xtext = x[3]
    xlen = len(xtext)
    xloc = x[2]
    lenfilter = theta * float(xlen)
    iprefix_len = xlen - int(ceil(2*lenfilter/(theta+1))) + 1
    lenfilter = int(ceil(lenfilter))
    xprefixlen = xlen - lenfilter + 1
    overlapx = {}
    for posx in xrange(0, xprefixlen):
      term = xtext[posx]
      probe.baseline_hamming(term, ric, theta, esquare, xloc, xlen, posx, lenfilter, overlapx)
      if x[0] <= 0:
        if posx < iprefix_len:
          postings = rio.get(term)
          if postings == None:
            postings = [(x, posx)]
          else:
            postings.append((x, posx))
          rio[term] = postings
        continue
      if posx < iprefix_len:
        postings = ric.get(term)
        if postings == None:
          postings = [(x, posx)]
        else:
          postings.append((x, posx))
        ric[term] = postings
      probe.baseline_hamming(term, rio, theta, esquare, xloc, xlen, posx, lenfilter, overlapx)
    for p in verify.verify1(theta, x[1], xtext, xlen, xprefixlen, overlapx, verify_counter):
      yield p


def join_grouping_hamming(g, theta, esquare, verify_counter): # group, theta and epsilon square
  ric = {} # inverted index for the current cell
  rio = {} # inverted index for other cells
  for x in g:
    xlen = x[0][0]
    xprefix = x[0][2]
    lenfilter = theta * float(xlen)
    iprefix_len = xlen - int(ceil(2*lenfilter/(theta+1))) + 1
    lenfilter = int(ceil(lenfilter))
    overlapx = {}
    for posx in xrange(0, len(xprefix)):
      term = xprefix[posx]
      probe.grouping_hamming(term, ric, theta, xlen, posx, lenfilter, overlapx)
      if x[0][1] <= 0:
        if posx < iprefix_len:
          postings = rio.get(term)
          if postings == None:
            postings = [(x, posx)]
          else:
            postings.append((x, posx))
          rio[term] = postings
        continue
      if posx < iprefix_len:
        postings = ric.get(term)
        if postings == None:
          postings = [(x, posx)]
        else:
          postings.append((x, posx))
        ric[term] = postings
      probe.grouping_hamming(term, rio, theta, xlen, posx, lenfilter, overlapx)
    for p in verify.grouping(theta, esquare, xlen, xprefix, x[2], overlapx, verify_counter):
      yield p
    del overlapx
    if x[0][1] > 0:
      for p in verify.grouping_self(theta, esquare, xlen, len(xprefix), x[2], verify_counter):
        yield p


def join_reverseprobing_hamming(g, theta, esquare, verify_counter): # group, theta and epsilon square
  if len(g) <= 1:
    return
  ric = {} # inverted index for the current cell
  rio = {} # inverted index for other cells
  for x in g:
    xtext = x[3]
    xlen = len(xtext)
    xloc = x[2]
    lenfilter = theta * float(xlen)
    iprefix_len = xlen - int(ceil(2*lenfilter/(theta+1))) + 1
    lenfilter = int(ceil(lenfilter))
    xprefixlen = xlen - lenfilter + 1
    overlapx = {}
    for posx in xrange(0, xprefixlen):
      term = xtext[posx]
      probe.baseline_reverse_hamming(term, ric, theta, esquare, xloc, xlen, posx, lenfilter, overlapx)
      if x[0] <= 0:
        if posx < iprefix_len:
          postings = rio.get(term)
          if postings == None:
            postings = [(x, posx)]
          else:
            postings.append((x, posx))
          rio[term] = postings
        continue
      if posx < iprefix_len:
        postings = ric.get(term)
        if postings == None:
          postings = [(x, posx)]
        else:
          postings.append((x, posx))
        ric[term] = postings
      probe.baseline_reverse_hamming(term, rio, theta, esquare, xloc, xlen, posx, lenfilter, overlapx)
    for p in verify.verify1(theta, x[1], xtext, xlen, xprefixlen, overlapx, verify_counter):
      yield p


def join_grouping_reverseprobing_hamming(g, theta, esquare, verify_counter): # group, theta and epsilon square
  ric = {} # inverted index for the current cell
  rio = {} # inverted index for other cells
  for x in g:
    xlen = x[0][0]
    xprefix = x[0][2]
    lenfilter = theta * float(xlen)
    iprefix_len = xlen - int(ceil(2*lenfilter/(theta+1))) + 1
    lenfilter = int(ceil(lenfilter))
    overlapx = {}
    for posx in xrange(0, len(xprefix)):
      term = xprefix[posx]
      probe.grouping_reverse_hamming(term, ric, theta, xlen, posx, lenfilter, overlapx)
      if x[0][1] <= 0:
        if posx < iprefix_len:
          postings = rio.get(term)
          if postings == None:
            postings = [(x, posx)]
          else:
            postings.append((x, posx))
          rio[term] = postings
        continue
      if posx < iprefix_len:
        postings = ric.get(term)
        if postings == None:
          postings = [(x, posx)]
        else:
          postings.append((x, posx))
        ric[term] = postings
      probe.grouping_reverse_hamming(term, rio, theta, xlen, posx, lenfilter, overlapx)
    for p in verify.grouping(theta, esquare, xlen, xprefix, x[2], overlapx, verify_counter):
      yield p
    del overlapx
    if x[0][1] > 0:
      for p in verify.grouping_self(theta, esquare, xlen, len(xprefix), x[2], verify_counter):
        yield p


