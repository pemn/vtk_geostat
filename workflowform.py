#!python
# Parameterized form with yaml persistence

import os, os.path, param, yaml, threading
import panel as pn
from functools import partial
webview = None

# shorten paths when they are subdirectories of the current working dir
def relative_paths(path):
  cwd_drive, cwd_tail = os.path.splitdrive(os.getcwd().lower())
  path_drive, path_tail = os.path.splitdrive(path.lower())
  if cwd_drive == path_drive and os.path.commonpath([path_tail, cwd_tail]) == cwd_tail:
    return os.path.relpath(path)
  return(path)

class Step(param.Parameterized):
  panel = pn.panel

def winforms_file_dialog(dialog_type, allow_multiple = False):
  import clr
  clr.AddReference('System.Windows.Forms') 
  import System.Windows.Forms as WinForms

  file_path = None
  if dialog_type == webview.OPEN_DIALOG:
    dialog = WinForms.OpenFileDialog()
    dialog.Multiselect = allow_multiple
    dialog.RestoreDirectory = True
    if dialog.ShowDialog() == WinForms.DialogResult.OK:
      file_path = tuple(dialog.FileNames)
  
  if dialog_type == webview.FOLDER_DIALOG:
    dialog = WinForms.FolderBrowserDialog()
    dialog.RestoreDirectory = True
    if dialog.ShowDialog() == WinForms.DialogResult.OK:
      file_path = (dialog.SelectedPath,)

  if dialog_type == webview.SAVE_DIALOG:
    dialog = WinForms.SaveFileDialog()
    dialog.RestoreDirectory = True
    if dialog.ShowDialog() == WinForms.DialogResult.OK:
      file_path = dialog.FileName

  return file_path


def webview_create_file_dialog(dialog_type, allow_multiple = False):
  global webview
  if webview is not None:
    w = webview.active_window()
    if w is not None:
      return w.create_file_dialog(dialog_type, allow_multiple)
  # fall back to Winforms
  return winforms_file_dialog(dialog_type, allow_multipe)  

class WorkFlowForm(list, param.Parameterized):
  _file = None
  _keys = None
  _qta = None

  def __init__(self, file = None, ww = None):
    if file is not None:
      self._file = file
    if ww is not None:
      ClientFileDialog.set_ww(ww)
    self.load()

  def widget(self, t, v):
    w = None
    if t == 'Integer':
      w = pn.widgets.IntInput(value=v)
    elif t == 'Boolean':
      w = pn.widgets.Checkbox(value=v)
    elif t == 'MultiFileSelector':
      w = pn.widgets.LiteralInput(value=v)
    elif t == 'Float':
      w = pn.widgets.FloatInput(value=v)
    elif t == 'List':
      w = pn.widgets.LiteralInput(value=v)
    else:
      w = pn.widgets.TextInput(value=v)

    return w

  def load(self, file = None):
    self.clear()
    if file is None:
      if self._file is None:
        return
      else:
        file = self._file
    if isinstance(file, list):
      data = file
    else:
      if not os.path.exists(file):
        return
      self._name = os.path.splitext(os.path.basename(file))[0]
      with open(file, 'r') as f:
        data = yaml.safe_load(f)
    for k,t,v in data:
      self.append([k, t, self.widget(t, v)])

  def get(self, key, default = None):
    for k,t,w in self:
      if k == key:
        return w.value

    return default

  def set(self, key, v):
    for k,t,w in self:
      if k == key:
        if t == 'FileSelector' and isinstance(v, (list,tuple)):
          v = ','.join(v)
        w.value = v

  def keys(self):
    return [k for k,t,w in self]

  def values(self):
    return [self.get(k) for k,t,w in self]

  def items(self, event = None):
    return [(k, self.get(k)) for k,t,w in self]
  
  def dump(self, event = None):
    # MUST use list instead of tuple or YAML will be incorrect
    return [[k, t, self.get(k)] for k,t,w in self]

  def save(self, file = None):
    if not isinstance(file, str):
      file = None

    if file is None:
      if self._file is None:
        return
      else:
        file = self._file

    with open(file, 'w') as f:
      yaml.dump(self.dump(), f)

  def file_browse(self, k, t, e = None):
    fl = None
    global webview
    if webview is not None:
      fl = self.wv_file_dialog(k, t)
    else:
      fl = self.qt_file_dialog(k, t)
    if fl is not None:
      fl = list(map(relative_paths, fl))

    if fl is not None:
      self.set(k, fl)

  def random_seed(self, k, e = None):
    import random
    self.set(k, random.randrange(100))

  def wv_file_dialog(self, k = '', t = ''):
    # OPEN_DIALOG = 10
    # FOLDER_DIALOG = 20
    # SAVE_DIALOG = 30
    dialog_type = 10
    allow_multiple = False
    if t == 'MultiFileSelector':
      allow_multiple = True
    if k.lower().startswith('output'):
      dialog_type = 30

    return webview_create_file_dialog(dialog_type, allow_multiple)

  @classmethod
  def qt_file_dialog(self, k = '', t = ''):
    from PyQt5.QtWidgets import QApplication, QFileDialog
    if self._qta is None:
      self._qta = QApplication([])

    fd = QFileDialog()

    if k.lower().startswith('output'):
      fd.setAcceptMode(QFileDialog.AcceptSave)
    if t == 'MultiFileSelector':
      fd.setFileMode(QFileDialog.ExistingFiles)

    if fd.exec():
      return tuple(fd.selectedFiles())

    return None

  def __call__(self):
    return self.panel()

  def __panel__(self):
    return self.panel()

  def panel(self):
    p = pn.GridBox(ncols=3)
    for k,t,w in self:
      p.append(k)
      p.append(w)
      b = None
      if t.endswith('FileSelector'):
        b = pn.widgets.Button(icon='folder-open')
        b.on_click(partial(self.file_browse, k, t))
      if t == 'Integer':
        b = pn.widgets.Button(icon='dice')
        b.on_click(partial(self.random_seed, k))

      p.append(b)

    p.append(self._file)
    b = pn.widgets.Button(name='save', icon='device-floppy', sizing_mode='stretch_width', min_width=120, icon_size='2em')
    b.on_click(self.save)
    p.append(b)
    return p

class WorkFlowForm_pp(param.Parameterized):
  _file = None
  _keys = None
  _qtapp = None
  live = param.Boolean(precedence=-1)

  def dump(self, event = None):
    d = []
    for k in self.param:
      if self.param[k].precedence != -1 and not self.param[k].constant:
        t = self.param[k]
        v = getattr(self, k)
        #if isinstance(t, param.parameters.FileSelector):
        #  v = None
        d.append([k, type(t).__name__, v])
    return d

  def save(self, file = None):
    if not isinstance(file, str):
      file = None
    WorkFlowForm.save_file(self, file)

  @classmethod
  def save_file(cls, self, file = None):
    if file is None:
      if cls._file is None:
        return
      else:
        file = cls._file

    with open(file, 'w') as f:
      yaml.dump(self.dump(), f)

  @classmethod
  def load(cls, file, **kwargs):
    if file is not None:
      if isinstance(file, list):
        data = file
      else:
        cls._file = file
        with open(file, 'r') as f:
          data = yaml.safe_load(f)
      for k,t,v in data:
        if k not in kwargs:
          f = getattr(param, t)
          kwargs[k] = f(default=v)

    return cls.factory(**kwargs)

  @classmethod
  def factory(cls, **kwargs):
    name = cls.__name__
    if cls._file is not None:
      name = os.path.basename(cls._file)
    ''' create a custom class instance that has the methods given as kwargs'''
    c = type(name, (cls,), kwargs)
    self = c()
    self._keys = kwargs.keys()
    return self


  def __getitem__(self, key):
    return self.get(key)

  def get(self, key, default = None):
    if hasattr(self, key):
      return getattr(self, key)
    return default

  def items(self):
    return [(k, getattr(self, k)) for k in self.keys()]

  def keys(self):
    return self._keys

  def __call__(self):
    return self.__panel__()

  def __panel__(self):
    w = {}
    for k in self.keys():
      t = getattr(self.param, k)
      if isinstance(t, param.parameters.FileSelector):
        w[k] = pn.widgets.FileSelector
    p = pn.GridBox(ncols=2)
    p.append(pn.Param(self, widgets=w))
    #p.append(pn.Column(*[_ for _ in self.keys()]))
    #p.append(pn.layout.spacer.Spacer())
    bt_save = pn.widgets.Button(name='save', icon='device-floppy', sizing_mode='stretch_width', min_width=120, icon_size='2em')
    bt_save.on_click(self.save)
    p.append(bt_save, bt_play)
    return p

# serverless alternative for running a panel pipeline
class WorkFlowCall(param.Parameterized):
  form = WorkFlowForm()
  df = param.DataFrame(precedence=-1)

  @classmethod
  def factory(cls, call=None, form=None, **kwargs):
    ''' create a new subclass with the given callback and name '''
    if 'name' not in kwargs and call is not None:
      kwargs['name'] = call.__name__

    name = kwargs.get('name','')
    m = dict()
    if call is not None:
      m['__call__'] = call
    c = type(cls.__name__ + '_' + name, (cls,), m)(form, **kwargs)
    return c

  def __init__(self, form=None, **kwargs):
    super().__init__(**kwargs)
    if form is not None:
      self.form = form

  def next(self, step = None):
    ''' fill parameters from previous step on this step '''
    if step is not None:
      for k in self.param:
        if self.param[k].precedence == -1 and not self.param[k].constant:
          setattr(self, k, getattr(step, k))
    return self

  @param.depends('form.live')
  def view(self):
    data = pn.Row()
    if self.form.live:
      if callable(self):
        data.append(self())        
      for name, (_, method, index) in self.param.outputs().items():
        data.append(method())        
    else:
      data.append('💤')
    return data

  def __panel__(self):
    ''' magic hook for regular Panels '''
    return self.view

  def panel(self):
    ''' magic hook only for Pipeline '''
    return self.view

def webview_panel_start(p, url = 'http://localhost:5000'):
  global webview
  import webview

  w = webview.create_window(None, url, maximized=False)

  t0 = threading.Thread(target=lambda: pn.serve(p, port=5000, show=False), daemon=True)
  t0.start()
  webview.start()

if __name__=='__main__':
  webview_panel_start(WorkFlowForm('workflowform.yaml'))
