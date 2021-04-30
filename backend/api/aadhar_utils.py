from PIL import Image
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import pytesseract
import io
from twocaptcha import TwoCaptcha
import time

def get_captcha(img):
    api_key="483852b189a89e09da6919178ae88526"
    solver = TwoCaptcha(api_key, defaultTimeout=100, pollingInterval=5)
    try:
        result = solver.normal(img,caseSensitive=1)

    except Exception as e:
        print(e)

    else:
        print(result)
        return result['code']

def verify_aadhar(aadhar):
    opts = Options()
    opts.headless = True
    driver = webdriver.Firefox(executable_path='/home/nishad/Desktop/geckodriver',options=opts)
    driver.get('https://resident.uidai.gov.in/verify')
    driver.find_element_by_name('uidno').send_keys(aadhar)
    img_path="./"+aadhar+".png"

    #text = pytesseract.image_to_string(threshold(image))
    #error
    for i in range(10):
        image=driver.find_element_by_id('captcha-img').screenshot(img_path)
        captcha = get_captcha(img_path)
        print('sleep', captcha)
        time.sleep(3)
        if(captcha!=None):
            driver.find_element_by_name('security_code').send_keys(captcha)
            try:
                driver.find_element_by_xpath('#/html/body/div[2]/div[2]/div[2]/div[1]/div/div[4]/div/div/div[2]/div/div/form/div[2]/div/div/div/div[1]/div')
            except:
                driver.find_element_by_id("submitButton").click()
                time.sleep(5)
                texts = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[1]/div/div[4]/div/div/div/div/div').text
                if('Captcha' in texts):
                    print('wrong code')
                    continue
                else:
                    break

    time.sleep(5)
    string=driver.find_element_by_id('maincontent').text
    if('Aadhaar Number '+aadhar+' Exists!' in string):
        return True
    else:
        return False