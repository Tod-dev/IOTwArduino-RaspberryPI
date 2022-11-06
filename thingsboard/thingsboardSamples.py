import requests
import json
import time

host='127.0.0.1'
port= 8080
bearer_token=""


def simDevicePost():
    DEVICE_TOKEN ='T2_TEST_TOKEN'
    url = 'http://{host}:{port}/api/v1/{ACCESS_TOKEN}/telemetry'.format(host=host,port=port,ACCESS_TOKEN=DEVICE_TOKEN)
    print (url)
    values = {"temperature":23, "humidity": 45.7}
    resp = requests.post(url,data=json.dumps(values))
    print (resp)

def simDeviceAttributePost():
    DEVICE_TOKEN ='T1_TEST_TOKEN'
    url = 'http://{host}:{port}/api/v1/{ACCESS_TOKEN}/attributes'.format(host=host,port=port,ACCESS_TOKEN=DEVICE_TOKEN)
    print (url)
    values = {"mykey1":23, "mykey2": "ciao"}
    resp = requests.post(url,data=json.dumps(values))
    print (resp)


def simDeviceGet():
    DEVICE_TOKEN ='T1_TEST_TOKEN'
    DEVICE_ID='yourdeviceID'
    url = 'http://{host}:{port}/api/plugins/telemetry/DEVICE/{ID}/values/timeseries'.format(host=host,port=port,ID=DEVICE_ID)
    print (url)
    headers={'Accept': 'application/json', 'x-authorization': 'Bearer {bearer_token}'.format(bearer_token=bearer_token)}

    resp = requests.get(url,headers=headers)
    print (resp)
    print(resp.json())


def getAdminToken():
    global bearer_token
    url ='http://{host}:{port}/api/auth/login'.format(host=host,port=port)
    auth = {"username":"tenant@thingsboard.org", "password": "tenant" }
    headers = {"Accept":"application/json"}

    resp = requests.post(url,data=json.dumps(auth), headers=headers)
    print (resp)
    print(resp.json())
    bearer_token=resp.json()['token']


def GetAttributes():
    DEVICE_ID='yourdeviceID'
    url = 'http://{host}:{port}/api/plugins/telemetry/DEVICE/{DEVICE_ID}/values/attributes/SERVER_SCOPE'.format(host=host,port=port,DEVICE_ID=DEVICE_ID)
    headers={'Accept': 'application/json', 'x-authorization': 'Bearer {bearer_token}'.format(bearer_token=bearer_token)}
    resp=requests.get(url, headers=headers )
    print (resp)
    print(resp.json())

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    getAdminToken()
    simDeviceGet()
    time.sleep(5)

    while (True):
        simDevicePost()
        time.sleep(5)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
