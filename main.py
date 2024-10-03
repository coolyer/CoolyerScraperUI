import sys
import threading
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QRadioButton,
    QLabel,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QButtonGroup,
    QMessageBox,
    QAction
)
from PyQt5.QtGui import QPalette, QColor
from bs4 import BeautifulSoup
import time
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
# Use to clean the code
from retailers_links import retailersFile
from browers_choice import initialize_driver
from theme_changer import read_theme_settings
from version_checker import check_for_updates, version_check



class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        theme_mode, background_color, text_color, buttons_color, text_size, font_style = read_theme_settings("config.json")


        # Set background color for the entire application
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(background_color))
        self.setPalette(palette)

        # Apply text color to various elements
        self.product_label.setStyleSheet(f"color: {text_color};font-size: {text_size}; font-family: {font_style}")
        self.scraper_output_label.setStyleSheet(f"color: {text_color}; font-size: {text_size}; font-family: {font_style}")
        self.start_button.setStyleSheet(f"color: {text_color}; background-color: {buttons_color};")
        #self.stop_button.setStyleSheet(f"color: {text_color}; background-color: {buttons_color};")
        self.product_input.setStyleSheet(f"color: {text_color}; background-color: transparent; font-size: {text_size}; font-family: {font_style}")
        self.scraper_output.setStyleSheet(f"color: {text_color}; background-color: transparent; font-size: {text_size}; font-family: {font_style}")
        self.firefox_radio.setStyleSheet(f"color: {text_color}; font-size: {text_size}; font-family: {font_style}")
        self.chrome_radio.setStyleSheet(f"color: {text_color}; font-size: {text_size}; font-family: {font_style}")
        self.edge_radio.setStyleSheet(f"color: {text_color}; font-size: {text_size}; font-family: {font_style}")
        self.original_button_palette = self.start_button.palette()
    def init_ui(self):

        # MenuBar
        menubar = self.menuBar()

        # Create an 'Options' menu with 'Check for Updates', 'About' and 'Exit' actions
        options_menu = menubar.addMenu('Options')

        check_for_updates_action = QAction('Check for Updates', self)
        check_for_updates_action.triggered.connect(lambda:check_for_updates(self))

        # Add the action to the 'Options' menu
        options_menu.addAction(check_for_updates_action)

        about_action = QAction('About',self)
        about_action.triggered.connect(lambda:version_check(self))
        options_menu.addAction(about_action)
        
    
        
        # Create the "Refresh Theme" QAction
        refresh_action = QAction("Refresh Theme", self)
        refresh_action.triggered.connect(self.refresh_theme)
        options_menu.addAction(refresh_action)
        
        
        
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        options_menu.addAction(exit_action)

        
        
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Create the layout
        layout = QVBoxLayout()

        # Browser selection radio buttons
        browser_layout = QHBoxLayout()
        self.browser_group = QButtonGroup()

        self.firefox_radio = QRadioButton('Firefox')
        self.chrome_radio = QRadioButton('Chrome')
        self.edge_radio = QRadioButton('Edge')

        self.browser_group.addButton(self.firefox_radio, 1)
        self.browser_group.addButton(self.chrome_radio, 2)
        self.browser_group.addButton(self.edge_radio, 3)

        browser_layout.addWidget(self.firefox_radio)
        browser_layout.addWidget(self.chrome_radio)
        browser_layout.addWidget(self.edge_radio)

        layout.addLayout(browser_layout)

        # Product label and input field
        self.product_layout = QHBoxLayout()
        self.product_label = QLabel('Product:')
        self.product_input = QLineEdit()
        self.product_input.returnPressed.connect(self.start_scraper)# When enter is pressed start scraping.
        self.product_layout.addWidget(self.product_label)
        self.product_layout.addWidget(self.product_input)
        layout.addLayout(self.product_layout)

        # Scraper output label and text area
        self.scraper_output_layout = QHBoxLayout()
        self.scraper_output_label = QLabel('Scraper Output:')
        self.scraper_output = QTextEdit()
        self.scraper_output.setReadOnly(True)
        self.scraper_output_layout.addWidget(self.scraper_output_label)
        self.scraper_output_layout.addWidget(self.scraper_output)
        layout.addLayout(self.scraper_output_layout)

        # Start button
        self.start_button = QPushButton('Start')
        self.start_button.clicked.connect(self.start_scraper)
        layout.addWidget(self.start_button)

        # Stop button
        self.stop_button = QPushButton('Not Scraping')
        self.stop_button.clicked.connect(self.stop_scraper)
        layout.addWidget(self.stop_button)
        self.stop_button.setEnabled(False)
        self.stop_button.setStyleSheet("background-color: #CCCCCC; color: #808080;")


        # Apply layout to central widget
        self.central_widget.setLayout(layout)

        self.setWindowTitle('CoolyerScraper GUI')
        self.setGeometry(100, 100, 600, 400)


    def refresh_theme(self):
        theme_mode, background_color, text_color, buttons_color, text_size, font_style = read_theme_settings("config.json")
        # Apply text color to various elements
        self.product_label.setStyleSheet(f"color: {text_color};font-size: {text_size}; font-family: {font_style}")
        self.scraper_output_label.setStyleSheet(f"color: {text_color}; font-size: {text_size}; font-family: {font_style}")
        self.start_button.setStyleSheet(f"color: {text_color}; background-color: {buttons_color};")
        #self.stop_button.setStyleSheet(f"color: {text_color}; background-color: {buttons_color};")
        self.product_input.setStyleSheet(f"color: {text_color}; background-color: transparent; font-size: {text_size}; font-family: {font_style}")
        self.scraper_output.setStyleSheet(f"color: {text_color}; background-color: transparent; font-size: {text_size}; font-family: {font_style}")
        self.firefox_radio.setStyleSheet(f"color: {text_color}; font-size: {text_size}; font-family: {font_style}")
        self.chrome_radio.setStyleSheet(f"color: {text_color}; font-size: {text_size}; font-family: {font_style}")
        self.edge_radio.setStyleSheet(f"color: {text_color}; font-size: {text_size}; font-family: {font_style}")
        print("Themed Refreshed")
        
    def start_scraper(self, from_enter=False):
        theme_mode, background_color, text_color, buttons_color, text_size, font_style = read_theme_settings("config.json")
        # Get the selected browser choice
        browser_choice = self.browser_group.checkedId()
        if browser_choice == -1:
            self.scraper_output.clear()
            self.scraper_output.append("Please choose a browser")
            return  # Exit the function if no browser is selected
        
        product_name = self.product_input.text()
    
        if not product_name:
            self.scraper_output.clear()
            self.scraper_output.append("Please enter a product name")
            return  # Exit the function if the product name is empty
        # Disable the start button while scraping is in progress
        self.start_button.setEnabled(False)
        self.start_button.setText("Scraping")
        self.start_button.setStyleSheet("background-color: #CCCCCC; color: #808080;")
        # Stop button
        self.stop_button.setEnabled(True)
        self.stop_button.setText("Stop")
        self.stop_button.setStyleSheet(f"color: {text_color}; background-color: {buttons_color};")

        # Get the product name from the input field
        product_name = self.product_input.text()

        # Clear the scraper output
        self.scraper_output.clear()
        
        # Start the thread to allow it not to stop responding.
        self.scraper_thread = ScraperThread(browser_choice, product_name)

        # Set scraping flag to True
        self.scraper_thread.scraping = True

        # The code to allow it to scrape in real time
        self.scraper_thread.price_scraped.connect(self.update_scraper_output_with_price)

        # Calls what retailer its scraping
        self.scraper_thread.retailer_current.connect(self.retailercurrent)

        # Connect the scraping completion signal to the handling method
        self.scraper_thread.scraping_complete.connect(self.handle_scraping_complete)
        self.scraper_thread.start()
 
    # Checks if scraping is done.  
    def handle_scraping_complete(self, complete):
        if complete:
            # Re-enable the start button after scraping is complete
            self.start_button.setEnabled(True)
            self.start_button.setText("Start Scraping")
            theme_mode, background_color, text_color, buttons_color, text_size, font_style = read_theme_settings("config.json")
            self.start_button.setStyleSheet(f"color: {text_color}; background-color: {buttons_color};")
      
    def retailercurrent(self, retailer):
        # Tells you real time what retailer is scraping from.
        self.scraper_output.append(f"Retailer:{retailer}\n")
        
    def update_scraper_output_with_price(self, price):
        # This method is called when a price is scraped
        self.scraper_output.append(f"{price}")

    def stop_scraper(self):
            # Set scraping flag to False and stops scraping
            self.scraper_thread.scraping = False
            self.scraper_output.append("User stopped scraping process")
            self.stop_button.setEnabled(False)
            self.stop_button.setStyleSheet("background-color: #CCCCCC; color: #808080;")



class ScraperThread(QObject, threading.Thread):
    scraping_complete = pyqtSignal(bool) 
    price_scraped = pyqtSignal(str)
    retailer_current = pyqtSignal(str)
    
    def __init__(self, browser_choice, product_name):
        super().__init__()
        self.browser_choice = browser_choice
        self.product_name = product_name
        self.scraper_output = QTextEdit()
        self.scraping = True
    def run(self):
        try:
            # Call the initialize_driver function to create the WebDriver instance
            driver = initialize_driver(self.browser_choice)
            if driver:
                retailers = retailersFile()
                # Define an empty dictionary to store the product prices and names
                product_data = {}
                
                # Define an empty dictionary to store the cheapest prices and names WIP #TODO
                #cheapest_prices = {}
                
                
                # Loop through each retailer and their search URL
                for retailer, url in retailers.items():
                    retailers = retailersFile()
                    webWaitTime = 4
                    # Construct the full search URL by appending the product name to the base URL
                    search_url = retailers[retailer]['url'] + self.product_name
                    # Open the search URL using the chosen browser
                    driver.get(search_url)
                    # Wait for some time for the web page to load
                    time.sleep(webWaitTime)
                    # Parse the HTML source of the web page using BeautifulSoup
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    print(f"Scraping: {retailer}")     
                    self.retailer_current.emit(retailer)   
                    # Stop the scraper when stop is pressed
                    if self.scraping == False:
                        self.scraping_complete.emit(True)
                        print("Scrape complete")
                        driver.quit()
                    # Scrape the data for each retailer using different CSS selectors or XPath expressions
                    if retailer == 'Tesco':
                        try:
                            tiles = driver.find_elements(By.XPATH, '//li[@class="LD7hL"]')[:retailers[retailer]['num_tiles_to_search']]
                            product_data[retailer] = ''
                            #min_price = float('inf')
                            #min_price_tile = None
                            for index, tile in enumerate(tiles):
                                try:
                                    price_element = WebDriverWait(tile, webWaitTime).until(
                                       EC.visibility_of_element_located((By.XPATH, './/p[contains(@class, "text__StyledText-sc-1jpzi8m-0") and contains(@class, "gyHOWz") and contains(@class, "ddsweb-text") and contains(@class, "styled__PriceText-sc-v0qv7n-1") and contains(@class, "cXlRF")]'))
                                    )
                                    

                                    item_name_element = WebDriverWait(tile, webWaitTime).until(
                                    EC.visibility_of_element_located((By.XPATH, './/span[contains(@class, "styled__Text-sc-1i711qa-1") and contains(@class, "bsLJsh") and contains(@class, "ddsweb-link__text")]'))
                                    )
                                    

                                    pricePerMil_element = WebDriverWait(tile, webWaitTime).until(
                                    EC.visibility_of_element_located((By.XPATH, './/p[contains(@class, "text__StyledText-sc-1jpzi8m-0") and contains(@class, "kiGrpI") and contains(@class, "ddsweb-text") and contains(@class, "styled__Subtext-sc-v0qv7n-2") and contains(@class, "kLkheV") and contains(@class, "ddsweb-price__subtext")]'))
                                    )
                                    try:
                                        clubcard_price_element = tile.find_element(By.XPATH, './/p[contains(@class, "text__StyledText-sc-1jpzi8m-0") and contains(@class, "gljcji") and contains(@class, "ddsweb-text") and contains(@class, "styled__ContentText-sc-1d7lp92-8") and contains(@class, "kjLZec") and contains(@class, "ddsweb-value-bar__content-text")]')
                                        clubcard_price = clubcard_price_element.text.strip()
                                    except NoSuchElementException:
                                        clubcard_price = None


                                    name_html = item_name_element.get_attribute('outerHTML')
                                    soup = BeautifulSoup(name_html, 'html.parser')
                                    name = soup.get_text(strip=True)

                                    # Extract the regular price from the price element
                                    price_html = price_element.get_attribute('innerHTML')
                                    soup = BeautifulSoup(price_html, 'html.parser')
                                    price = soup.get_text(strip=True)
                                    pricePerMil = pricePerMil_element.text.strip()
                                    # Convert price to a float for comparison
                                    #price_value = float(price.replace('£', '').replace(',', ''))

                                    # Update the minimum price if the current price is lower WIP
                                    '''
                                    if price_value < min_price:
                                        min_price = price_value
                                        min_price_tile = {
                                            'name': name,
                                            'price': price,
                                            'price_per_mil': pricePerMil,
                                            'clubcard_price': clubcard_price
                                        }
                                        '''
                                    if clubcard_price is not None:
                                        product_data[retailer] += (f"|Tile {index + 1} - Name: {name}, Price: {price} {pricePerMil}|{clubcard_price}\n")
                                    else:
                                        product_data[retailer] += (f"|Tile  {index + 1} - Name: {name}, Price: {price} {pricePerMil}|\n")
                                except Exception as tile_exception:
                                        print(f"Error processing tile {index + 1}: {str(tile_exception)}")
                            # Part of the cheapest price WIP 
                            '''
                            if min_price_tile:
                                print(f"Cheapest price for {retailer}: {min_price_tile['price']} for {min_price_tile['name']}")
                                cheapest_prices[retailer] = min_price_tile
                            '''
                        # Error handler           
                        except Exception as e:
                            print("Error parsing tile:", str(e))
                            
                        
                        self.price_scraped.emit(product_data[retailer])
                        
                        #cheapest_prices_summary = "\n".join([f"{retailer}: {data['price']} for {data['name']}" for retailer, data in cheapest_prices.items()])
                        #self.price_scraped.emit(cheapest_prices_summary)
                        
                    elif retailer == 'Asda':
                        try:
                            tiles = driver.find_elements(By.XPATH, '//li[@class=" co-item co-item--rest-in-shelf "]')[:retailers[retailer]['num_tiles_to_search']]
                            product_data[retailer] = ""
                            #min_price = float('inf')
                            #min_price_tile = None
                            for index, tile in enumerate(tiles):
                                try:
                                    price_element = WebDriverWait(tile, webWaitTime).until(
                                    EC.visibility_of_element_located((By.XPATH, './/strong[contains(@class,"co-product__price")]'))
                                    )
                                    
                                    item_name_element = tile.find_element(By.XPATH, './/h3[@class="co-product__title"]/a[@class="co-product__anchor"]')
                                    
                                    try:
                                        Asdalitres_element = tile.find_element(By.XPATH, './/span[@class="co-product__volume co-item__volume"]')
                                        Asdalitres = Asdalitres_element.text.strip()
                                        
                                    except NoSuchElementException:
                                        Asdalitres = None
                                    try:
                                        deal_element = tile.find_element(By.XPATH, '//a[@data-auto-id="linkPromoDetail"]')
                                        deal_text = deal_element.find_element(By.CLASS_NAME, 'link-save-banner-large__config--font-normal').text
                                        deal_price = deal_element.find_element(By.CLASS_NAME, 'link-save-banner-large__config--font-huge').text
                                        deal_info = f"{deal_text} {deal_price}"
                                    except NoSuchElementException:
                                        deal_info =""
                                    name = item_name_element.text.strip()
                                    price_html = price_element.get_attribute('innerHTML')
                                    soup = BeautifulSoup(price_html, 'html.parser')
                                    price = soup.get_text(strip=True).replace("now", "")
                                   
                                   
                                    if Asdalitres is not None:
                                        product_data[retailer] += (f"|Tile {index + 1} - Name: {name} {Asdalitres}, Price: {price}|{deal_info}\n")
                                    else:
                                        product_data[retailer] += (f"|Tile {index + 1} - Name: {name}, Price: {price}|{deal_info}\n")
                                except Exception as e:
                                        print(f"{retailer} error: {str(e)}")
                                    
                            
                            
                        except Exception as e:
                            print(f"{retailer} error: {str(e)}")
                        # Code to allow it to update in real time.
                        self.price_scraped.emit(product_data[retailer])   
                         
                        
                    elif retailer == 'B&M':
                        try:
                            tiles = driver.find_elements(By.XPATH, '//li[@class="col-6 col-landscape-4 mt-3 pt-lg-3 px-lg-3"]')[:retailers[retailer]['num_tiles_to_search']]
                            product_data[retailer] = ''
                            for index, tile in enumerate(tiles):
                                try:
                                    price_element = WebDriverWait(tile, webWaitTime).until(
                                        EC.visibility_of_element_located((By.XPATH, '//span[contains(@class, "d-block h5 mb-0 text-secondary bm-line-compact")][contains(@class, "bm-line-compact")]'))
                                    )

                                    item_name_element = WebDriverWait(tile, webWaitTime).until(
                                        EC.visibility_of_element_located((By.CLASS_NAME, 'bm-product-stretch-link')))

                                    try:
                                        bmdeals_element = tile.find_element(By.XPATH, './/span[contains(@class, "offer-text")]')
                                        bmdeals = bmdeals_element.text.strip()
                                    except NoSuchElementException:
                                        bmdeals = None
                                    try:
                                        bmoffer_element = tile.find_element(By.XPATH, './/span[contains(@class, "badge badge-primary text-wrap")]')
                                        bmoffer = bmoffer_element.text.strip()
                                    except NoSuchElementException:
                                        bmoffer =None
                                        

                                    name_html = item_name_element.get_attribute('outerHTML')
                                    soup = BeautifulSoup(name_html, 'html.parser')
                                    name = soup.get_text(strip=True)

                                    # Extract the regular price from the price element
                                    price_html = price_element.get_attribute('innerHTML')
                                    soup = BeautifulSoup(price_html, 'html.parser')
                                    price = soup.get_text(strip=True)
                                    if bmdeals is not None and bmoffer is not None:
                                        product_data[retailer] += (f"|Tile {index + 1} - Name: {name}, Price: {price}| Deals: {bmdeals}, Offers: {bmoffer}|\n")
                                    elif bmdeals is not None:
                                        product_data[retailer] += (f"|Tile {index + 1} - Name: {name}, Price: {price}| Deals: {bmdeals}|\n")
                                    elif bmoffer is not None:
                                        product_data[retailer] += (f"|Tile {index + 1} - Name: {name}, Price: {price}| Offers: {bmoffer}|\n")
                                    else:
                                        product_data[retailer] += (f"|Tile {index + 1} - Name: {name}, Price: {price}|\n") 

                                except Exception as e:
                                    print(f"{retailer} error: {str(e)}")
                            # Add an error handler or continue based on your needs

                        except Exception as e:
                                print(f"{retailer} error: {str(e)}")
                        # Code to allow it to update in real time.
                        self.price_scraped.emit(product_data[retailer])     
                    elif retailer == 'Sainsburys':
                        try:
                            tiles1 = driver.find_elements(By.XPATH, '//li[@class= "pt-grid-item ln-o-grid__item ln-u-1/2@xs ln-u-1/3@sm ln-u-1/4@md ln-u-1/5@xl"]')[:retailers[retailer]['num_tiles_to_search']]
                            tiles2 = driver.find_elements(By.XPATH, '//li[@class="gridItem"]')[:retailers[retailer]['num_tiles_to_search']]
                            tiles = tiles1 + tiles2
                            product_data[retailer] = ""
                            for index, tile in enumerate(tiles):
                                try:
                                    price_element1 = tile.find_elements(By.XPATH, './/div[@class = "pricing"]/p[@class = "pricePerUnit"]')
                                    price_element2 = tile.find_elements(By.XPATH, './/span[contains(@class, "pt__cost__retail-price pt__cost__retail-price--with-nectar-not-associated")]')
                                    price_element3 = tile.find_elements(By.CLASS_NAME, 'pt__cost__retail-price')
                                    # Extract the price based on whichever element is found
                                    price = ""
                                    if price_element1:
                                        price = price_element1[0].text.strip()
                                    elif price_element2:
                                        price = price_element2[0].text.strip()
                                    elif price_element3:
                                        price = price_element3[0].text.strip()
                                        
                                    name_element1 = tile.find_elements(By.XPATH, './/a[contains(@class, "pt__link")]')
                                    name_element2 = tile.find_elements(By.XPATH, './/div[contains(@class, "productNameAndPromotions")]/h3/a')

                                    # Extract the product name based on whichever element is found
                                    name = ""
                                    if name_element1:
                                        name = name_element1[0].text.strip()
                                    elif name_element2:
                                        name = name_element2[0].text.strip()
                                    try:
                                        nectar_price_element1 = tile.find_elements(By.XPATH, './/div[@class = "pricing"]/p[@class = "pricePerUnit nectarPrice"]')
                                        nectar_price_element2 = tile.find_elements(By.XPATH, './/span[contains(@class, "pt__cost--price")]')
                                        # Extract the nectar price based on whichever element is found
                                        nectar_price = ""
                                        if nectar_price_element1:
                                            nectar_price = "Nectar price: " + nectar_price_element1[0].text.strip()
                                        elif nectar_price_element2:
                                            nectar_price = "Nectar price: " + nectar_price_element2[0].text.strip()
                                    except NoSuchElementException:
                                        nectar_price = ''

                                    # Extract the regular price from the price element
                                    
                                    product_data[retailer] += (f"|Tile {index + 1} - Name: {name}, Price: {price}|{nectar_price}\n")
                                except Exception as e:
                                    print(f"{retailer} error: {str(e)}")
                        except Exception as e:
                                print(f"{retailer} error: {str(e)}")
                        # Code to allow it to update in real time.
                        self.price_scraped.emit(product_data[retailer])    
                    elif retailer == 'Iceland':
                        try:
                            tiles = driver.find_elements(By.XPATH, './/div[@data-test-selector="product-list-item"]')[:retailers[retailer]['num_tiles_to_search']]
                            product_data[retailer] = ""
                            for index, tile in enumerate(tiles):
                                try:
                                    price_elements = tile.find_elements(By.XPATH, './/span[contains(@class, "_105qcvc3w3") and contains(@class, "_105qcvc3wl") and contains(@class, "_105qcvc3xo")]')
                                    price = price_elements[0].text.strip()
                                    

                                    item_name_element = tile.find_element(By.XPATH, './/a[@data-test-selector="product-list-item-name"]')
                                    
                                    pricePerUnit_element = tile.find_element(By.XPATH, './/p[contains(@class, "_105qcvc3w3")]')
                                    
                                    try:
                                        iceLandOffers_element = tile.find_element(By.XPATH, './/div[contains(@class, "_105qcvcu9") and contains(@class, "_105qcvcwu") and contains(@class, "_105qcvcxc")]')
                                        offer_spans = iceLandOffers_element.find_elements(By.XPATH, './/span[contains(@class, "_105qcvc3w3")]')
                                        iceLandOffers = " ".join([span.text.strip() for span in offer_spans])
                                        # Remove duplicate "each" if present
                                        iceLandOffers = iceLandOffers.replace(" each each", " each")
                                    except NoSuchElementException:
                                        iceLandOffers = None
                                    
                                    name = item_name_element.text.strip()
                                    pricePerMil = pricePerUnit_element.text.strip()
                                    
                                    
                                    if iceLandOffers is not None:
                                        product_data[retailer] += (f"|Tile {index + 1} - Name: {name}, Price: {price} ({pricePerMil}) |Multibuy Price: {iceLandOffers} each \n")
                                    else:
                                        product_data[retailer] += (f"|Tile {index + 1} - Name: {name}, Price: {price} ({pricePerMil})|\n")
                                except NoSuchElementException as e:
                                    print(f"Error finding elements for tile {index + 1}: {str(e)}")
                                except Exception as e:
                                    print(f"Error processing tile {index + 1}: {str(e)}")
                        except Exception as e:
                                print(f"{retailer} error: {str(e)}")
                        # Code to allow it to update in real time.
                        self.price_scraped.emit(product_data[retailer])    
                    elif retailer == 'Poundshop':
                        try:
                            tiles = driver.find_elements(By.XPATH, '//li[@class= "rrp item product product-item"]')[:retailers[retailer]['num_tiles_to_search']]
                            product_data[retailer] = ""
                            for index, tile in enumerate(tiles):
                                try:
                                    price_element = WebDriverWait(driver, webWaitTime).until(
                                    EC.visibility_of_element_located((By.CLASS_NAME, 'price'))
                                    )
                                    

                                    item_name_element = tile.find_element(By.CLASS_NAME, 'product-item-link')
                                    
                                    try:
                                        poundShopOffersStart_element = tile.find_element(By.CLASS_NAME, 'price')
                                        poundShopOffersStart = poundShopOffersStart_element.text.strip()
                                        poundShopOffersExtra_element = tile.find_element(By.CLASS_NAME, 'qty-label')
                                        poundShopOffersExtra = poundShopOffersExtra_element.text.strip()
                                        poundShopOffers = (f" {poundShopOffersStart} {poundShopOffersExtra}")
                                    except NoSuchElementException:
                                        poundShopOffers = None
                                    
                                    name = item_name_element.text.strip()
                                    price_html = price_element.get_attribute('innerHTML')
                                    soup = BeautifulSoup(price_html, 'html.parser')
                                    price = soup.get_text(strip=True).replace("now", "")
                                    
                                    if poundShopOffers is not None:
                                        product_data[retailer] += (f"|Tile {index + 1} - Name: {name}, Price: £{price}|{poundShopOffers}\n")
                                    else:
                                        product_data[retailer] += (f"|Tile {index + 1} - Name: {name}, Price: £{price}|\n")
                                except Exception as e:
                                        print(f"{retailer} error: {str(e)}")
                                    # Add an error handler or continue based on your needs
                            
                        except Exception as e:
                            print(f"{retailer} error: {str(e)}")    
                        # Code to allow it to update in real time.
                        self.price_scraped.emit(product_data[retailer]) 
                    elif retailer == 'Poundland':
                        try:
                            tiles = driver.find_elements(By.XPATH, '//li[@class= " item product product-item c-product c-product__item"]')[:retailers[retailer]['num_tiles_to_search']]
                            product_data[retailer] = ""
                            for index, tile in enumerate(tiles):
                                try:
                                    price_element = tile.find_elements(By.CLASS_NAME, 'c-product__price')
                                    price = price_element[0].text.strip()
                                    item_name_element = tile.find_element(By.CLASS_NAME, 'c-product__title')
                                    
                                    try:
                                        poundLandOffers_element = tile.find_element(By.CLASS_NAME, 'c-product__promo')
                                        poundLandOffers = poundLandOffers_element.text.strip()
                                        
                                    except NoSuchElementException:
                                        poundLandOffers = None
                                    
                                    name = item_name_element.text.strip()
                                    
                                    if poundLandOffers is not None:
                                        product_data[retailer] += (f"|Tile {index + 1} - Name: {name}, Price: {price}|{poundLandOffers} each \n")
                                    else:
                                        product_data[retailer] += (f"|Tile {index + 1} - Name: {name}, Price: {price}|\n")
                                except Exception as e:
                                        print(f"{retailer} error: {str(e)}")
                                    # Add an error handler or continue based on your needs
                            
                        except Exception as e:
                            print(f"{retailer} error: {str(e)}")  
                        # Code to allow it to update in real time.
                        self.price_scraped.emit(product_data[retailer]) 
                    elif retailer == 'Aldi':
                        try:
                            tiles = driver.find_elements(By.XPATH, '//div[@data-qa="search-result"]')[:retailers[retailer]['num_tiles_to_search']]
                            product_data[retailer] = ""
                            for index, tile in enumerate(tiles):
                                    try:
                                        name_element = tile.find_element(By.XPATH, './/a[@data-qa="search-product-title"]')
                                        price_element = tile.find_element(By.XPATH, './/span[@class="h4"]/span')

                                        # Extract the product name and price
                                        name = name_element.text.strip()
                                        price = price_element.text.strip()

                                        # Add the extracted data to product_data
                                        product_data[retailer] += (f"|Tile {index + 1} - Name: {name}, Price: {price}|\n")
                                    except Exception as e:
                                        print(f"{retailer} error: {str(e)}")
                        except Exception as e:
                            print(f"{retailer} error: {str(e)}")
                        # Code to allow it to update in real time.
                        self.price_scraped.emit(product_data[retailer])     
                    elif retailer == 'Morrisons':
                        try:
                            tiles = driver.find_elements(By.XPATH, '//div[contains(@class, "sc-filq44-0") and contains(@class, "cZSNQJ")]')[:retailers[retailer]['num_tiles_to_search']]
                            #print(f"Found {len(tiles)} tiles for {retailer}")
                            product_data[retailer] = ""
                            for index, tile in enumerate(tiles):
                                try:
                                    #print(f"Processing tile {index + 1}/{len(tiles)}")
                                    name_element = tile.find_element(By.XPATH, './/h3[@data-test="fop-title"]')
                                    price_element = tile.find_elements(By.XPATH, './/span[@data-test="fop-price"]')
                                    #price_element1 = tile.find_elements(By.XPATH, './/div[@data-test = "fop-offer-text"]')
                                    price = ""
                                    if price_element:
                                        price = price_element[0].text.strip()
                                       # print(f"Price found: {price}")
                                    
                                    
                                    # Extract the product name and price
                                    name = name_element.text.strip()
                                    try:
                                    # Check if there's a promotional offer
                                        promo_element = tile.find_element(By.XPATH, './/span[@data-test = "fop-offer-text"]')
                                        promo = promo_element.text.strip()
                                    except NoSuchElementException:
                                        promo = None
                                    try:
                                        weight_element = tile.find_element(By.XPATH, './/span[@data-test="fop-price-per-unit"]')
                                        weight = weight_element.text.strip()
                                    except NoSuchElementException:
                                        weight = None
                                    # Add the extracted data to product_data
                                    if promo:
                                        product_data[retailer] += (f"|Tile {index + 1} - Name: {name} {weight}, Price: {price}|{promo}\n")
                                    else:
                                        product_data[retailer] += (f"|Tile {index + 1} - Name: {name} {weight}, Price: {price}|\n")
                                except NoSuchElementException as e:
                                    print(f"Error finding elements for tile {index + 1}: {str(e)}")
                                except Exception as e:
                                    print(f"Error processing tile {index + 1}: {str(e)}")
                            self.price_scraped.emit(product_data[retailer])
                        except Exception as e:
                            print(f"{retailer} error: {str(e)}")
            
                                         
        except WebDriverException as e:
                print(f"WebDriverException: {str(e)}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        finally:
            # Set scraping flag to False when scraping is done
            self.scraping = False
            self.scraping_complete.emit(True)
            if driver:
                print("Scrape complete")
                driver.quit()
                
                          
def main():
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()