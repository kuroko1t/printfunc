import inspect
import os,re

def location():
  frame = inspect.currentframe().f_back
  local_dict = inspect.getargvalues(frame).locals
  #path_split = __file__.split('/')
  #egg_num = [i for i, name in enumerate(path_split) if re.search('\.egg$',name)]
  path = ''
  #if len(egg_num) > 1:
  #  for i , name in enumerate(path_split):
  #    if i > egg_num[0]:
  #      path += '/{}'.format(name)
  #else:
  #path = __file__
  m = re.search('\.egg/(.+)',__file__)
  if m:
    path = m.group(1)
  else:
    path = __file__
  with open('log.txt','a') as f:
      f.write('{}'.format(path) + ' ,')
      f.write('{}'.format(frame.f_lineno) + '\n')
      f.write('func:[{}]'.format(frame.f_code.co_name) + '\n')
      for name, value in local_dict.items():
        f.write('{}:{}'.format(name,value) + ' ,')
      if local_dict:
        f.write('\n#----#\n')
      else:
        f.write('#----#\n')
  return path, frame.f_code.co_name, frame.f_lineno,inspect.getargvalues(frame).locals
