import wx
import views

background = '#222222'
text_main  = '#eeeeee'
text_soft  = '#aaaaaa'
text_green = '#44ee44'

class Window(wx.Frame):

  def __init__(self, parent, title):
    wx.Frame.__init__(self, parent, title=title
                      , size = (1100, 750)
                      , style = wx.DEFAULT_FRAME_STYLE|wx.NO_FULL_REPAINT_ON_RESIZE)

    self.container  = wx.Panel(self)
    self.control    = self.container
    self.vbox       = wx.BoxSizer(wx.VERTICAL)
    self.sections   = []
    
    self.container.SetBackgroundColour(background)

  def add_box(self, label):
    widget    = wx.Panel(self.container)
    wrapper   = wx.BoxSizer(wx.VERTICAL)
    
    box       = wx.StaticBox(widget, label=label)
    boxsizer  = wx.StaticBoxSizer(box, wx.VERTICAL)
    sizer     = wx.GridBagSizer(4, 4)

    box.SetForegroundColour(text_soft)
    
    boxsizer.Add(sizer, flag=wx.LEFT|wx.TOP|wx.EXPAND)
    
    sizer.AddGrowableCol(2)
    #widget.SetSizerAndFit(sizer)
    
    wrapper.Add(boxsizer,flag=wx.ALL|wx.EXPAND)
    widget.SetSizer(wrapper)
    widget.SetBackgroundColour(background)
    widget.SetForegroundColour(text_main)
    
    self.sections.append(widget)
    return (widget, sizer)

  def add_textbox(self, box, row, label, units):
    labeltext = wx.StaticText(box[0], label=label, style=wx.ALIGN_CENTRE)
    info      = wx.TextCtrl(box[0])
    info.Disable()
    units     = wx.StaticText(box[0], label=units, style=wx.ALIGN_CENTRE)
    
    box[1].Add(labeltext, pos=(row, 0), flag=wx.TOP|wx.BOTTOM, border=0)
    box[1].Add(info,      pos=(row, 1))
    box[1].Add(units,     pos=(row, 2), flag=wx.TOP|wx.BOTTOM, border=0)
    
    return info
  
  def add_button(self, box, row, label, callback):
    button    = wx.Button(box[0], label=label)
    button_id = button.GetId()
    box[1].Add(button, pos=(row, 0), flag=wx.TOP|wx.BOTTOM, border=5)
    
    self.Bind(wx.EVT_BUTTON, callback, id=button_id)
    
    return button
  
  def add_dropdown(self, box, row, label):
    labeltext = wx.StaticText(box[0], label=label, style=wx.ALIGN_CENTRE)
    combo     = wx.ComboBox(box[0])
    
    box[1].Add(labeltext, pos=(row, 0), flag=wx.TOP|wx.BOTTOM, border=5)
    box[1].Add(combo,     pos=(row, 1), span=(1,2), flag=wx.TOP|wx.BOTTOM|wx.EXPAND, border=5)

    return combo
  
  def add_textinfo(self, box, row, label):
    labeltext = wx.StaticText(box[0], label=label, style=wx.ALIGN_CENTRE)
    info      = wx.StaticText(box[0])
    
    info.SetFont(wx.Font(9,wx.FONTFAMILY_TELETYPE,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL))
    #info.SetForegroundColour('#eeeeee')
    
    box[1].Add(labeltext, pos=(row, 0), flag=wx.TOP|wx.BOTTOM, border=2)
    box[1].Add(info,      pos=(row, 1), flag=wx.TOP|wx.BOTTOM, border=2)
    
    return info
  
  def add_widgets(self):
    for section in self.sections:
      self.vbox.Add(section, flag=wx.ALL|wx.EXPAND, border=6)
    
    self.container.SetSizer(self.vbox)
    
    self.Centre()
    self.Show(True)
    
class Application():

  def __init__(self):
    self.app  = wx.App()
    
  def run(self):
    self.app.SetTopWindow(self.main.window)
    self.app.MainLoop()
