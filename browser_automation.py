def open_link(proxy, url, x): 
  from selenium import webdriver
  from webdriver_manager.chrome import ChromeDriverManager
  from selenium.webdriver.common.keys import Keys
  from selenium.webdriver.common.desired_capabilities import DesiredCapabilities    

  # logging config which is not completly understandable now probably will go away soonish
  d = DesiredCapabilities.CHROME
  d['goog:loggingPrefs'] = { 'browser':'ALL' }

  chrome_options = webdriver.ChromeOptions()
  chrome_options.add_argument('--incognito')
  
  if proxy == True: 
    # proxy config
    PROXY = "127.0.0.1:4001" 
    chrome_options.add_argument('--proxy-server=http://%s' % PROXY)

  driver = webdriver.Chrome(ChromeDriverManager().install(), desired_capabilities=d, chrome_options=chrome_options)
  
  # remote and local ip logging 
  import socket
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
  remote_ip = socket.gethostbyname(url)
  print(remote_ip)
  s.connect((remote_ip, 80))
  local_ip = s.getsockname()[0] 
  print(local_ip)
  s.close()
  

  # creating directories
  import os
  if not os.path.exists(url):
      os.makedirs(url)

  # starting tcpdump
  filename = url + '/cap' + str(x) + '.pcap'
  import subprocess
  p = subprocess.Popen(['tcpdump', 'port', '443', '-w', filename], stdout=subprocess.PIPE)

  url = "https://" + url
  driver.get(url)

  for entry in driver.get_log('browser'):
      print (entry)

         
  #Time
  #navigationStart is the first timestamp available by window.performance.timing
  navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
  #loadEventEnd is the last timestamp available by window.performance.timing
  loadEventEnd = driver.execute_script("return window.performance.timing.loadEventEnd")  

  print("Timestamp Start: %s" % navigationStart) 
  print("Timestamp Finish: %s" % loadEventEnd)



  driver.close()
  p.terminate()

def main():
  for x in range(1,100):
    open_link(True, 'www.google.de', x)
    open_link(True, 'www.b-tu.de', x)
    open_link(True, 'www.heise.de', x)
  
if name == "main":
  main()
