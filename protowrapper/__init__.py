import sys
import inspect

class ValidationError(Exception):
  pass

def patch_setattr(what):
  old_setattr = what.__setattr__
  def new_setattr(self, name, value):
    old_setattr(self, name, value)
    if hasattr(self, "check_" + name):
      check_name = getattr(self, 'check_' + name)
      if callable(check_name):
        if not check_name():
          raise ValidationError("check_" + name + " failed")

  if not hasattr(what, '__big_ugly_protowrapping_monkey_patch'):
    setattr(what, '__setattr__', new_setattr)
    setattr(what, '__big_ugly_protowrapping_monkey_patch', True)
  else:
    sys.stderr.write("Warning: patched " + what.__name__ + " multiple times")

def add_init(what, func):
  old_init = what.__init__
  def new_init(self, *args, **kwargs):
    old_init(self, *args, **kwargs)
    spec = inspect.getfullargspec(func)
    if len(spec[0]) != 1 or spec[1] is not None or spec[2] is not None:
      func(self, *args, **kwargs)
    else:
      func(self)
  what.__init__ = new_init

class ProtowrapperMeta(type):
  def __new__(cls, name, bases, attrs):
    if name != 'Protowrapper':
      frame = inspect.currentframe()
      try:
        if name not in frame.f_back.f_globals:
          raise TypeError("Could not find protobuffer " + name)
        Protobuffer = frame.f_back.f_globals[name]
        patch_setattr(Protobuffer)
        for name, attr in attrs.items():
          if name == 'init':
            add_init(Protobuffer, attr)
          else:
            setattr(Protobuffer, name, attr)
        return Protobuffer
      # print(globals()[name[0:-len(ProtowrapperMeta.suffix)]])
      finally:
        del frame
    return super().__new__(cls, name, bases, attrs)

class Protowrapper(object,metaclass=ProtowrapperMeta):
  pass         
