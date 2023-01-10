from selenium_recaptcha.components import find_until_located, find_until_clicklable
from selenium_recaptcha import Recaptcha_Solver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from urllib.parse import quote_plus
from seleniumwire import webdriver
from time import sleep
import os

def get_int(text:str) -> int:
    number=''
    for letter in text:
        if letter.isdigit():
            number+=letter
    return int(number)

def interceptor(request):
    if 'pagead2.googlesyndication.com' in request.url:
        request.abort()
    request.headers['X-Requested-With'] = 'com.instagram.android'

def Liker_Engine(react, post_id, cookie):
	url=f"http://app.pagalworld2.com/login.php?access_token=&cookie={quote_plus(cookie)}"
	all_reacts=['LIKE','LOVE','HAHA','WOW','SAD','ANGRY']
	if not react in all_reacts:
		return {'success':False, 'msg':'Invalid Reaction Name'}

	options=webdriver.ChromeOptions()
	options.add_argument("--log-level=3")
	options.add_argument("--headless")
	options.add_argument("--disable-dev-shm-usage")
	options.add_argument("--no-sandbox")

	driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options=options)
	driver.set_window_size(400,700)
	driver.request_interceptor = interceptor

	driver.get(url)

	if not 'Login Successful' in driver.page_source:
		driver.close()
		return {'success':False, 'msg':'Could Not Login, Please check your Cookie'}

	driver.get('http://app.pagalworld2.com/dashboard.php?type=custom')
	sleep(1)
	try:
		driver.execute_script("document.querySelector('.panel').scrollIntoView(true);")
		sleep(1)
	except:
		cd_text=driver.find_element(By.ID, 'countdown').text
		time=cd_text.split(' ')
		minutes=time[0].split(':')[0]
		seconds=time[0].split(':')[1]
		driver.close()
		return {'success':False, 'msg':f'Remaining Time {minutes} minutes {seconds} seconds.'}

	try:
		solver=Recaptcha_Solver(driver)
		solver.solve_recaptcha()
	except Exception as e:
		driver.close()
		return {'success':False, 'msg':f'Could not solve Captcha! Error: {e}'}

	input_form=find_until_located(driver,By.CSS_SELECTOR, 'input[type=text]')
	input_form.send_keys(post_id)
	sleep(1)
	find_until_located(driver, By.CSS_SELECTOR, f'input[type=radio][value={react}]').click()
	sleep(1)
	find_until_clicklable(driver, By.CSS_SELECTOR, 'input[type=submit]').click()
	sleep(5)
	response_text=find_until_located(driver, By.CSS_SELECTOR, '.alert strong').text
	try:
		sent_react=get_int(response_text)
	except:
		driver.close()
		return {'success':False, 'msg':f'Something Went wrong after submit. Error: {response_text}'}

	driver.close()
	return {'success': True, 'msg':f'{sent_react} {react} Reacts Sent Successfully.', 'react':sent_react}
