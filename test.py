import datetime,time
now = datetime.datetime.now()
minute = time.strftime("%M",now.timetuple())
minute_start = 0 if int(minute) - 30 < 0 else 30
minute_end = 0 if minute_start == 30 else 30
firest_start = time.strftime("%Y-%m-%d %H:" + str(minute_start) + ":0",now.timetuple())
firest_end = time.strftime("%Y-%m-%d %H:" + str(minute_end) + ":0",now.timetuple())
print("start",minute_start)
print("end",minute_end)