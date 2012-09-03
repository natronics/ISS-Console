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

JARGON =  {   'S3AFT':      "S3 Aft"
            , 'S1UPOB':     "S1 Upper Outboard"
            , 'S1LOOB':     "S1 Lower Outboard"
            , 'S1UPIB':     "S1 Upper Inboard"
            , 'S1LOIB':     "S1 Lower Inboard"
            , 'P1UPIB':     "P1 Upper Inboard"
            , 'P1LOIB':     "P1 Lower Inboard"
            , 'P1UPOB':     "P1 Upper Outboard"
            , 'P1LOOB':     "P1 Lower Outboard"
            , 'P3AFT':      "P3 Aft"
            , 'NOD2LO':     "Node 2 Nadir"
            , 'NOD1UP':     "Node 1 Zenith"
            , 'LABS':       "Lab Starboard"
            , 'NOD3S':      "Node 3 Starboard/Forward"
            , 'BLEE':       "SSRMS Base LEE"
            , 'BELB':       "SSRMS Base Elbow"
            , 'TELB':       "SSRMS Tip Elbow"
            , 'TLEE':       "SSRMS Tip LEE"
            , 'POA':        "MBS POA"
            , 'MBS CLPA':   "MBS CLPA LAUNCH"
            , 'MAST':       "MBS CLPA"
            , 'SPDMS1':     "SPDM Spare"
            , 'SPDMS2':     "SPDM Spare"
            , 'SPDMLEE':    "SPDM LEE"
            , 'OTCM1':      "SPDM Arm 1 OTCM"
            , 'BODY1':      "SPDM Body Camera 1"
            , 'OTCM2':      "SPDM Arm 2 OTCM"
            , 'BODY2':      "SPDM Body Camera 2"
            , 'SSRMS PL1':  "MSS Payload Camera 1"
            , 'SSRMS PL2':  "MSS Payload Camera 2"
            , 'SSRMS PL3':  "MSS Payload Camera 3"
            , 'MSS PL1':    "MSS Payload Camera 4"
            , 'MSS PL2':    "MSS Payload Camera 5"
            , 'JPM a':      "JEM Channel 1"
            , 'JPM b':      "JEM Channel 2"
            , 'COL 1':      "APM Channel 1"
            , 'COL 2':      "APM Channel 2"
            , 'ORB1':       "Orbiter Channel 1"
            , 'ORB2':       "Orbiter Channel 2"
            , 'Lab AVU1':   "AVU1 Channel A"
            , 'Lab AVU2':   "AVU1 Channel B"
            , 'CUP AVU1':   "AVU2 Channel A"
            , 'CUP AVU2':   "AVU2 Channel B"
            , 'VTR1':       "VTR1 PLAYBACK"
            , 'VTR2':       "VTR2 PLAYBACK"
            , 'SCU1':       "SCU 1 MUX Output"
            , 'SCU2':       "SCU 2 MUX Output"
            , 'SCU1 Test':  "SCU 1 Test Pattern"
            , 'SCU2 Test':  "SCU 2 Test Pattern"
            , 'LABCAM':     "LAB Camcorder"
            , 'A/L CAM':    "Airlock Camcorder"
            , 'N1 CAM':     "Node 1 Camcorder"
            , 'N3 CAM':     "Node 3 Camcorder"
            , 'LAB1D3':     "ISPR LAB1D3"
            , 'LAB1P2':     "ISPR LAB1P2"
            , 'LAB1P4':     "ISPR LAB1P4"
            , 'LAB105':     "ISPR LAB1O5"
            , 'LAB104':     "ISPR LAB1O4"
            , 'LAB103':     "ISPR LAB1O3"
            , 'LAB102':     "ISPR LAB1O2"
            , 'LAB101':     "ISPR LAB1O1"
            , 'LAB1S1':     "ISPR LAB1S1"
            , 'LAB1S2':     "ISPR LAB1S2"
            , 'LAB1S3':     "ISPR LAB1S3"
            , 'LAB1S4':     "ISPR LAB1S4"
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
                if self.verbose:
                  #print key, rawdata
                  pass
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
