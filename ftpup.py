import ftplib
from datetime import datetime, timedelta
import time
stime = time.time()

session = ftplib.FTP('144.24.105.86','admin_epg','123456')

file = open('allepg.xml.gz','rb')                  # file to send
session.storbinary('STOR allepg.xml.gz', file)     # send the file
file.close()                                    # close file and FTP
session.quit()
# print("Update done")
print("FTP updated", datetime.now())
print(f"Took {time.time()-stime:.2f} seconds")