import httplib
import urllib
import time
import json

ISS_KEY = {   'statex': {'name': "J2000 State Vector - X (km)", 'key': "USLAB000032"}
            , 'statey': {'name': "J2000 State Vector - Y (km)", 'key': "USLAB000033"}
            , 'statez': {'name': "J2000 State Vector - Z (km)", 'key': "USLAB000034"}
            , 'beta': {'name': "Solar Beta angle",            'key': "USLAB000040"}
            , 'CMG1status': {'name': "Control Moment Gyroscope (CMG)-1 On-Line", 'key': "USLAB000001"}
            , 'CMG2status': {'name': "Control Moment Gyroscope (CMG)-2 On-Line", 'key': "USLAB000002"}
            , 'CMG3status': {'name': "Control Moment Gyroscope (CMG)-3 On-Line", 'key': "USLAB000003"}
            , 'CMG4status': {'name': "Control Moment Gyroscope (CMG)-4 On-Line", 'key': "USLAB000004"}
            , 'CMGnum': {'name': "Number of Control Moment Gyroscope (CMG)s Online", 'key': "USLAB000005"}
            , 'CMGrollt': {'name': "Control Moment Gyroscope (CMG) Control Torque - Roll (N-m)", 'key': "USLAB000006"}
            , 'CMGpitcht': {'name': "Control Moment Gyroscope (CMG) Control Torque - Pitch (N-m)", 'key': "USLAB000007"}
            , 'CMGyawt': {'name': "Control Moment Gyroscope (CMG) Control Torque - Yaw (N-m)", 'key': "USLAB000008"}
            , 'CMGp': {'name': "Active Control Moment Gyroscope (CMG) Momentum (Nms)", 'key': "USLAB000009"}
            , 'CMGppercent': {'name': "Control Moment Gyroscope (CMG) Momentum Percentage", 'key': "USLAB000010"}
            , 'CMGdsat': {'name': "Desaturation Request (Enabled/Inhibited)", 'key': "USLAB000011"}
            , 'GNCmode': {'name': "US Guidance, Navigation and Control (GNC) Mode", 'key': "USLAB000012"}
            , 'attsource': {'name': "US Attitude Source", 'key': "USLAB000013"}
            , 'ratesource': {'name': "US Rate Source", 'key': "USLAB000014"}
            , 'statesource': {'name': "US State Vector Source", 'key': "USLAB000015"}
            , 'attcontroller': {'name': "Attitude Controller Type", 'key': "USLAB000016"}
            , 'attframe': {'name': "Attitude Control Reference Frame", 'key': "USLAB000017"}
            , 'ku1status': {'name': "Ku-Band Video Downlink Channel 1 Activity", 'key': "USLAB000088"}
            , 'vid1source': {'name': "Video Source Routed to Downlink 1", 'key': "USLAB000095"}
            , 'utc': {'name': "Greenwich Mean Time (GMT)", 'key': "TIME_000001"}
            , 'utcyear': {'name': "Year", 'key': "TIME_000002"}
            , 'statevx': {'name': "J2000 State Vector Velocity - X (m/s)", 'key': "USLAB000035"}
            , 'statevy': {'name': "J2000 State Vector Velocity - Y (m/s)", 'key': "USLAB000036"}
            , 'statevz': {'name': "J2000 State Vector Velocity - Z (m/s)", 'key': "USLAB000037"}
            , 'statetime': {'name': "State vector time tag", 'key': "USLAB000102"}
            #, '': {'name': "", 'key': ""}
          }

JARGON = {'S1LOOB': "S1 Lower Outboard Camera"}

class ISSLive():
  """A class to get real time data from the space station"""
  
  def __init__(self, keys, vebose=False):
    self.keys     = keys
    self.verbose  = vebose
    self.buffer   = ""
  
  def start(self, callback):
    self.create_session()
    self.send_control()
    
    while (1):
      self.buffer += self.streaming.read(1)
      data = self.parse_data()
      if data:
        callback(data)

  def parse_data(self):
    ret = {}
    if '\n' in self.buffer:
      if "1,1|" in self.buffer:
        data = self.buffer.split("1,1|")[0].strip()
        data = data.split("|")
        for d in data:
          try:
            rawdata = json.loads(d)
            for key in ISS_KEY:
              if rawdata["Name"] == ISS_KEY[key]['key']:
                ret[key] = rawdata["CalibratedData"]
                if self.verbose:
                  print key, rawdata
                break
          except:
            pass
        self.buffer = ""
    return ret
  
  def create_session(self):
    params = urllib.urlencode({   'LS_adapter_set':     'PROXYTELEMETRY'
                                , 'LS_client_version':  '5.0'
                                , 'LS_domain':          'nasa.gov'
                             })

    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    
    conn = httplib.HTTPConnection("push1.jsc.nasa.gov:80")
    conn.request("POST", "/lightstreamer/create_session.txt", params, headers)
    response = conn.getresponse()
    
    if self.verbose:
      print response.status
    self.streaming = response
    session = response.read(79).split("SessionId:")[1]
    session = session.split('\n')[0].strip()
    print session
    self.session = session
  
  def send_control(self):
    
    # Container for lightstreamer keys to ask for
    k = ""
    for key in self.keys:
       k += ISS_KEY[key]['key'] + " "
    
    params = urllib.urlencode({   'LS_id':      "ISPWebItem"
                                , 'LS_mode':    "RAW"
                                , 'LS_op':      "add"
                                , 'LS_schema':   k
                                , 'LS_session':  self.session
                                , 'LS_table':    1
                              })
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = httplib.HTTPConnection("push1.jsc.nasa.gov:80")
    conn.request("POST", "/lightstreamer/control.txt", params, headers)
    response = conn.getresponse()
    
    print response.status, response.reason
