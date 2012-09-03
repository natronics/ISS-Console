import datetime

GPS_EPOCH = datetime.datetime(1980,1,6,0,0,0)

def gps2dt(s):
  days = int(s.split('/')[0])
  
  hms = s.split('/')[1].split(':')
  h = int(hms[0])
  m = int(hms[1])
  s = int(hms[2])
  
  dt = GPS_EPOCH + datetime.timedelta(days=days, hours=h, minutes=m, seconds=s)
  return dt

def age(dt):
  now = datetime.datetime.utcnow()
  diff = now - dt
  days = diff.days
  secs = diff.seconds
  
  return (days * 86400) + secs
