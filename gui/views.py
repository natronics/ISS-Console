import framework
import wx

class MainWindow(object):
  
  def __init__(self, controller, model):
    self.window   = framework.Window(None, "ISS Console")
    self.model    = model
    self.control  = controller
    
    self.init_UI()
    
    self.window.add_widgets()

  def init_UI(self):
  
    self.s_vector_box       = self.window.add_box("State Vector")
    self.s_time             = self.window.add_textinfo(self.s_vector_box, 0, "State Vector Timestamp:  ")
    self.s_age              = self.window.add_textinfo(self.s_vector_box, 1, "State Vector Age:  ")
    self.s_vec_pos          = self.window.add_textinfo(self.s_vector_box, 2, "J2000 Position (km): ")
    self.s_vec_vel          = self.window.add_textinfo(self.s_vector_box, 3, "J2000 Velocity (m/s): ")
    
    self.comm_box           = self.window.add_box("Downlink")
    self.ku1_status         = self.window.add_textinfo(self.comm_box, 0, "Ku Downlink 1 Status: ")
    self.ku1_source         = self.window.add_textinfo(self.comm_box, 1, "Ku Downlink 1 Source: ")
    
  def update_view_threadsafe(self):
    wx.MutexGuiEnter()
    self.s_vec_pos.SetLabel("[%9.3f, %9.3f, %9.3f]" % (self.model.j2000_pos[0], self.model.j2000_pos[1], self.model.j2000_pos[2]))
    self.s_vec_vel.SetLabel("[%9.3f, %9.3f, %9.3f]" % (self.model.j2000_vel[0], self.model.j2000_vel[1], self.model.j2000_vel[2]))
    self.s_time.SetLabel(self.model.state_time.strftime("%Y-%m-%d %H:%M:%S"))
    self.s_age.SetLabel("%0.1f seconds" % self.model.state_time_age)
    self.ku1_status.SetLabel(self.model.ku1_status)
    if self.model.ku1_status.lower() == 'active':
      self.ku1_status.SetForegroundColour(framework.text_green)
    else:
      self.ku1_status.SetForegroundColour(framework.text_soft)
    self.ku1_source.SetLabel(self.model.ku1_source)
    wx.MutexGuiLeave()
