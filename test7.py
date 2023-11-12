from multiprocessing import Pool

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, ElementNotInteractableException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver

chrome_options = webdriver.ChromeOptions()

# chrome_options.add_argument("--headless")



def is_element_present(driver, by, value, timeout=10):
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        return True
    except TimeoutException:
        return False


def scrape(url):
    try:
        user_agent = "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.92 Mobile Safari/537.36"
        chrome_options.add_argument(f"user-agent={user_agent}")
        referer = "https://moviesmod.shop/"
        chrome_options.add_argument('--disable-gpu')  # Required in some cases for headless mode
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument("--enable-javascript")
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--pageLoadStrategy=normal')

        driver = webdriver.Chrome(options=chrome_options)
        try:
            driver.get(url)
        except:
            try:
                driver.get(url)
            except:
                try:
                    driver.get(url)
                except:
                    pass
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

        wait = WebDriverWait(driver, 20)  # Set a timeout of 10 seconds

        element2 = wait.until(
            EC.presence_of_element_located((By.LINK_TEXT, 'GO TO DOWNLOAD')))
        if element2:
            driver.execute_script("""var button4 = document.getElementById("two_steps_btn");
                                                                                        button4.click()""")
            # Print the page source code
            window_handles = driver.window_handles

            if len(window_handles) == 2:
                driver.switch_to.window(driver.window_handles[0])
                driver.close()
                # time.sleep(2)
                driver.switch_to.window(driver.window_handles[0])

                c_url = driver.current_url
                print(c_url)
        # Close the browser window
        driver.quit()
    except:
        try:
            user_agent = "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.92 Mobile Safari/537.36"
            chrome_options.add_argument(f"user-agent={user_agent}")
            referer = "https://moviesmod.shop/"
            chrome_options.add_argument('--disable-gpu')  # Required in some cases for headless mode
            chrome_options.add_argument('--disable-infobars')
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument("--enable-javascript")
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--pageLoadStrategy=normal')

            driver = webdriver.Chrome(options=chrome_options)
            try:
                driver.get(url)
            except:
                try:
                    driver.get(url)
                except:
                    try:
                        driver.get(url)
                    except:
                        pass
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

            wait = WebDriverWait(driver, 20)  # Set a timeout of 10 seconds

            element2 = wait.until(
                EC.presence_of_element_located((By.LINK_TEXT, 'GO TO DOWNLOAD')))
            if element2:
                driver.execute_script("""var button4 = document.getElementById("two_steps_btn");
                                                                                            button4.click()""")
                # Print the page source code
                window_handles = driver.window_handles

                if len(window_handles) == 2:
                    driver.switch_to.window(driver.window_handles[0])
                    driver.close()
                    # time.sleep(2)
                    driver.switch_to.window(driver.window_handles[0])

                    c_url = driver.current_url
                    print(c_url)
            # Close the browser window
            driver.quit()
        except:
            try:
                user_agent = "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.92 Mobile Safari/537.36"
                chrome_options.add_argument(f"user-agent={user_agent}")
                referer = "https://moviesmod.shop/"
                chrome_options.add_argument('--disable-gpu')  # Required in some cases for headless mode
                chrome_options.add_argument('--disable-infobars')
                chrome_options.add_argument('--disable-extensions')
                chrome_options.add_argument('--disable-dev-shm-usage')
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument("--enable-javascript")
                chrome_options.add_argument('--headless')
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('--disable-dev-shm-usage')
                chrome_options.add_argument('--pageLoadStrategy=normal')

                driver = webdriver.Chrome(options=chrome_options)
                try:
                    driver.get(url)
                except:
                    try:
                        driver.get(url)
                    except:
                        try:
                            driver.get(url)
                        except:
                            pass
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

                wait = WebDriverWait(driver, 20)  # Set a timeout of 10 seconds

                element2 = wait.until(
                    EC.presence_of_element_located((By.LINK_TEXT, 'GO TO DOWNLOAD')))
                if element2:
                    driver.execute_script("""var button4 = document.getElementById("two_steps_btn");
                                                                                                button4.click()""")
                    # Print the page source code
                    window_handles = driver.window_handles

                    if len(window_handles) == 2:
                        driver.switch_to.window(driver.window_handles[0])
                        driver.close()
                        # time.sleep(2)
                        driver.switch_to.window(driver.window_handles[0])

                        c_url = driver.current_url
                        print(c_url)
                # Close the browser window
                driver.quit()
            except:
                pass
if __name__ == '__main__':
    urls = ["https://techmny.com/?id=bnpxOTF5Uk9VOVFZM2lEMkxXUmp0VkVIRldsWmpjSk1yaGxRaGNYdnZ2MTU5SkU5dE83dTRQTFdtaXVPV1Btc0xTeUJMNEgyelFKT1Z5RTJHUlBUeHNBTmxiK1RkM3VoRzE1NlZyZHpxbmNHTEFWc2dNZlpoZDNJblZJTGNVRE0rRFZwR2oySU1lZnRENWhYV2hYVStVMTJhb0VrMmhNZTN2YmJYUDh3d1drMXprUEFiQTREU01ycU1UUCttWW5CMVZTUkZyWCtuMUl6eUgyK0M2Y3FURVFxVEh6R0lTZ1MxKzhlbjhndjIxZ2pTalBDcW1rV1lCTGhkQXFTRXBmTw==",
            "https://techmny.com/?id=bnpxOTF5Uk9VOVFZM2lEMkxXUmp0VkVIRldsWmpjSk1yaGxRaGNYdnZ2MTU5SkU5dE83dTRQTFdtaXVPV1Btc0xTeUJMNEgyelFKT1Z5RTJHUlBUeHNBTmxiK1RkM3VoRzE1NlZyZHpxbmVYaFA1a3F4bnZsUytjWHZ1aTdQRGNiQ0pETVZ4dXorZEZKZzZWMS83TmNJMkVkRXRTcElabkpXZENSOW41Zk84WXpMMkhTVW5qOFY2ckxsWmlxb1JFK3FXV1hZWUF4NnQ2aG01UlN0eGJBZWl4NHJnK1grYjR0bkZMb0VPTUhHSndiUTYrU05CUXJxUi9jYU5aaHNWVg==",
            "https://techmny.com/?id=bnpxOTF5Uk9VOVFZM2lEMkxXUmp0VkVIRldsWmpjSk1yaGxRaGNYdnZ2MTU5SkU5dE83dTRQTFdtaXVPV1Btc0xTeUJMNEgyelFKT1Z5RTJHUlBUeHNBTmxiK1RkM3VoRzE1NlZyZHpxbmY1V1hDeXdpZHlCMzZ3eGF1cTJ6UXh6Rk5nc3lKSE1ZQjJCeE5qcGxLTWJyR3VSWHVicUhWVSt0T0wzb0tIc3QvaUhQNDNqTkhheTBNZU43cXMxVU9CTzU2enUyRit6bUxnV1BPcnZ2S0d4R1I4ZGtrNmZ0SjdkQVFWbVJmMk82NWg0TW9tRUNFSE1EaUptOHo1OTYwQw==",
            "https://techmny.com/?id=bnpxOTF5Uk9VOVFZM2lEMkxXUmp0VkVIRldsWmpjSk1yaGxRaGNYdnZ2MTU5SkU5dE83dTRQTFdtaXVPV1Btc0xTeUJMNEgyelFKT1Z5RTJHUlBUeHNBTmxiK1RkM3VoRzE1NlZyZHpxbmZGaDJhU0RBN2U0L0R3VkN3ei9BMEk3bzJGTWVnQzFEUkFlL2FJdGYzeWpIa2pQeXJlalpaVVBLNEY0RXRYZEhKbUlicm9rNXY3TG9mRytLTjdwRmpIbXZqTGRNNEpVVE9ZUWlVLzQxV05Mazl2TFVqRjFwVEtEOVdYelNDYXdnYVpzNXNXSWZXNlp2L09tZHBIaFFjZw==",
            "https://techmny.com/?id=bnpxOTF5Uk9VOVFZM2lEMkxXUmp0VkVIRldsWmpjSk1yaGxRaGNYdnZ2MTU5SkU5dE83dTRQTFdtaXVPV1Btc0xTeUJMNEgyelFKT1Z5RTJHUlBUeHNBTmxiK1RkM3VoRzE1NlZyZHpxbmRnUUlIb2JHUXd3QWFBcjNybDd1RmJrZVVuc0QraHhCbkd1OWl1cUkxNEcreldBZmhXVGNScW9nYXE1S0U2c3RtR2ZqUGtuWWJDYlhpeEpjbllENnNxQzlIMlRlL080ODdyM2duR1gzajhoNzdCOFFUcVBDdW04czVFcTNnU3UrRFlBMVd0MDA4RnI4SVdrTm9RS3k0Vg==",
            "https://techmny.com/?id=bnpxOTF5Uk9VOVFZM2lEMkxXUmp0VkVIRldsWmpjSk1yaGxRaGNYdnZ2MTU5SkU5dE83dTRQTFdtaXVPV1Btc0xTeUJMNEgyelFKT1Z5RTJHUlBUeHNBTmxiK1RkM3VoRzE1NlZyZHpxbmNrR3pzeXdOV0djU2ZJYm5XaWNjSHM4RjJIWHhhQytwVVd5bUFJaXpIbVJyeS9nNno2aEZsc3g2ei94blhLQ2ttOTBYcFhqSTlnVVhqZVFrTTcvRVppRnZaNEV4T1cwVG5RQm4zbmdSZGxtNkZtbzJvcmFiN282bkRoWVlwSnNPbXJ6K0dQU2o0cHQ2ZVpBUVpXZVA5Sg==",
            "https://techmny.com/?id=bnpxOTF5Uk9VOVFZM2lEMkxXUmp0VkVIRldsWmpjSk1yaGxRaGNYdnZ2MTU5SkU5dE83dTRQTFdtaXVPV1Btc0xTeUJMNEgyelFKT1Z5RTJHUlBUeHNBTmxiK1RkM3VoRzE1NlZyZHpxbmVIYUxtZHJUR0MxMlgrdGh1WElwUG5sZnNUSkZzR1lOOEt5WUFubUpVUEI5Qnoya1RtcFRTamNJRlBWRUVkTUtvTHZZRkQzOU8rSHJQWUFJSXV6bmR1OHkwSGVTandVbFBtLzhKbFpkN254N0hnZXNEc0MzM1BPOXVoTlNCdnMwUVJWRUhxRWE5aWs1MXpPZmFGcDlDVg==",
            "https://techmny.com/?id=bnpxOTF5Uk9VOVFZM2lEMkxXUmp0VkVIRldsWmpjSk1yaGxRaGNYdnZ2MTU5SkU5dE83dTRQTFdtaXVPV1Btc0xTeUJMNEgyelFKT1Z5RTJHUlBUeHNBTmxiK1RkM3VoRzE1NlZyZHpxbmNDeE01cEFyb3VJc29jSFhScGRvaGdMWnZXejVjOGZJQlJxWHRpNUJLSDkxUnRiV0cybWRaZTVZaGp4WFFMZUc5UHZEQmlXcFlMU01uOEkzdG9HbUkxN2tlalB3NkJQZ1JTbDFTbS9xWEQ0U3FhaTM2T3NtVlg3dTNDaUZTbFlKY0twcktqajRwVXJjTFBpQ20zNHU1ZA==",
            "https://techmny.com/?id=bnpxOTF5Uk9VOVFZM2lEMkxXUmp0VkVIRldsWmpjSk1yaGxRaGNYdnZ2MTU5SkU5dE83dTRQTFdtaXVPV1Btc0xTeUJMNEgyelFKT1Z5RTJHUlBUeHNBTmxiK1RkM3VoRzE1NlZyZHpxbmVaNzRMWVRrVTFoQytkZ2p0L1RvdWNwbGdDRXNpYkVTODJDQlFLSGVYYWZUWGZtdldTRjczMU44ZmdUcXlPWHBuUmhEcVBXbURZUE5mL0pNekdDRTAvUGkxOE1pYUxxNzFhL1oxNEIrZnFEeTdFaXgrb2NoS09zcXFCMy91QjZhQ2dVUUlMUjJnMTI5UGtVZVdab3pKdA==",
            "https://techmny.com/?id=bnpxOTF5Uk9VOVFZM2lEMkxXUmp0VkVIRldsWmpjSk1yaGxRaGNYdnZ2MTU5SkU5dE83dTRQTFdtaXVPV1Btc0xTeUJMNEgyelFKT1Z5RTJHUlBUeHNBTmxiK1RkM3VoRzE1NlZyZHpxbmYxS3dkbWs4aGxFQnhlR1hZRUtYdnhmY0dKeGtqMEtMTENqbUMzd1hTZWxUcmJPRmtRblp3UFdhQnpLMGFCSFBSYUNJdzdpVjhUZXFUcm14cXZCaXl1dU95QXM4NVpHa3lKYXVlL2E4Ulp4NDZ5ZldWOEJjVnJOMUZETTJNYnJlSDR2eUhwOG54Z2w0M3J3aWVIbXV3SQ==",
            "https://techmny.com/?id=bnpxOTF5Uk9VOVFZM2lEMkxXUmp0VkVIRldsWmpjSk1yaGxRaGNYdnZ2MTU5SkU5dE83dTRQTFdtaXVPV1Btc0xTeUJMNEgyelFKT1Z5RTJHUlBUeHNBTmxiK1RkM3VoRzE1NlZyZHpxbmVhTEVZY25vWE1aSFpxK1ZudlpDNWRJbWpQSkQwQ3plQkR5SmZRcDlndFRkbk5XK2tzQXVJYzgzemdSWmxXaFlnNVZUc1RCQ0QyQlU1QnIzMU54cUhlUjFoMW9BVStBZFUvV243UFRZZGFGZHBFV3FLVktDVDVjTXdoMjlvM1BROUYweWhEdzh4VEx2UjAvOWlKVTJUYQ==",
            "https://techmny.com/?id=bnpxOTF5Uk9VOVFZM2lEMkxXUmp0VkVIRldsWmpjSk1yaGxRaGNYdnZ2MTU5SkU5dE83dTRQTFdtaXVPV1Btc0xTeUJMNEgyelFKT1Z5RTJHUlBUeHNBTmxiK1RkM3VoRzE1NlZyZHpxbmVZOUp1SmRKNHcxclhoL3NBNTdQRndTcVphcnRCZVo5Vnd5UVZGZmZpREs3Tms3WVlUeTZadWR5Zlh4a3llbHV5NFpGd1JIditGamg0dk1xVTBycVFabjlITnhOVkZPMndNdEk1ZUJRdWtLeHZSUnF3OXhhYTU1T0hsblIzRStQTUZPR1QrR1lxUlZ1NUtBQm1iWkhOTA==",
            "https://techmny.com/?id=bnpxOTF5Uk9VOVFZM2lEMkxXUmp0VkVIRldsWmpjSk1yaGxRaGNYdnZ2MTU5SkU5dE83dTRQTFdtaXVPV1Btc0xTeUJMNEgyelFKT1Z5RTJHUlBUeHNBTmxiK1RkM3VoRzE1NlZyZHpxbmUxcGxyTlB0ak9pd2tPVWpvM1MvSEI2M3JkZ0REV3p6aEt2TFJQWnFQS2ZsN2JDbjRwSHhGRThPbU9rdWFnd1YvNHIwU1pkTlJjSHhNTGU1dnZIelVMcjZ1YVVkTTRuZDYyNHdpVXVPQytuNVNCMDB3dVRYR0Z3eUdBSXF6VWw3N3A4Wm5Ec2k2YXBvY0VEdDNzb01CTg==",
            "https://techmny.com/?id=bnpxOTF5Uk9VOVFZM2lEMkxXUmp0VkVIRldsWmpjSk1yaGxRaGNYdnZ2MTU5SkU5dE83dTRQTFdtaXVPV1Btc0xTeUJMNEgyelFKT1Z5RTJHUlBUeHNBTmxiK1RkM3VoRzE1NlZyZHpxbmNCOC9pL2dvZmg3N25NTEpPV0NjZXpUT3g0ZEtSUVViMllsYm5UZ2EycS9JQTNYK2JwUkN6YUFGU3FvQXVQdXRmUm54akV0dUJ0N00vU2c3WVBWa1FDYXJNT2lzVVJWVTFCYjBoTFZxK3pXS2dWOWI2ZHRXSTdJdTllVksreDhhOTdiK29WdTUzU01FdGhCZndLdXY4Nw==",
            "https://techmny.com/?id=bnpxOTF5Uk9VOVFZM2lEMkxXUmp0VkVIRldsWmpjSk1yaGxRaGNYdnZ2MTU5SkU5dE83dTRQTFdtaXVPV1Btc0xTeUJMNEgyelFKT1Z5RTJHUlBUeHNBTmxiK1RkM3VoRzE1NlZyZHpxbmZPVGxsVGZKZFA1WmNoUnhzYTVaT0ZwN1VDTFNBM0c0YXBQekJqN0pwcVZWS2F3amtYSmFrRjFaZzJWNGhhcm9Td3VzbCt4Yjdkd2VSMGhjcDRrVDcyMEFINHlXYk5tdWovdHRTWmFuSWNFOFdLU3lxbHhzQUhkQnNGTWc0dis0WkVlV0VWaVFtZGdJQi9DY3kzU3Z1QQ==",
            "https://techmny.com/?id=bnpxOTF5Uk9VOVFZM2lEMkxXUmp0VkVIRldsWmpjSk1yaGxRaGNYdnZ2MTU5SkU5dE83dTRQTFdtaXVPV1Btc0xTeUJMNEgyelFKT1Z5RTJHUlBUeHNBTmxiK1RkM3VoRzE1NlZyZHpxbmZ1SSttS250UWhqQ29JTjZyVXNFU2ZVYUNuc2pRYjloZm9EZHFaN0pHS3ZsZzMyalgzV2JmRndTenVDTE5Ba0liN1A4MEJIeElxeXV4UGw4c3dCNlpvUVUrTXNLOWtzZC9kSDhra3RINVVGOXhpLzU5QU1jc1YyOXlGMTZHNDBjWXNjaGxhallQM2NVR1JRcXgxWVZobg==",
            "https://techmny.com/?id=bnpxOTF5Uk9VOVFZM2lEMkxXUmp0VkVIRldsWmpjSk1yaGxRaGNYdnZ2MTU5SkU5dE83dTRQTFdtaXVPV1Btc0xTeUJMNEgyelFKT1Z5RTJHUlBUeHNBTmxiK1RkM3VoRzE1NlZyZHpxbmN2amx3MEFhQ05SN3c2cUNwTEFuMUlTZXR3RTZkR3lGUmMrb0cyT05HaGpQa1FpZi8vbTdvczk5dXJHREtGUTNGdDNUbzZha0VRNEpVTkVMQzhGdjVuRkkzMjdyb3hFenYyVGZwUnFqdzFEa0sxcEJpNWRKSWJzNEVPOXBhd3ZIdkVZTk9QbjFmcFlXSWJpaXVIanFBOQ==",
            "https://techmny.com/?id=bnpxOTF5Uk9VOVFZM2lEMkxXUmp0VkVIRldsWmpjSk1yaGxRaGNYdnZ2MTU5SkU5dE83dTRQTFdtaXVPV1Btc0xTeUJMNEgyelFKT1Z5RTJHUlBUeHNBTmxiK1RkM3VoRzE1NlZyZHpxbmRiWU9pUElxSGxxSUsraUZndmNUL1YrbytHTGNJRmpXMjVrUkJSa2x0ckw5ME8xajZuNk82czM5ckpQYkcwcWVwS2dyWWpqNHRESWRiYW1Nd2hNYUl6OTR4a3N1aUowajA0NVAwZExCN3Y0S0tWOStvZ1RlVWZCcUxRUkNROEZpeEtMMlhVUW03THF1ekUxMXBDL1RPYw==",
            "https://techmny.com/?id=bnpxOTF5Uk9VOVFZM2lEMkxXUmp0VkVIRldsWmpjSk1yaGxRaGNYdnZ2MTU5SkU5dE83dTRQTFdtaXVPV1Btc0xTeUJMNEgyelFKT1Z5RTJHUlBUeHNBTmxiK1RkM3VoRzE1NlZyZHpxbmNhM2h3by9WV2ZNRVg5dCtLSTU0bm9sbDR4Rko3WjQ4UkdwYkpBb2lKc21UNWxSekdrYVFSRUliUjJUbzh1VnAzdUdrWkhDYVMwamJrZ2FkeElmM0taYXRjeDh2RzVGazREZkFRSnNYcnRIS2dwTTdWT1o3Z2RmaFUzaHF4NVhrQThBYXhnaUtWTmx0MVNkM3NKd0J4ZQ==",
            "https://techmny.com/?id=bnpxOTF5Uk9VOVFZM2lEMkxXUmp0VkVIRldsWmpjSk1yaGxRaGNYdnZ2MTU5SkU5dE83dTRQTFdtaXVPV1Btc0xTeUJMNEgyelFKT1Z5RTJHUlBUeHNBTmxiK1RkM3VoRzE1NlZyZHpxbmZ6ck03NGF1UXRBeHpYTzkxMm5WWEQzR2JoZklGUVBNT1AxMXYvbFczYkpQTmpSc1RkZVRYd1JXWHYxcnFHWmtXMVk3U0xTVlcxMjdNczRWRGUxNmsvVzFENDJ0OG1tWWtCZmRaTkFYb1hPMzdod0Z1alFvVmhTZzluSmRyeFcxSTJyYmxOOFVDWUVHK1NXR1FKVlFZeA==",
            "https://techmny.com/?id=bnpxOTF5Uk9VOVFZM2lEMkxXUmp0VkVIRldsWmpjSk1yaGxRaGNYdnZ2MTU5SkU5dE83dTRQTFdtaXVPV1Btc0xTeUJMNEgyelFKT1Z5RTJHUlBUeHNBTmxiK1RkM3VoRzE1NlZyZHpxbmNod25yeGdaSWxZakU2WXBzVTNEdUljUVhQWXFUazQzVEU0c2dib1JVaXZNOXFEeTdWN2U4ZEFYVnpwcmxlQmNoN2x4ZXk4WHZyWW5oblo0MXlUazRXRW0rZWhKcThZTWVWTmJ4cG1wRzBzeGZ2eTRNMnRLV2IwTGR6aXNlak1FZmNUMGhWd3k1SjJBWmtENkYrakV6TA==",
            "https://techmny.com/?id=bnpxOTF5Uk9VOVFZM2lEMkxXUmp0VkVIRldsWmpjSk1yaGxRaGNYdnZ2MTU5SkU5dE83dTRQTFdtaXVPV1Btc0xTeUJMNEgyelFKT1Z5RTJHUlBUeHNBTmxiK1RkM3VoRzE1NlZyZHpxbmZud01kanhWVm1heUpURlV4K2tHRzMvZzRybEMxQkhCdDd0T1BpWkg4UDJ0STRYL3RldjJPNEZTbm50Q01tcDgybE1aM28rUWIrbXMxaHdmZ2I2SXprQkdvcDdoRVhBNFpUYW1mU3NFM1JZYmpVRWtZdnpPTmNWZFBoNGFoTHc4MTh6R09BUmJCOHQyNXhhWE9nRGJ3Zg==",
            "https://techmny.com/?id=bnpxOTF5Uk9VOVFZM2lEMkxXUmp0VkVIRldsWmpjSk1yaGxRaGNYdnZ2MTU5SkU5dE83dTRQTFdtaXVPV1Btc0xTeUJMNEgyelFKT1Z5RTJHUlBUeHNBTmxiK1RkM3VoRzE1NlZyZHpxbmVrdkxLTU44RVZ0TXV6ejZLay9YSWk4bEl3MHZVbVJvU3ZMZ2t2N0xHMHF5U3JSQzBqUXp2bm1QU3BSaUtYeDR6ems3ZkZVeEh0bHd0aVZ3dGZTcUJsQ29VdnBCL1VFZnlQVDViK0d5SnMrN3BIQmdDeCtKT2FDRys4Tjg1UG1MdkQ2QThLdjN2WkFLU1pLL2JPVlg1cw==",
            "https://techmny.com/?id=bnpxOTF5Uk9VOVFZM2lEMkxXUmp0VkVIRldsWmpjSk1yaGxRaGNYdnZ2MTU5SkU5dE83dTRQTFdtaXVPV1Btc0xTeUJMNEgyelFKT1Z5RTJHUlBUeHNBTmxiK1RkM3VoRzE1NlZyZHpxbmVtSFNaMGdPQi9EUVR2bEFJTWRNMGFsa25EV2hBTlorYVBCRDN5MlM0clcvbmJnbUgrdjVUREFOczA2QzZtY21OdzRmWVBMcThheVZleFY1RzkrOW9Udk51alA2MVRnTzFOek1xaDZhTitLUXRZTnBWSDdXL2xKbHRqU3ZzZXhHcW9OWVM1VjhuZWxDYTNtYU40a2s1cQ==",
            "https://techmny.com/?id=bnpxOTF5Uk9VOVFZM2lEMkxXUmp0VkVIRldsWmpjSk1yaGxRaGNYdnZ2MTU5SkU5dE83dTRQTFdtaXVPV1Btc0xTeUJMNEgyelFKT1Z5RTJHUlBUeHNBTmxiK1RkM3VoRzE1NlZyZHpxbmZuM3BjUFV1ZnNFT3RuRVVyZjhxK1hReXlIdW41RW4yV1lvNDZ2QTJ6cjkrYjhTQ2xDWlk4K2hoYno1eUxXMTg4WXU4WlJpS3UzYVVra0FZaWpiOGNtQWVLcUY3ZjZpNFpoMStNSi96ckx0NDhabGNUd29HNTFyVzlSZWlGUkJYRSt6U1FNdW1Od0gxNTlZc25jV0Q4bg==",
            "https://techmny.com/?id=bnpxOTF5Uk9VOVFZM2lEMkxXUmp0VkVIRldsWmpjSk1yaGxRaGNYdnZ2MTU5SkU5dE83dTRQTFdtaXVPV1Btc0xTeUJMNEgyelFKT1Z5RTJHUlBUeHNBTmxiK1RkM3VoRzE1NlZyZHpxbmNxT05TYVRFdnZoaE9ZdWU0YmNmMS9rbktLM0NBVkNCYStSQXJmdkVvai9tVEpPVzdCMGdjNmU0ODlML3NoSFk0YzcvWGlZT252NmY0M1BoeFVmYVlmTU9iZytHK3Y4dE0vcDVDaFVlMDlTNFI4aUNWS2lYay9VRGdiaDhISUlEWVluWlZML2ZFWkFTUXFGaGFIWDg2NQ==",
            "https://techmny.com/?id=bnpxOTF5Uk9VOVFZM2lEMkxXUmp0VkVIRldsWmpjSk1yaGxRaGNYdnZ2MTU5SkU5dE83dTRQTFdtaXVPV1Btc0xTeUJMNEgyelFKT1Z5RTJHUlBUeHNBTmxiK1RkM3VoRzE1NlZyZHpxbmRZRWZxYXNHb29qelg3aVNBcjZHR1NJc2cySVcvaEdMNWY0ZHFYbk0vb0tIczNHRTNYeHJWU09ldk9LTHRkNnBrRVAydkJyc1pQNHkwMkR4eEoyR1VzbE9Yc1AyOHlPWU1Sa2dhd0pONE01WFRGY2FhQVhIbU9mbU1jaHJJSFo0OURhSXc5M09Jc3IwYjhmMXZ1bjJJYw=="
       ]  # List of URLs to scrape
    with Pool(processes=16) as pool:  # Adjust the number of processes as needed
        pool.map(scrape, urls)
