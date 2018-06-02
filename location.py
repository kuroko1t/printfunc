import inspect
import os

def location(depth=0):
  frame = inspect.currentframe().f_back
  with open('log.txt','a') as f:
      f.write(__file__ + ',')
      f.write(frame.f_code.co_name + ',')
      f.write(frame.f_lineno + ',')
      f.write(frame.f_lineno + '\n' )
  return __file__, frame.f_code.co_name, frame.f_lineno,inspect.getargvalues(frame)