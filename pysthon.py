import requests

def send_request(session, proxy):
   try:
       response = session.get('http://httpbin.org/ip', proxies={'http': f"http://{proxy}"})
       print(response.json())
   except:
       pass

if __name__ == "__main__":
   with open('list_proxy.txt', 'r') as file:
       proxies = file.readlines()