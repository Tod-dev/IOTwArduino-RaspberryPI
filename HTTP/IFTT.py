import requests
import time
import configparser
import os


ADAFRUIT_IO_USERNAME = "YOURUSERNAME"
ADAFRUIT_IO_KEY = "YOURKEY"




#If This Then That
class IFTTT():


    def setup(self):
        thisfolder = os.path.dirname(os.path.abspath(__file__))
        initfile = os.path.join(thisfolder, 'config.ini')
        self.config = configparser.ConfigParser()
        self.config.read(initfile)
        self.ADAFRUIT_IO_USERNAME = self.config.get("HTTP","ADAFRUIT_IO_USERNAME")
        self.ADAFRUIT_IO_KEY = self.config.get("HTTP","ADAFRUIT_IO_KEY")
        
    def loop(self):
        # infinite loop for serial managing
        #
        lasttime = time.time()
        while (True):

            # get from feed each 2 seconds
            ts = time.time()
            if ts-lasttime>2:

                feedname = 'test'
                headers = {'X-AIO-Key': self.ADAFRUIT_IO_KEY}
                url = 'https://io.adafruit.com/api/v2/{}/feeds/{}/data/last'.format(self.ADAFRUIT_IO_USERNAME, feedname)
                print(url)
                myGET = requests.get(url, headers=headers)
                responseJsonBody= myGET.json()
                val = responseJsonBody.get('value',None)
                print(val)


                if int(val) < 128:
                    self.sendPost(1)

                if int(val) >= 128:
                    self.sendPost(0)

                lasttime = time.time()



    def sendPost(self, val):

            mypostdata = {'value': val}
            feedname = 'test-out'
            headers = {'X-AIO-Key': self.ADAFRUIT_IO_KEY}
            url = 'https://io.adafruit.com/api/v2/{}/feeds/{}/data'.format(self.ADAFRUIT_IO_USERNAME,feedname)
            print (url)

            myPOST = requests.post(url, data = mypostdata, headers=headers)
            print(myPOST.json())




if __name__ == '__main__':
    ift=IFTTT()
    ift.setup()
    ift.loop()
