from selenium import webdriver #used to interface with the website
from selenium.webdriver.common.keys import Keys 
import datefinder, datetime, pause #used to extract the date from infotext and pause the script until we can enter again
from getpass import getpass #used to hide the users password in console

def raffle(usernamet, passwordt):
    op = webdriver.ChromeOptions() #set selenium to use google chrome
    op.add_argument('headless') #set selenium to headless mode (don't display the window)
    driver = webdriver.Chrome(options=op) #set the driver variable to the selenium chrome webdriver
    #Login to the site
    driver.get('https://plexguide.com/login/')
    username = driver.find_element_by_name('login')
    username.send_keys(str(usernamet))
    password = driver.find_element_by_name('password')
    password.send_keys(str(passwordt))
    password.send_keys(Keys.RETURN)
    if driver.current_url == 'https://plexguide.com/login/login':
        return 'signIn'
    #navigate to the raffle page
    driver.get('https://plexguide.com/raffles/')
    link = driver.find_element_by_xpath('/html/body/div[2]/div/div[4]/div/div/div/div/div/div/div/div/table/tbody/tr/td[1]/a')
    link.click()
    #try to enter the raffle 
    try:
        agree = driver.find_element_by_xpath('//*[@id="top"]/div[4]/div/div[2]/div/div/div/div/div/div/div[4]/table/tbody/tr/td[2]/form/ul/li/label/i')
        agree.click()
        enterRaffle = driver.find_element_by_xpath('//*[@id="top"]/div[4]/div/div[2]/div/div/div/div/div/div/div[4]/table/tbody/tr/td[2]/form/div/div/button')
        enterRaffle.click()
        print('\nEntry Successful!')
        driver.refresh()
    except:
        print('\nRaffle already entered [Skipping]')
    #get raffle info
    info = driver.find_element_by_xpath('/html/body/div[2]/div/div[4]/div/div[2]/div/div/div/div/div/div/div[4]/table/tbody/tr/td[2]')
    infotext = info.text #this variable contains how many times we entered, and when we can enter again
    #close connection
    driver.close()
    return infotext

if __name__ == "__main__":
    print('Raffle Entry Bot\n')
    #get username and password via console prompt
    username = input('Username: ')
    password = getpass()

    while True: #loop continuously
        print('\n[Running]')
        msg = raffle(username, password) #call the raffle function with the given username and password
        if str(msg) == 'signIn': #if the raffle function returns the string signIn that means we were redirected to the sign in page after entering credentials so the login has failed
            print('Credentials Failed! Exiting script...')
            break #break the loop if the login fails
        print(f'\n{msg}\n') #print the return value of the raffle function
        matches = datefinder.find_dates(msg) 
        now = datetime.datetime.now() #set a varaible to the current date and time
        nextRun = now #set the next time we can run the script to right now
        for match in matches: #extract the date from the return value
            if match > now: #if the return values date (aka. when you can enter again) is greater than the current time 
                nextRun = match + datetime.timedelta(minutes=1) #set nextRun = when you can enter again + 1 minute (we add a minute just to be safe)
        print(f'Pausing script until: {nextRun}')
        pause.until(nextRun) #pause the script until we can run again