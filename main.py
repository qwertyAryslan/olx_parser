import pandas as pd
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


chrome_driver = "/usr/bin/safaridriver"
df_url = pd.DataFrame(columns=['url'])
df_phone = pd.DataFrame(columns=['phone'])
df_desc = pd.DataFrame(columns=['description'])
df_user = pd.DataFrame(columns=['username'])
df_post = pd.DataFrame(columns=['postname'])
df_date = pd.DataFrame(columns=['date_of_inserting'])
df_adr = pd.DataFrame(columns=['address'])
df_views = pd.DataFrame(columns=['views'])


number_of_pages = 25
driver = webdriver.Safari()
x=1
for x in range(number_of_pages):
    
    #https://www.olx.kz/list/q-%D0%BA%D1%80%D0%B5%D0%B4%D0%B8%D1%82%D1%8B/?page=2
    driver.get('https://www.olx.kz/list/q-%D0%BA%D1%80%D0%B5%D0%B4%D0%B8%D1%82/?page={}'.format(x))
    get_all_urls = driver.find_elements_by_xpath("//h3[@class='lheight22 margintop5']//a")
    for i in get_all_urls:
        url = i.get_attribute('href')
        row1={'url':url}
        df_url=df_url.append(row1,ignore_index=True)
    x=x+1
    time.sleep(1)
df_url.drop_duplicates()


x = 0
#driver = webdriver.Safari()
for z in df_url['url'].values:
    try:
        driver.get(z)
        

        try:
            time.sleep(1)
            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'contact-button link-phone')]")))
            element.click()
            #driver.find_element_by_xpath("//div[contains(@class, 'contact-button link-phone')]").click()
            time.sleep(2)
            phone = driver.find_element_by_axpath("//div[contains(@class, 'contact-button link-phone')]//strong").text
        except (NoSuchElementException,TimeoutException):
            phone = "no phone"
        time.sleep(2)
        try:
            user_name = driver.find_element_by_xpath("//div[contains(@class, 'offer-user__actions')]//a").text
            post_name = driver.find_element_by_xpath("//div[contains(@class, 'offer-titlebox')]//h1").text
            description = driver.find_element_by_xpath("//div[contains(@class, 'clr lheight20 large')]").text
            date_of_inserting = driver.find_element_by_xpath("//li[contains(@class, 'offer-bottombar__item')]//em//strong").text
            address = driver.find_element_by_xpath("//div[contains(@class, 'offer-user__address')]//address//p").text
            view = driver.find_element_by_xpath("//li[contains(@class, 'offer-bottombar__item')]//span//strong").text
        except (NoSuchElementException,TimeoutException):
            user_name = "no info"
            post_name = "no info"
            description = "no info"
            date_of_inserting = "no info"
            address = "no info"
            view = "no info"

        row2={'phone':phone}
        df_phone=df_phone.append(row2,ignore_index=True)

        row3={'username':user_name}
        df_user=df_user.append(row3,ignore_index=True)

        row4={'postname':post_name}
        df_post=df_post.append(row4,ignore_index=True)

        row5={'description':description}
        df_desc=df_desc.append(row5,ignore_index=True)


        row7={'date_of_inserting':date_of_inserting}
        df_date=df_date.append(row7,ignore_index=True)


        row9={'views':view}
        df_views=df_views.append(row9,ignore_index=True)

        row8={'address':address}
        df_adr=df_adr.append(row8,ignore_index=True)
        time.sleep(1)
        x = x + 1
    except TimeoutException:
        print("problems")
    print(x)
    print(phone)


pdList = [df_url, df_phone, df_user, df_post, df_views, df_date, df_adr, df_desc]  # List of your dataframes
new_df = pd.concat(pdList, axis=1, sort=False)
new_df.to_excel(r'/Users/aryslanbulantayev/Desktop/krisha2.xlsx',index=False)
driver.quit()
new_df
