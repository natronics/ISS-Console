import httplib
import urllib
import time
import json

ISS_KEY = {   'statex': {'name': "J2000 State Vector - X (km)", 'key': "USLAB000032"}
            , 'statey': {'name': "J2000 State Vector - Y (km)", 'key': "USLAB000033"}
            , 'statez': {'name': "J2000 State Vector - Z (km)", 'key': "USLAB000034"}
            , 'beta':   {'name': "Solar Beta angle",            'key': "USLAB000040"}
            #, '': {'name': "", 'key': ""}
          }

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
