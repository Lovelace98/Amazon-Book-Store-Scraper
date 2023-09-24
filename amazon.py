from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

options = Options()
service = Service()
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager(driver_version="116.0.5845.141").install(), options=options))


#Grabs the url to be scraped
driver.get("https://www.amazon.com/kindle-dbs/browse/ref=dbs_b_def_rwt_brws_ts_recs_pg_1?storeType=ebooks&widgetId"
           "=unified-ebooks-storefront-default_TopSellersStrategy&sourceAsin=&content-id=amzn1.sym.bb33addf-488a-4e99"
           "-909f-3acc87146400&refTagFromService=ts&title=Best+sellers+&view=GRID&pf_rd_p=bb33addf-488a-4e99-909f"
           "-3acc87146400&sourceType=recs&pf_rd_r=JAFPF423ZB1FPX3MBD04&pd_rd_wg=zfC0w&ref_"
           "=dbs_f_def_rwt_wigo_ts_recs_wigo&SkipDeviceExclusion=true&pd_rd_w=iBZTh&nodeId=154606011&pd_rd_r=16679887"
           "-9715-409f-8d5c-dd0d6552bd28&metadata=cardAppType%3ADESKTOP%24deviceTypeID%3AA2Y8LFC259B97P"
           "%24clientRequestId%3AJAFPF423ZB1FPX3MBD04%24deviceAppType%3ADESKTOP%24ipAddress%3A10.91.215.179"
           "%24browseNodes%3A154606011%24userAgent%3AMozilla%2F5.0+%28Windows+NT+10.0%3B+Win64%3B+x64%29+AppleWebKit"
           "%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F117.0.0.0+Safari%2F537.36%24cardSurfaceType%3Adesktop"
           "%24cardMobileOS%3AUnknown%24locale%3Aen_US%24deviceSurfaceType%3Adesktop&page=1")

time.sleep(5)

#These are lists containing the data scraped
title_names = []
rating_numbers = []
reviews = []
for i in range(6):

    container = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "browse-views-area")))
    # driver.find_element(By.ID, "browse-views-area")
    # sections = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="browse-grid-view'
    #                                                                                      '"]/div/div')))
    
    #This block of code gets the container housing the data we want to scrape and then loops through it
    sections = container.find_elements(By.XPATH, '//*[@id="browse-grid-view"]/div/div')
    for section in sections:
        titles = section.find_elements(By.XPATH, '//*[@id="sponsoredLabel-title"]/a/li/span/span')

    #This grabs the title names from the list of titles on the page
    for title in titles:
        title_names.append(title.text)

        ratings = section.find_elements(By.XPATH, "//span[contains(@class, 'dbs-icon-alt')]")
    
    #This block of code goes through the list of ratings for each book and then saves each of them in a list
    for rating in ratings:
        whole_rating = rating.get_attribute("innerHTML")
        only_whole_rating = whole_rating.split(",")[1]
        rating_only = int(only_whole_rating.removesuffix(" ratings"))
        rating_numbers.append(rating_only)
        only_whole_review = whole_rating.split(",")[0]
        review_only = float(only_whole_review.removesuffix(" out of 5 stars"))
        reviews.append(review_only)


    # Pagination: This block of code finds the next button if any and then clicks on it to scrape the next page
    try:
        next_button = driver.find_element(By.XPATH, '//*[@id="pagination-section"]/div/ul/li[2]/a')
        next_button.click()
        time.sleep(5)
    except:
        print("No buttons to click")

    # print(reviews)
    # print(len(reviews))
    # print(title_names)
    # print(len(title_names))
    # print(rating_numbers)
    # print(len(rating_numbers))
    
#this block of code saves the data we have scraped in a csv fie.
df_books = pd.DataFrame({'Book Title': title_names, 'Book Rating': reviews, 'Number of reviews': rating_numbers})
df_books.to_csv("amazon_data.csv", index=False)
    
ratings_above_expected = df_books[(df_books["Book Rating"] >= 4.5) & (df_books['Number of reviews'] >= 10000)]

ratings_above_expected.to_csv('books_to_read.csv', index=False)
    
# df_books.to_csv("amazon_data.csv", index=False)
