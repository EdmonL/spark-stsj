from pyspark import AccumulatorParam

class MaxAccumParam(AccumulatorParam):

  def zero(self, initialValue):
    return None

  def addInPlace(self, a, b):
    if a == None:
      return b
    if b == None:
      return a
    return max(a, b)



class MinAccumParam(AccumulatorParam):

  def zero(self, initialValue):
    return None

  def addInPlace(self, a, b):
    if a == None:
      return b
    if b == None:
      return a
    return min(a, b)
  


