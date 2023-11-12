import multiprocessing
import asyncio
from telegram import Bot
from requests import Timeout
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from selenium.common.exceptions import StaleElementReferenceException, ElementNotInteractableException, TimeoutException
from retry import retry  # Make sure to install the 'retry' module (pip install retry)
import mysql.connector

# Replace these with your actual database connection details
db_params = {
    'host': 'database-1.c6x5n1s4dnxc.ap-south-1.rds.amazonaws.com',
    'user': 'admin',
    'password': 'barry1616',
    'database': 'projecttelegram',
}

# Connect to MySQL server
connection = mysql.connector.connect(**db_params)
cursor = connection.cursor()


async def send_telegram_message(bot_token, group_chat_id, message_text):
    bot = Bot(token=bot_token)
    await bot.send_message(chat_id=group_chat_id, text=message_text)


def is_element_present(driver, by, value, timeout=10):
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        return True
    except TimeoutException:
        return False


allimagesrcdb = []
# table_name = 'movies'
# column_name = 'image_url'
# cursor.execute(f"SELECT {column_name} FROM {table_name}")
# rows = cursor.fetchall()
# for row in rows:
#     allimagesrcdb.append(row[0])
# table_name = 'series'
# column_name = 'image_url'
# cursor.execute(f"SELECT {column_name} FROM {table_name}")
# rows = cursor.fetchall()
# for row in rows:
#     allimagesrcdb.append(row[0])
table_name = 'series'
column_name = 'image_url'
cursor.execute(f"SELECT {column_name} FROM {table_name}")
rows = cursor.fetchall()
for row in rows:
    allimagesrcdb.append(row[0])
table_name = 'movies'
column_name = 'image_url'
cursor.execute(f"SELECT {column_name} FROM {table_name}")
rows = cursor.fetchall()
for row in rows:
    allimagesrcdb.append(row[0])

cursor.close()
connection.close()


@retry((ConnectionError, Timeout), tries=10, delay=2, backoff=2)
def shorten_url(api_key, destination_url, custom_alias=None):
    try:

        base_url = "https://tnshort.net/api"
        params = {
            "api": api_key,
            "url": destination_url,
            "alias": custom_alias,
            "format": "text"  # Request response in text format
        }
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            return response.text.strip()  # Strip any leading/trailing whitespace
        else:
            return None
    except (ConnectionError, Timeout) as e:
        print(f"Error: {e}. Retrying...")
        raise e


def scraping(start_page, end_page, imagesrc, downloadlinks, allongoing, lock):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    user_agent = "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.92 Mobile Safari/537.36"
    chrome_options.add_argument(f"user-agent={user_agent}")
    referer = "https://moviesmod.vip/"
    chrome_options.add_argument('--ignore-ssl-errors=yes')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument(f"referer={referer}")

    driver = webdriver.Chrome(options=chrome_options)
    # driver.implicitly_wait(20)

    local_imagesrc = []
    local_downloadlinks = []
    local_allongoing = []

    for i in range(start_page, end_page + 1):
        formatted_url = f"https://moviesmod.shop/page/{i}"
        driver.get(formatted_url)

        div_elements = driver.find_elements(By.CLASS_NAME, "featured-thumbnail")
        counter = 0
        counterchecker = []
        for div_element in div_elements:
            mpsrc = div_element.find_element(By.TAG_NAME, "img").get_attribute("src")
            counter += 1
            if mpsrc in allimagesrcdb:
                counterchecker.append(counter)
                continue

            local_imagesrc.append(mpsrc)

        print(counterchecker)
        ml = driver.find_elements(By.CSS_SELECTOR, 'h2.title.front-view-title')
        counter = 0
        for link in ml:
            mll = link.find_elements(By.CSS_SELECTOR, 'a[href]')
            text = link.text
            for abc in mll:
                mdl = abc.get_attribute('href')
                counter += 1
                if counter in counterchecker:
                    continue
                local_downloadlinks.append(mdl)

            if 'Added]' in text:
                local_allongoing.append(mdl)
        if 'https://moviesmod.shop/download-superhero-movie-2008-comedy-movie-720p/' in local_downloadlinks:
            break

    driver.quit()

    # Acquire lock before updating shared lists
    with lock:
        imagesrc.extend(local_imagesrc)
        downloadlinks.extend(local_downloadlinks)
        allongoing.extend(local_allongoing)


if __name__ == '__main__':
    num_processes = 4

    # Specify the start and end page numbers
    start_page = 100
    end_page = 100

    imagesrc = multiprocessing.Manager().list()
    downloadlinks = multiprocessing.Manager().list()
    allongoing = multiprocessing.Manager().list()

    page_ranges = [(start_page, end_page)]

    # Create a lock for synchronizing access to shared lists
    lock = multiprocessing.Manager().Lock()

    # Create a multiprocessing pool
    pool = multiprocessing.Pool(processes=num_processes)

    # Create and start the processes
    pool.starmap(scraping, [(start, end, imagesrc, downloadlinks, allongoing, lock) for start, end in page_ranges])

    # Close the pool and wait for all processes to finish
    pool.close()
    pool.join()

    # Calculate and print the lengths of the lists
    imagesrc_length = len(imagesrc)
    downloadlinks_length = len(downloadlinks)
    allongoing_length = len(allongoing)

    print(f"Length of imagesrc list: {imagesrc_length}")
    for i in range(len(imagesrc)):
        print(imagesrc[i])
    print(f"Length of downloadlinks list: {downloadlinks_length}")
    for i in range(len(downloadlinks)):
        print(downloadlinks[i])
    print(f"Length of allongoing list: {allongoing_length}")


def process_download_link(thread_id, imagesrc, link_queue, allongoing,chrome_options):
    # Create a new WebDriver instance for each thread
    global resolution
    try:


        # Initialize Firefox WebDriver with the configured options
        driver = webdriver.Chrome(options=chrome_options)
        # driver.set_page_load_timeout(60)  # Set timeout in seconds

        # driver.implicitly_wait(16)
        while not link_queue.empty():

            ongoingseries = False
            ongoingseriesepilist = {}
            allscrapedepisodes = []
            unbrokenlink = False
            # Get the next download link from the queue

            downloadlinks = link_queue.get(block=False)
            imagesourceurl = imagesrc.get(block=False)
            if imagesourceurl in allimagesrcdb:
                continue
            if imagesourceurl not in allimagesrcdb:

                # Visit the download link
                try:
                    driver.get(downloadlinks)
                except:
                    try:
                        driver.get(downloadlinks)
                    except:
                        try:
                            driver.get(downloadlinks)
                        except:
                            continue
                checker = downloadlinks

                if checker in allongoing:
                    ongoingseries = True
                    allscrapedepisodes = []
                category = driver.find_elements(By.CSS_SELECTOR, 'div.thecategory a[href]')
                anime = False

                animecheck = []
                for cat in category:
                    cate = cat.get_attribute('href')
                    animecheck.append(cate)

                if 'https://moviesmod.shop/anime/' in animecheck:
                    anime = True

                try:
                    list_items_with_strong = driver.find_elements(By.XPATH, "//li[strong]")
                    text_items = []
                    for li in list_items_with_strong:
                        text = li.text
                        text_items.append(text)

                    result = "\n".join(text_items)

                    starti = 5
                    endi = result.index("Size")
                    movie_descrp = result[starti:endi]
                    print(movie_descrp)
                except:
                    extracted_text = []
                    movie_info = driver.find_elements(By.XPATH, '//p[strong]')
                    for info in movie_info:
                        infoo = info.text
                        extracted_text.append(infoo)
                    result = '\n'.join(extracted_text)
                    starti = result.index("Name")
                    endi = result.index("Size")
                    movie_descrp = result[starti:endi]
                    print(movie_descrp)
                series = False
                if 'Season' in result:
                    series = True
                theatreprint = 'HDCaM' in result
                if series and not anime:
                    print('series found')
                    driver.implicitly_wait(10)
                    checkzip = False
                    checkzip = is_element_present(driver, By.CSS_SELECTOR,
                                                  'a.maxbutton-24.maxbutton.maxbutton-batch-zip')
                    zipfilelinks = []
                    if checkzip:
                        zipfileb = driver.find_elements(By.CSS_SELECTOR, 'a.maxbutton-24.maxbutton.maxbutton-batch-zip')
                        zipfilecount = len(zipfileb)
                        for zipf in zipfileb:
                            zipfilel = zipf.get_attribute('href')
                            zipfilelinks.append(zipfilel)
                    zipchecker = len(zipfilelinks)
                    if zipchecker == 0:
                        continue
                    seriesdownloadlink = []
                    sdbutton = driver.find_elements(By.CSS_SELECTOR,
                                                    'a.maxbutton-23.maxbutton.maxbutton-episode-links')
                    try17 = is_element_present(driver, By.CSS_SELECTOR, 'a.maxbutton-19.maxbutton.maxbutton-g-drive')
                    if try17:
                        try19 = driver.find_elements(By.CSS_SELECTOR, 'a.maxbutton-19.maxbutton.maxbutton-g-drive')
                        for tries in try19:
                            try11 = tries.get_attribute('href')
                            seriesdownloadlink.append(try11)
                    else:
                        pass

                    for sdb in sdbutton:
                        sdbl = sdb.get_attribute('href')
                        seriesdownloadlink.append(sdbl)
                    sdbc = len(seriesdownloadlink)
                    captions = []
                    season_encountered = set()
                    allepidirectlinks = []
                    for i in range(sdbc):
                        count = 1
                        episodelist = []
                        shortlink480p = None
                        shortlink720p = None
                        shortlink1080p = None
                        shortlink720pbit = None
                        shortlink1080pbit = None
                        shortlink1080px264 = None
                        shortlink720px264 = None
                        shortlink480px264 = None
                        Season = None
                        iteration_caption = None

                        if seriesdownloadlink[i].startswith('https://moviesmod.vip/download'):
                            pass

                        else:
                            print(len(seriesdownloadlink))
                            try:
                                driver.get(seriesdownloadlink[i])
                            except:
                                print(f"error occured while getting seriesdlink :{seriesdownloadlink[i]}")
                            epidl = driver.find_elements(By.CSS_SELECTOR, 'h3[style="text-align: center;"] a[href]')
                            episodedownloadlink = []

                            for epi in epidl:
                                epid = epi.get_attribute('href')
                                if epid.startswith('https://oddfirm.com/?'):
                                    episodedownloadlink.append(epid)
                            print(len(episodedownloadlink))
                            if ongoingseries:
                                allscrapedepisodes.extend(episodedownloadlink)

                            else:
                                pass
                            for i in range(len(episodedownloadlink)):
                                try:
                                    try:
                                        driver.get(episodedownloadlink[i])
                                    except Exception as e:
                                        try:
                                            # Handle the ERR_CONNECTION_CLOSED error by refreshing the page
                                            driver.get(episodedownloadlink[i])
                                            print("Page refreshed due to ERR_CONNECTION_CLOSED error. in episodedlink")
                                        except:
                                            continue
                                    # time.sleep(1)
                                    wait = WebDriverWait(driver, 30)  # Set a timeout of 10 seconds

                                    timer = wait.until(EC.presence_of_element_located((By.ID, 'timer')))
                                    # timer=driver.find_element(By.CSS_SELECTOR,"#timer")
                                    if timer:
                                        driver.execute_script("document.getElementById('landing').submit();")
                                        wait = WebDriverWait(driver, 10)  # Set a timeout of 10 seconds

                                        element = wait.until(EC.presence_of_element_located((By.ID, 'verify_button2')))
                                        if element:
                                            driver.execute_script("""var ubPopupContent = document.querySelector(".ub-popupcontent");
                                                                    if (ubPopupContent) {
                                                                        ubPopupContent.style.display = "none";
                                                                    }
                                                                    var button2 = document.getElementById("verify_button2");
                                                                    button2.style.visibility = "visible";
                                                                    button2.dispatchEvent(new Event("click"));
                                                                    var button3 = document.getElementById("verify_button");
                                                                    button3.style.visibility = "visible";

                                                                    button3.dispatchEvent(new Event("click"));

                                                                    var button4 = document.getElementById("two_steps_btn");
                                                                    button4.style.display = "block";
                                                                    """)

                                        wait = WebDriverWait(driver, 10)  # Set a timeout of 10 seconds

                                        element2 = wait.until(
                                            EC.presence_of_element_located((By.LINK_TEXT, 'GO TO DOWNLOAD')))
                                        if element2:
                                            driver.execute_script("""var button4 = document.getElementById("two_steps_btn");
                                                                            button4.click()""")


                                except Exception as e:
                                    try:
                                        try:
                                            driver.get(episodedownloadlink[i])
                                        except Exception as e:

                                            # Handle the ERR_CONNECTION_CLOSED error by refreshing the page
                                            driver.get(episodedownloadlink[i])
                                            print("Page refreshed due to ERR_CONNECTION_CLOSED error. in episodedlink")

                                        # time.sleep(1)
                                        wait = WebDriverWait(driver, 30)  # Set a timeout of 10 seconds

                                        timer = wait.until(EC.presence_of_element_located((By.ID, 'timer')))
                                        # timer=driver.find_element(By.CSS_SELECTOR,"#timer")
                                        if timer:
                                            driver.execute_script("""document.getElementById('landing').submit();""")
                                            wait = WebDriverWait(driver, 10)  # Set a timeout of 10 seconds

                                            element = wait.until(
                                                EC.presence_of_element_located((By.ID, 'verify_button2')))
                                            if element:
                                                driver.execute_script("""var ubPopupContent = document.querySelector(".ub-popupcontent");
                                                                        if (ubPopupContent) {
                                                                            ubPopupContent.style.display = "none";
                                                                        }
                                                                        var button2 = document.getElementById("verify_button2");
                                                                        button2.style.visibility = "visible";
                                                                        button2.dispatchEvent(new Event("click"));
                                                                        var button3 = document.getElementById("verify_button");
                                                                        button3.style.visibility = "visible";

                                                                        button3.dispatchEvent(new Event("click"));

                                                                        var button4 = document.getElementById("two_steps_btn");
                                                                        button4.style.display = "block";
                                                                        """)

                                            wait = WebDriverWait(driver, 10)  # Set a timeout of 10 seconds

                                            element2 = wait.until(
                                                EC.presence_of_element_located((By.LINK_TEXT, 'GO TO DOWNLOAD')))
                                            if element2:
                                                driver.execute_script("""var button4 = document.getElementById("two_steps_btn");
                                                                                button4.click()""")
                                    except Exception as e:
                                        print(f'error occured while getting episodedlink : {episodedownloadlink[i]}')
                                        print(f'Error details: {str(e)}')

                                        driver.save_screenshot(f"error-episode-screenshot{count}.png")
                                        count += 1
                                        continue
                                # try:

                                window_handles = driver.window_handles

                                if len(window_handles) == 2:
                                    driver.switch_to.window(driver.window_handles[0])
                                    driver.close()
                                    # time.sleep(2)
                                    driver.switch_to.window(driver.window_handles[0])
                                try:
                                    try16 = is_element_present(driver, By.CSS_SELECTOR, 'a.navbar-brand')
                                except:
                                    try:
                                        try16 = is_element_present(driver, By.CSS_SELECTOR, 'a.navbar-brand')
                                    except:

                                        if driver.current_url.startswith('https://driveseed.org/file/'):
                                            try16 = True
                                        else:
                                            print(
                                                f"could make sure if this is the final downloadlink : {driver.current_url}")
                                            continue
                                if try16:
                                    c_url = driver.current_url
                                    print(c_url)

                                    if c_url == 'https://driveseed.org/404':
                                        continue

                                    elif driver.current_url.startswith('https://driveseed.org/file/'):
                                        allepidirectlinks.append(c_url)
                                        resolution=None
                                        unbrokenlink = True
                                        try:
                                            name_li_element = driver.find_element(By.CSS_SELECTOR, "li.list-group-item")
                                            name_li_text = name_li_element.text.lower()
                                        except Exception as e:
                                            driver.refresh()
                                            name_li_element = driver.find_element(By.CSS_SELECTOR, "li.list-group-item")
                                            name_li_text = name_li_element.text.lower()
                                            print(name_li_text)
                                        if '720p 10bit' in name_li_text or '720p.10bit' in name_li_text or '720p.bluray.10bit' in name_li_text or '720.10bit' in name_li_text:
                                            resolution = '720pbit'

                                        elif '1080p 10bit' in name_li_text or '1080p.10bit' in name_li_text or '1080p.bluray.10bit' in name_li_text or '1080.10bit' in name_li_text:
                                            resolution = '1080pbit'
                                        elif '480p.x264' in name_li_text or '480.x264' in name_li_text:
                                            resolution = '480px264'

                                        elif '720p.x264' in name_li_text or '720.x264' in name_li_text:
                                            resolution = '720px264'
                                        elif '1080p.x264' in name_li_text or '1080.x264' in name_li_text:
                                            resolution = '1080px264'
                                        elif '480p' in name_li_text or '480' in name_li_text:
                                            resolution = '480p'

                                        elif '720p' in name_li_text or '720' in name_li_text:
                                            resolution = '720p'

                                        elif '1080p' in name_li_text or '1080' in name_li_text:
                                            resolution = '1080p'

                                        else:
                                            pass
                                        try:
                                            api_key = "18ea1c83b795f1f3809ac4c3faad54670542d275"
                                            destination_url = c_url
                                            scopy = None
                                            try:
                                                scopy = shorten_url(api_key, destination_url)
                                            except:
                                                try:
                                                    scopy = shorten_url(api_key, destination_url)
                                                except:
                                                    try:
                                                        scopy = shorten_url(api_key, destination_url)
                                                    except:
                                                        print(f"======>something wrong with the scopy link : {c_url}")
                                            print(scopy)

                                            if resolution == '480p':
                                                shortlink480p = scopy
                                            elif resolution == '720p':
                                                shortlink720p = scopy
                                            elif resolution == '1080p':
                                                shortlink1080p = scopy
                                            elif resolution == '720pbit':
                                                shortlink720pbit = scopy
                                            elif resolution == '1080pbit':
                                                shortlink1080pbit = scopy
                                            elif resolution == '1080px264':
                                                shortlink1080px264 = scopy
                                            elif resolution == '720px264':
                                                shortlink720px264 = scopy
                                            elif resolution == '480px264':
                                                shortlink480px264 = scopy
                                            season_mapping = {
                                                's01': '1',
                                                's02': '2',
                                                's03': '3',
                                                's04': '4',
                                                's05': '5',
                                                's06': '6',
                                                's07': '7',
                                                's08': '8',
                                                's09': '9',
                                                's10': '10',
                                                's11': '11',
                                                's12': '12',
                                                's13': '13',
                                                's14': '14',
                                                's15': '15',
                                                's16': '16',
                                                's17': '17',
                                                's18': '18',
                                                's19': '19',
                                                's20': '20',
                                                's21': '21',
                                                's22': '22',
                                                's23': '23',
                                                's24': '24',
                                                's25': '25',
                                                's26': '26',
                                                's27': '27',
                                                's28': '28',
                                                's29': '29',
                                                's30': '30',
                                                's31': '31',
                                                's32': '32',
                                                's33': '33',
                                                's34': '34'
                                            }
                                            episode_mapping = {
                                                'e01': '1',
                                                'e02': '2',
                                                'e03': '3',
                                                'e04': '4',
                                                'e05': '5',
                                                'e06': '6',
                                                'e07': '7',
                                                'e08': '8',
                                                'e09': '9',
                                                'e10': '10',
                                                'e11': '11',
                                                'e12': '12',
                                                'e13': '13',
                                                'e14': '14',
                                                'e15': '15',
                                                'e16': '16',
                                                'e17': '17',
                                                'e18': '18',
                                                'e19': '19',
                                                'e20': '20',
                                                'e21': '21',
                                                'e22': '22',
                                                'e23': '23',
                                                'e24': '24',
                                                'e25': '25',
                                                'e26': '26',
                                                'e27': '27',
                                                'e28': '28',
                                                'e29': '29',
                                                'e30': '30',
                                                'e31': '31',
                                                'e32': '32',
                                                'e33': '33',
                                                'e34': '34'
                                            }
                                            iteration_caption = ""

                                            for identifier, value in season_mapping.items():
                                                if identifier in name_li_text:
                                                    Season = value
                                                    if Season not in season_encountered:
                                                        season_encountered.add(Season)
                                                        if iteration_caption:
                                                            # Add newline between seasons
                                                            pass
                                                        iteration_caption += f'\n★★★★★★★★★★★★★★\nSeason {Season}'

                                            if shortlink480p:
                                                episodelist.append(shortlink480p)

                                                if len(episodedownloadlink) == len(episodelist):
                                                    iteration_caption += '\n480p'
                                                    fulllist = len(episodelist)
                                                    for i in range(fulllist):
                                                        iteration_caption += f"\nEpisode {i + 1} - " + episodelist[
                                                            i]


                                            elif shortlink720p:

                                                episodelist.append(shortlink720p)
                                                if len(episodedownloadlink) == len(episodelist):
                                                    iteration_caption += '\n720p'
                                                    fulllist = len(episodelist)
                                                    for i in range(fulllist):
                                                        iteration_caption += f"\nEpisode {i + 1} - " + episodelist[
                                                            i]
                                            elif shortlink1080p:

                                                episodelist.append(shortlink1080p)
                                                if len(episodedownloadlink) == len(episodelist):
                                                    iteration_caption += '\n1080p'
                                                    fulllist = len(episodelist)
                                                    for i in range(fulllist):
                                                        iteration_caption += f"\nEpisode {i + 1} - " + episodelist[
                                                            i]
                                            elif shortlink480px264:

                                                episodelist.append(shortlink480px264)
                                                if len(episodedownloadlink) == len(episodelist):
                                                    iteration_caption += '\n480p x264'
                                                    fulllist = len(episodelist)
                                                    for i in range(fulllist):
                                                        iteration_caption += f"\nEpisode {i + 1} - " + episodelist[
                                                            i]
                                            elif shortlink720px264:

                                                episodelist.append(shortlink720px264)
                                                if len(episodedownloadlink) == len(episodelist):
                                                    iteration_caption += '\n720p x264'
                                                    fulllist = len(episodelist)
                                                    for i in range(fulllist):
                                                        iteration_caption += f"\nEpisode {i + 1} - " + episodelist[
                                                            i]
                                            elif shortlink1080px264:

                                                episodelist.append(shortlink1080px264)
                                                if len(episodedownloadlink) == len(episodelist):
                                                    iteration_caption += '\n1080p x264'
                                                    fulllist = len(episodelist)
                                                    for i in range(fulllist):
                                                        iteration_caption += f"\nEpisode {i + 1} - " + episodelist[
                                                            i]

                                            elif shortlink720pbit:

                                                episodelist.append(shortlink720pbit)
                                                if len(episodedownloadlink) == len(episodelist):
                                                    iteration_caption += '\n720p 10Bit'
                                                    fulllist = len(episodelist)
                                                    for i in range(fulllist):
                                                        iteration_caption += f"\nEpisode {i + 1} - " + episodelist[
                                                            i]
                                            elif shortlink1080pbit:

                                                episodelist.append(shortlink1080pbit)
                                                if len(episodedownloadlink) == len(episodelist):
                                                    iteration_caption += '\n1080p 10Bit'
                                                    fulllist = len(episodelist)
                                                    for i in range(fulllist):
                                                        iteration_caption += f"\nEpisode {i + 1} - " + episodelist[
                                                            i]
                                            if Season:
                                                captions.append(iteration_caption)


                                        except Exception as e:
                                            print('error 1')
                                            print(f'Error details: {str(e)}')
                                        finally:
                                            pass

                                    pass

                                    # # except Exception as e:
                                    # #     print('error 2')
                                    # #     print(f'Error details: {str(e)}')
                                    # # finally:
                                    #     pass

                                    # except Exception as e:
                                    #     print('error 3')
                                    #     print(f'Error details: {str(e)}')
                                    # finally:
                                    #     pass

                    if ongoingseries:
                        ongoingseriesepilist[checker] = [allscrapedepisodes]
                    else:
                        pass
                    if unbrokenlink:
                        print(movie_descrp)
                        # print(imagesourceurl)

                        allsdirectlinks = '\n'.join(allepidirectlinks)
                        if allsdirectlinks:
                            print(f"all episode dirextlinks : {allsdirectlinks}")
                        final_captions = ''.join(captions)
                        print(final_captions)
                        db_params = {
                            'host': 'database-1.c6x5n1s4dnxc.ap-south-1.rds.amazonaws.com',
                            'user': 'admin',
                            'password': 'barry1616',
                            'database': 'projecttelegram',
                        }

                        # Connect to MySQL server
                        connection = mysql.connector.connect(**db_params)
                        cursor = connection.cursor()

                        cursor.execute(
                            'INSERT INTO series (image_url,movie_descrp,links,org_links) VALUES(%s, %s,%s,%s)',
                            (imagesourceurl, movie_descrp, final_captions, allsdirectlinks))
                        connection.commit()
                        if ongoingseries:
                            for key, nested_values in ongoingseriesepilist.items():
                                nested_values_str = ', '.join([', '.join(values) for values in nested_values])
                                cursor.execute('INSERT INTO ongoing (serieslink, episodelinks) VALUES (%s, %s)',
                                               (key, nested_values_str))
                            connection.commit()
                        connection.close()

                    if checkzip:

                        print('checking for zip files')
                        captions = []
                        season_encountered = set()
                        allzipdirectlinks = []

                        for i in range(zipfilecount):
                            shortlink480p = None
                            shortlink720p = None
                            shortlink1080p = None
                            shortlink720pbit = None
                            shortlink1080pbit = None
                            shortlink1080px264 = None
                            shortlink720px264 = None
                            shortlink480px264 = None
                            Season = None
                            iteration_caption = None
                            if zipfilelinks[i].startswith('https://moviesmod.vip/download'):
                                pass
                            else:
                                try:
                                    driver.get(zipfilelinks[i])
                                except:
                                    try:
                                        driver.get(zipfilelinks[i])
                                    except:
                                        continue

                            try:
                                try1 = is_element_present(driver, By.CSS_SELECTOR,
                                                          'a.maxbutton-1.maxbutton.maxbutton-fast-server-gdrive')
                                if try1:
                                    fds = driver.find_element(By.CSS_SELECTOR,
                                                              'a.maxbutton-1.maxbutton.maxbutton-fast-server-gdrive')
                                else:
                                    fds = driver.find_element(By.CSS_SELECTOR,
                                                              'a.maxbutton-1.maxbutton.maxbutton-fast-server-gdrive')

                            except:
                                try:
                                    fds = driver.find_element(By.CSS_SELECTOR,
                                                              'a.maxbutton-3.maxbutton.maxbutton-fast-server-gdrive')
                                except:
                                    print(f"could find zipfile links: {downloadlinks}")
                                    continue
                            fdsl = fds.get_attribute('href')
                            print(fdsl)
                            try:
                                driver.get(fdsl)
                            except Exception as e:
                                if "ERR_CONNECTION_CLOSED" in str(e):
                                    # Handle the ERR_CONNECTION_CLOSED error by refreshing the page
                                    driver.get(fdsl)
                                    print("Page refreshed due to ERR_CONNECTION_CLOSED error.in fdsl")

                            try:
                                try:
                                    driver.execute_script("""document.getElementById('landing').submit();""")
                                    wait = WebDriverWait(driver, 10)  # Set a timeout of 10 seconds

                                    element = wait.until(EC.presence_of_element_located((By.ID, 'verify_button2')))
                                    if element:
                                        driver.execute_script("""var ubPopupContent = document.querySelector(".ub-popupcontent");
                                    if (ubPopupContent) {
                                        ubPopupContent.style.display = "none";
                                    }
                                    var button2 = document.getElementById("verify_button2");
                                    button2.style.visibility = "visible";
                                    button2.dispatchEvent(new Event("click"));
                                    var button3 = document.getElementById("verify_button");
                                    button3.style.visibility = "visible";

                                    button3.dispatchEvent(new Event("click"));

                                    var button4 = document.getElementById("two_steps_btn");
                                    button4.style.display = "block";
                                    """)

                                    wait = WebDriverWait(driver, 10)  # Set a timeout of 10 seconds

                                    element2 = wait.until(
                                        EC.presence_of_element_located((By.LINK_TEXT, 'GO TO DOWNLOAD')))
                                    if element2:
                                        driver.execute_script("""var button4 = document.getElementById("two_steps_btn");
                                            button4.click()""")
                                except:
                                    pass
                            except:
                                pass
                            window_handles = driver.window_handles

                            if len(window_handles) == 2:
                                driver.switch_to.window(driver.window_handles[0])
                                driver.close()
                                # time.sleep(2)
                                driver.switch_to.window(driver.window_handles[0])
                            try:
                                try16 = is_element_present(driver, By.CSS_SELECTOR, 'a.navbar-brand')
                            except:
                                try:
                                    try16 = is_element_present(driver, By.CSS_SELECTOR, 'a.navbar-brand')
                                except:

                                    if driver.current_url.startswith('https://driveseed.org/file/'):
                                        try16 = True
                                    else:
                                        print(
                                            f"could make sure if this is the final downloadlink : {driver.current_url}")
                                        continue
                            if try16:
                                c_url = driver.current_url

                                # Get the redirected URL

                                print(c_url)
                                if c_url == 'https://driveseed.org/404':
                                    continue
                                elif c_url.startswith('https://driveseed.org/file/'):
                                    allzipdirectlinks.append(c_url)
                                    seasoncounter = None
                                    unbrokenlink = True
                                    try:
                                        name_li_element = driver.find_element(By.CSS_SELECTOR, "li.list-group-item")
                                        name_li_text = name_li_element.text.lower()
                                    except Exception as e:
                                        driver.refresh()
                                        name_li_element = driver.find_element(By.CSS_SELECTOR, "li.list-group-item")
                                        name_li_text = name_li_element.text.lower()
                                        print(name_li_text)
                                    if '720p 10bit' in name_li_text or '720p.10bit' in name_li_text or '720p.bluray.10bit' in name_li_text or '720.10bit' in name_li_text:
                                        resolution = '720pbit'

                                    elif '1080p 10bit' in name_li_text or '1080p.10bit' in name_li_text or '1080p.bluray.10bit' in name_li_text or '1080.10bit' in name_li_text:
                                        resolution = '1080pbit'
                                    elif '480p.x264' in name_li_text or '480.x264' in name_li_text:
                                        resolution = '480px264'

                                    elif '720p.x264' in name_li_text or '720.x264' in name_li_text:
                                        resolution = '720px264'
                                    elif '1080p.x264' in name_li_text or '1080.x264' in name_li_text:
                                        resolution = '1080px264'
                                    elif '480p' in name_li_text or '480' in name_li_text:
                                        resolution = '480p'

                                    elif '720p' in name_li_text or '720' in name_li_text:
                                        resolution = '720p'

                                    elif '1080p' in name_li_text or '1080' in name_li_text:
                                        resolution = '1080p'

                                    else:
                                        pass

                                    api_key = "18ea1c83b795f1f3809ac4c3faad54670542d275"
                                    destination_url = c_url
                                    try:
                                        scopy = shorten_url(api_key, destination_url)
                                    except:
                                        try:
                                            scopy = shorten_url(api_key, destination_url)
                                        except:
                                            print(f"======>something wrong with the scopy link : {c_url}")
                                    print(scopy)
                                    if resolution == '480p':
                                        shortlink480p = scopy
                                    elif resolution == '720p':
                                        shortlink720p = scopy
                                    elif resolution == '1080p':
                                        shortlink1080p = scopy
                                    elif resolution == '720pbit':
                                        shortlink720pbit = scopy
                                    elif resolution == '1080pbit':
                                        shortlink1080pbit = scopy
                                    elif resolution == '1080px264':
                                        shortlink1080px264 = scopy
                                    elif resolution == '720px264':
                                        shortlink720px264 = scopy
                                    elif resolution == '480px264':
                                        shortlink480px264 = scopy

                                    season_mapping = {
                                        's01': '1',
                                        's02': '2',
                                        's03': '3',
                                        's04': '4',
                                        's05': '5',
                                        's06': '6',
                                        's07': '7',
                                        's08': '8',
                                        's09': '9',
                                        's10': '10',
                                        's11': '11',
                                        's12': '12',
                                        's13': '13',
                                        's14': '14',
                                        's15': '15',
                                        's16': '16',
                                        's17': '17',
                                        's18': '18',
                                        's19': '19',
                                        's20': '20',
                                        's21': '21',
                                        's22': '22',
                                        's23': '23',
                                        's24': '24',
                                        's25': '25',
                                        's26': '26',
                                        's27': '27',
                                        's28': '28',
                                        's29': '29',
                                        's30': '30',
                                        's31': '31',
                                        's32': '32',
                                        's33': '33',
                                        's34': '34'
                                    }

                                    iteration_caption = ""

                                    for identifier, value in season_mapping.items():
                                        if identifier in name_li_text:
                                            Season = value
                                            if Season not in season_encountered:
                                                season_encountered.add(Season)
                                                if iteration_caption:
                                                    # Add newline between seasons
                                                    pass
                                                iteration_caption += f'\n★★★★★★★★★★★★★★\nSeason {Season}'
                                                seasoncounter = int(Season)
                                            break
                                    # if "★★★★★★★★★★★★★★" not in iteration_caption:
                                    #     if seasoncounter==None:
                                    #         seasoncounter=0
                                    #
                                    #     driver.save_screenshot(f"{c_url}.png")
                                    #     print(f"season no not found :{name_li_text} - {c_url}")
                                    #     if f"\n★★★★★★★★★★★★★★\nSeason {seasoncounter+1}" in captions:
                                    #         pass
                                    #     elif f"\n★★★★★★★★★★★★★★\nSeason {seasoncounter+1}" not in captions:
                                    #         iteration_caption += f'\n★★★★★★★★★★★★★★\nSeason {seasoncounter+1}'
                                    # seasoncounter+=1
                                    # Define a dictionary for the season mappings
                                    if shortlink480p:
                                        iteration_caption += '\n' + '480p - ' + shortlink480p
                                    elif shortlink720p:
                                        iteration_caption += '\n' + '720p - ' + shortlink720p
                                    elif shortlink1080p:
                                        iteration_caption += '\n' + '1080p - ' + shortlink1080p
                                    elif shortlink480px264:
                                        iteration_caption += '\n' + '480p x264 - ' + shortlink480px264
                                    elif shortlink720px264:
                                        iteration_caption += '\n' + '720p x264 - ' + shortlink720px264
                                    elif shortlink1080px264:
                                        iteration_caption += '\n' + '1080p x264 - ' + shortlink1080px264
                                    elif shortlink720pbit:
                                        iteration_caption += '\n' + '720p 10Bit - ' + shortlink720pbit
                                    elif shortlink1080pbit:
                                        iteration_caption += '\n' + '1080p 10Bit - ' + shortlink1080pbit

                                    # ... Your existing code ...

                                    # Append the iteration's caption to the list
                                    if Season:
                                        captions.append(iteration_caption)

                                # poster = imagesrc[movieorseriesindex]

                                # finally:
                                #     pass
                        if unbrokenlink:
                            final_captions = ''.join(captions)
                            fullcaption = ''
                            fullcaption += movie_descrp
                            fullcaption += final_captions
                            fullcaption += "\n@projectorparadise"
                            print(fullcaption)
                            allzdirectlinks = '\n'.join(allzipdirectlinks)
                            if allzdirectlinks:
                                print(f"all zip file links : {allzdirectlinks}")
                            db_params = {
                                'host': 'database-1.c6x5n1s4dnxc.ap-south-1.rds.amazonaws.com',
                                'user': 'admin',
                                'password': 'barry1616',
                                'database': 'projecttelegram',
                            }

                            # Connect to MySQL server
                            if "★★★★★★★★★★★★★★" not in fullcaption:
                                bot_token = '6407514901:AAHU4wk67IGgKQIUslHGiMotggWZmwKFf90'
                                group_chat_id = '@barryallen16projectgroup'
                                text = f"no season mentioned : {allzdirectlinks}"
                                loop = asyncio.get_event_loop()
                                loop.run_until_complete(send_telegram_message(bot_token, group_chat_id, text))

                            connection = mysql.connector.connect(**db_params)
                            cursor = connection.cursor()

                            cursor.execute('INSERT INTO zip (image_url,links,org_links) VALUES(%s, %s,%s)',
                                           (imagesourceurl, fullcaption, allzdirectlinks))
                            connection.commit()
                            connection.close()

                elif not series and not anime:
                    downloadbutton = driver.find_elements(By.CSS_SELECTOR,
                                                          'a.maxbutton-1.maxbutton.maxbutton-download-links[href]')
                    if not theatreprint:
                        driver.implicitly_wait(10)
                        cdb = len(downloadbutton)
                        brokenlinkcount = 0
                        buttonlinks = []
                        for button in downloadbutton:
                            blinks = button.get_attribute('href')
                            buttonlinks.append(blinks)
                        shortlink480p = None
                        shortlink720p = None
                        shortlink1080p = None
                        shortlink720pbit = None
                        shortlink1080pbit = None
                        shortlink1080px264 = None
                        shortlink720px264 = None
                        shortlink480px264 = None
                        allmoviedirectlinks = []

                        for i in range(cdb):

                            if buttonlinks[i].startswith('https://moviesmod.vip/download'):
                                pass
                            if is_element_present(driver, By.CSS_SELECTOR,
                                                  'a.maxbutton-1.maxbutton.maxbutton-download-links.custom-linethrough'):

                                continue

                            else:
                                print(buttonlinks[i])
                                try:
                                    driver.get(buttonlinks[i])
                                except:
                                    try:
                                        driver.get(buttonlinks[i])
                                    except:
                                        continue
                            try1 = is_element_present(driver, By.CSS_SELECTOR,
                                                      'a.maxbutton-2.maxbutton.maxbutton-google-drive-server-2')

                            if try1:
                                gddl = driver.find_element(By.CSS_SELECTOR,
                                                           'a.maxbutton-2.maxbutton.maxbutton-google-drive-server-2')

                            elif not try1:
                                try2 = is_element_present(driver, By.CSS_SELECTOR,
                                                          'a.maxbutton-2.maxbutton.maxbutton-gdrive-links-login')

                                if try2:
                                    gddl = driver.find_element(By.CSS_SELECTOR,
                                                               'a.maxbutton-2.maxbutton.maxbutton-gdrive-links-login')
                            try:
                                gddlh = gddl.get_attribute('href')
                            except:
                                print(f'++++++++gddl not present checking the website manually : {buttonlinks[i]}')
                                continue
                            print(cdb)

                            print(gddlh)

                            try:
                                driver.get(gddlh)
                            except Exception as e:
                                if "ERR_CONNECTION_CLOSED" in str(e):
                                    # Handle the ERR_CONNECTION_CLOSED error by refreshing the page
                                    driver.get(gddlh)
                                    print("Page refreshed due to ERR_CONNECTION_CLOSED error.in gddlh")

                            # try:
                            try:
                                driver.execute_script("""document.getElementById('landing').submit();""")
                                wait = WebDriverWait(driver, 10)  # Set a timeout of 10 seconds

                                element = wait.until(EC.presence_of_element_located((By.ID, 'verify_button2')))
                                if element:
                                    driver.execute_script("""var ubPopupContent = document.querySelector(".ub-popupcontent");
        if (ubPopupContent) {
            ubPopupContent.style.display = "none";
        }
        var button2 = document.getElementById("verify_button2");
        button2.style.visibility = "visible";
        button2.dispatchEvent(new Event("click"));
        var button3 = document.getElementById("verify_button");
        button3.style.visibility = "visible";

        button3.dispatchEvent(new Event("click"));

        var button4 = document.getElementById("two_steps_btn");
        button4.style.display = "block";
        """)

                                wait = WebDriverWait(driver, 10)  # Set a timeout of 10 seconds

                                element2 = wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'GO TO DOWNLOAD')))
                                if element2:
                                    driver.execute_script("""var button4 = document.getElementById("two_steps_btn");
                                        button4.click()""")
                            except:
                                pass
                            window_handles = driver.window_handles

                            if len(window_handles) == 2:
                                driver.switch_to.window(driver.window_handles[0])
                                driver.close()
                                # time.sleep(2)
                                driver.switch_to.window(driver.window_handles[0])
                            try:
                                try16 = is_element_present(driver, By.CSS_SELECTOR, 'a.navbar-brand')
                            except:
                                try:
                                    try16 = is_element_present(driver, By.CSS_SELECTOR, 'a.navbar-brand')
                                except:

                                    if driver.current_url.startswith('https://driveseed.org/file/'):
                                        try16 = True
                                    else:
                                        print(
                                            f"could make sure if this is the final downloadlink : {driver.current_url}")
                                        continue
                            if try16:
                                c_url = driver.current_url
                                print(c_url)
                                if c_url == 'https://driveseed.org/404':
                                    continue

                                elif c_url.startswith('https://driveseed.org/file/'):
                                    allmoviedirectlinks.append(c_url)
                                    unbrokenlink = True
                                    try:
                                        name_li_element = driver.find_element(By.CSS_SELECTOR, "li.list-group-item")
                                        name_li_text = name_li_element.text.lower()
                                    except Exception as e:
                                        driver.refresh()
                                        name_li_element = driver.find_element(By.CSS_SELECTOR, "li.list-group-item")
                                        name_li_text = name_li_element.text.lower()
                                        print(name_li_text)
                                    if '720p 10bit' in name_li_text or '720p.10bit' in name_li_text or '720p.bluray.10bit' in name_li_text or '720.10bit' in name_li_text:
                                        resolution = '720pbit'

                                    elif '1080p 10bit' in name_li_text or '1080p.10bit' in name_li_text or '1080p.bluray.10bit' in name_li_text or '1080.10bit' in name_li_text:
                                        resolution = '1080pbit'
                                    elif '480p.x264' in name_li_text or '480.x264' in name_li_text:
                                        resolution = '480px264'

                                    elif '720p.x264' in name_li_text or '720.x264' in name_li_text:
                                        resolution = '720px264'
                                    elif '1080p.x264' in name_li_text or '1080.x264' in name_li_text:
                                        resolution = '1080px264'
                                    elif '480p' in name_li_text or '480' in name_li_text:
                                        resolution = '480p'

                                    elif '720p' in name_li_text or '720' in name_li_text:
                                        resolution = '720p'

                                    elif '1080p' in name_li_text or '1080' in name_li_text:
                                        resolution = '1080p'

                                    else:
                                        pass
                                    try:
                                        api_key = "18ea1c83b795f1f3809ac4c3faad54670542d275"
                                        destination_url = c_url
                                        scopy = None
                                        try:
                                            scopy = shorten_url(api_key, destination_url)
                                        except:
                                            try:
                                                scopy = shorten_url(api_key, destination_url)
                                            except:
                                                print(f"======>something wrong with the scopy link : {c_url}")
                                        print(scopy)

                                        if resolution == '480p':
                                            shortlink480p = scopy
                                        elif resolution == '720p':
                                            shortlink720p = scopy
                                        elif resolution == '1080p':
                                            shortlink1080p = scopy
                                        elif resolution == '720pbit':
                                            shortlink720pbit = scopy
                                        elif resolution == '1080pbit':
                                            shortlink1080pbit = scopy
                                        elif resolution == '1080px264':
                                            shortlink1080px264 = scopy
                                        elif resolution == '720px264':
                                            shortlink720px264 = scopy
                                        elif resolution == '480px264':
                                            shortlink480px264 = scopy



                                    except Exception as e:
                                        print('error 1')
                                        print(f'Error details: {str(e)}')

                                    finally:
                                        pass

                            # except Exception as e:
                            #     print('error 3')
                            #     print(f'Error details: {str(e)}')
                            # finally:
                            #     pass
                        if unbrokenlink:
                            captions = []
                            caption3 = ""
                            allmdirectlinks = '\n'.join(allmoviedirectlinks)
                            if allmdirectlinks:
                                print(allmdirectlinks)
                            resolution_links = {
                                '480p': shortlink480p,
                                '720p': shortlink720p,
                                '1080p': shortlink1080p,
                                '480p x264': shortlink480px264,
                                '720p x264': shortlink720px264,
                                '1080p x264': shortlink1080px264,
                                '720p 10Bit': shortlink720pbit,
                                '1080p 10Bit': shortlink1080pbit
                            }

                            for resolution, link in resolution_links.items():
                                if link:
                                    caption3 += f'\n{resolution} - {link}'

                            # After adding the shortlinks, create the final caption
                            final_caption = movie_descrp + '\n★★★★★★★★★★★★★★' + caption3 + '\n@projectorparadise'

                            # Append the final caption to the captions list
                            captions.append(final_caption)

                            # Join the captions and print them
                            all_captions = '\n'.join(captions)
                            db_params = {
                                'host': 'database-1.c6x5n1s4dnxc.ap-south-1.rds.amazonaws.com',
                                'user': 'admin',
                                'password': 'barry1616',
                                'database': 'projecttelegram',
                            }

                            # Connect to MySQL server
                            try:
                                connection = mysql.connector.connect(**db_params)
                                cursor = connection.cursor()
                            except:
                                try:
                                    connection = mysql.connector.connect(**db_params)
                                    cursor = connection.cursor()
                                except:
                                    continue
                            cursor.execute('INSERT INTO movies (image_url,caption,org_links) VALUES(%s, %s,%s)',
                                           (imagesourceurl, all_captions, allmdirectlinks))
                            connection.commit()
                            connection.close()
    except TimeoutException:
        pass
    except Exception as e:
        error_message = str(e)
        bot_token = '6407514901:AAHU4wk67IGgKQIUslHGiMotggWZmwKFf90'
        group_chat_id = '@barryallen16projectgroup'

        loop = asyncio.get_event_loop()
        loop.run_until_complete(send_telegram_message(bot_token, group_chat_id, error_message))
    finally:
        try:
            driver.quit()
        except:
            pass

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
user_agent = "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.92 Mobile Safari/537.36"
chrome_options.add_argument(f"user-agent={user_agent}")
referer = "https://moviesmod.shop/"
chrome_options.add_argument('--disable-gpu')  # Required in some cases for headless mode
chrome_options.add_argument('--disable-infobars')
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--enable-javascript")
chrome_options.add_argument('--disable-features=VizDisplayCompositor')
# chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
# chrome_options.add_argument('--disable-logging')
chrome_options.add_argument('--pageLoadStrategy=normal')
# chrome_options.add_argument("--auto-open-devtools-for-tabs")
# chrome_options.add_argument("--host-resolver-rules=MAP * 127.0.0.1")
# chrome_options.add_argument("--proxy-server='direct://'")
# chrome_options.add_argument("--proxy-bypass-list=*")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--headless")  # Optional, for headless mode
#
# # Enable caching for Chrome
# chrome_options.add_argument("--disk-cache-dir=/tmp/cache")
# chrome_options.add_argument("--disk-cache-size=10485760")
#
# chrome_options.add_argument('--ignore-ssl-errors=yes')
# chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument(f"referer={referer}")
# Your list of download links
if __name__ == '__main__':
    # Create a queue for link distribution
    link_queue = multiprocessing.Queue()
    # copy_downloadlinks=downloadlinks
    # lengthdlinks=len(copy_downloadlinks)//2
    # print(f"divided portion of dlinks is {lengthdlinks} from {len(copy_downloadlinks)}")
    # downloadlinks=downloadlinks[:8]
    # dlength=len(downloadlinks)
    # print(f"length of download links after dividing {dlength}")
    for link in downloadlinks:
        link_queue.put(link)

    imagesrc_queue = multiprocessing.Queue()
    # copy_imagesrc = imagesrc
    # lengthilinks = len(copy_imagesrc) // 2
    # print(f"divided portion of dlinks is {lengthilinks} from {len(copy_imagesrc)}")
    # imagesrc = imagesrc[:8]
    # length=len(imagesrc)
    # print(f"length of imagesrc after dividing {length} ")

    for images in imagesrc:
        imagesrc_queue.put(images)

    start_time = time.time()

    # Determine the number of processes
    num_processes = 16

    # Create and start the processes
    processes = []
    for i in range(num_processes):
        process = multiprocessing.Process(target=process_download_link,
                                          args=(i, imagesrc_queue, link_queue, allongoing,chrome_options))
        processes.append(process)
        process.start()

    # Wait for all processes to finish
    for process in processes:
        process.join()

    end_time = time.time()

    # Calculate the total execution time
    total_time = end_time - start_time
    print(f"Total time taken: {total_time} seconds")
    endingmessage = f"Total time taken: {total_time} seconds"
    bot_token = '6407514901:AAHU4wk67IGgKQIUslHGiMotggWZmwKFf90'
    group_chat_id = '@barryallen16projectgroup'

    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_telegram_message(bot_token, group_chat_id, endingmessage))



