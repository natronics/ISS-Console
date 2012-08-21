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
  
    # Test
    self.s_vector_box       = self.window.add_box("State Vector")
    self.s_vec_pos          = self.window.add_textinfo(self.s_vector_box, 0, "J2000 Position (km):")
    self.s_vec_vel          = self.window.add_textinfo(self.s_vector_box, 1, "J2000 Velocity (m/s):")

  def update_view_threadsafe(self):
    wx.MutexGuiEnter()
    self.s_vec_pos.SetLabel("[%9.3f,%9.3f,%9.3f]" % (self.model.j2000_pos[0], self.model.j2000_pos[1], self.model.j2000_pos[2]))
    self.s_vec_vel.SetLabel("[%9.3f,%9.3f,%9.3f]" % (self.model.j2000_vel[0], self.model.j2000_vel[1], self.model.j2000_vel[2]))
    wx.MutexGuiLeave()
