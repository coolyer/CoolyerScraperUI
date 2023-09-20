import sys
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

        # TODO Make this work when threading is implemented
        # Stop button
        #self.stop_button = QPushButton('Stop')
        #self.stop_button.clicked.connect(self.stop_scraper)
        #layout.addWidget(self.stop_button)

        # Apply layout to central widget
        self.central_widget.setLayout(layout)

        self.setWindowTitle('CoolyerScraper GUI')
        self.setGeometry(100, 100, 600, 400)

    
    def start_scraper(self, from_enter=False):
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
        
        # Get the product name from the input field
        product_name = self.product_input.text()

        # Clear the scraper output
        self.scraper_output.clear()
        self.show_freeze_warning()
        
        # Set scraping flag to True
        self.scraping = True

        # Call the scrape_and_update_ui method in the main thread
        self.scrape_and_update_ui(browser_choice, product_name)
        
        # Re-enable the start button after scraping is complete
        self.start_button.setEnabled(True)
        
    def show_freeze_warning(self):
        # Fetch theme settings from config
        theme_mode, background_color, text_color, button_color, text_size, font_style = read_theme_settings("config.json")

        # Create and configure the message box
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setWindowTitle("Information")
        self.msg.setText("Scraping may freeze the program. Please wait.")
        self.msg.setStandardButtons(QMessageBox.Ok)

        # Set the style of the message box using the fetched color values
        style = f"""
            QLabel {{
            color: {text_color};
            }}
            QPushButton {{
                color: {text_color};
                background-color: {button_color};
            }}
            QMessageBox {{
                background-color: {background_color};
            }}
            """
        self.msg.setStyleSheet(style)

        # Execute the message box
        self.msg.exec_()
        
    def stop_scraper(self):
            # Set scraping flag to False
            self.scraping = False
               
    def scrape_and_update_ui(self, browser_choice, product_name):
        try:
            # Call the initialize_driver function to create the WebDriver instance
            driver = initialize_driver(browser_choice)
       
            if driver:
                retailers = retailersFile()
                # Define an empty dictionary to store the product prices and names
                product_data = {}
                # Loop through each retailer and their search URL
                for retailer, url in retailers.items():
                    retailers = retailersFile()
                    webWaitTime = 4
                    # Construct the full search URL by appending the product name to the base URL
                    search_url = retailers[retailer]['url'] + product_name
                    # Open the search URL using the chosen browser
                    driver.get(search_url)
                    # Wait for some time for the web page to load
                    time.sleep(webWaitTime)
                    # Parse the HTML source of the web page using BeautifulSoup
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    print(f"Scraping: {retailer}")     
                    
                    # Scrape the data for each retailer using different CSS selectors or XPath expressions
                    if retailer == 'Tesco':
                        try:
                            tiles = driver.find_elements(By.XPATH, '//li[@class="product-list--list-item"]')[:retailers[retailer]['num_tiles_to_search']]
                            product_data[retailer] = ''
                            for index, tile in enumerate(tiles):
                                try:
                                    price_element = WebDriverWait(tile, webWaitTime).until(
                                        EC.visibility_of_element_located((By.CLASS_NAME, 'beans-price__text'))
                                    )

                                    item_name_element = WebDriverWait(tile, webWaitTime).until(
                                    EC.visibility_of_element_located((
                                                    By.XPATH,
                                                    './/span[@class= "styled__Text-sc-1i711qa-1 xZAYu ddsweb-link__text"]')))

                                    pricePerMil_element = WebDriverWait(tile, webWaitTime).until(
                                    EC.visibility_of_element_located((By.CSS_SELECTOR, '.styled__StyledFootnote-sc-119w3hf-7.icrlVF.styled__Subtext-sc-8qlq5b-2.bNJmdc.beans-price__subtext')))
                                    try:
                                        clubcard_price_element = tile.find_element(By.XPATH, './/span[contains(@class, "offer-text")]')
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
                                    if clubcard_price is not None:
                                        product_data[retailer] += (f"|Tile {index + 1} - Name: {name}, Price: {price} {pricePerMil}|{clubcard_price}\n")
                                    else:
                                        product_data[retailer] += (f"|Tile {index + 1} - Name: {name}, Price: {price} {pricePerMil}|\n")
                                except Exception as e:
                                        print("Error parsing tile:", str(e))
                                    # Add an error handler or continue based on your needs
                        except Exception as e:
                            print(f"{retailer} error: {str(e)}")

                    elif retailer == 'Asda':
                        try:
                            tiles = driver.find_elements(By.XPATH, '//li[@class=" co-item co-item--rest-in-shelf "]')[:retailers[retailer]['num_tiles_to_search']]
                            product_data[retailer] = ""
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
                                    # Add an error handler or continue based on your needs
                            
                        except Exception as e:
                            print(f"{retailer} error: {str(e)}")
                            
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
                            
                    elif retailer == 'Iceland':
                        try:
                            tiles = driver.find_elements(By.CLASS_NAME, 'grid-tile ')[:retailers[retailer]['num_tiles_to_search']]
                            product_data[retailer] = ""
                            for index, tile in enumerate(tiles):
                                try:
                                    price_elements = tile.find_elements(By.XPATH, './/span[@class="product-sales-price"]/span')
                                    price = price_elements[0].text.strip()
                                    

                                    item_name_element = tile.find_element(By.CLASS_NAME, 'name-link')
                                    
                                    try:
                                        iceLandOffers_element = tile.find_element(By.CLASS_NAME, 'price')
                                        iceLandOffers = iceLandOffers_element.text.strip()
                                        
                                    except NoSuchElementException:
                                        iceLandOffers = None
                                    
                                    name = item_name_element.text.strip()
                                    
                                    
                                    if iceLandOffers is not None:
                                        product_data[retailer] += (f"|Tile {index + 1} - Name: {name}, Price: {price}|Multibuy Price: {iceLandOffers} each \n")
                                    else:
                                        product_data[retailer] += (f"|Tile {index + 1} - Name: {name}, Price: {price}|\n")
                                except Exception as e:
                                        pass # There is a list index out of range error but shows all the correct prices and products so no idea.
                        
                        except Exception as e:
                            print(f"{retailer} error: {str(e)}")
                            
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
                            
                    elif retailer == 'Morrisons':
                        try:
                            tiles = driver.find_elements(By.XPATH, '//li[contains(@class, "fops-item") and contains(@class, "fops-item--on_offer") or contains (@class, "fops-item fops-item--cluster")]')[:retailers[retailer]['num_tiles_to_search']]
                            product_data[retailer] = ""
                            for index, tile in enumerate(tiles):
                                try:
                                    name_element = tile.find_element(By.XPATH, './/div[@class ="fop-description"]/h4[@class="fop-title"]')
                                    price_element = tile.find_elements(By.XPATH, './/div[@class = "price-group-wrapper"]/span[@class="fop-price"]')
                                    price_element1 = tile.find_elements(By.XPATH, './/div[@class = "price-group-wrapper"]/span[@class ="fop-price price-offer"]')
                                    price = ""
                                    if price_element:
                                        price = price_element[0].text.strip()
                                    
                                    elif price_element1:
                                        price = price_element1[0].text.strip()
                                    # Extract the product name and price
                                    name = name_element.text.strip()
                                    try:
                                    # Check if there's a promotional offer
                                        promo_element = tile.find_element(By.XPATH, './/a[@class="fop-row-promo promotion-offer"]/span')
                                        promo = promo_element.text.strip()
                                    except NoSuchElementException:
                                        promo = None
                                    try:
                                        weight_element = tile.find_element(By.XPATH, './/span[@class="fop-catch-weight"]')
                                        weight = weight_element.text.strip()
                                    except NoSuchElementException:
                                        weight = None
                                    # Add the extracted data to product_data
                                    if promo:
                                        product_data[retailer] += (f"|Tile {index + 1} - Name: {name} {weight}, Price: {price}|{promo}\n")
                                    else:
                                        product_data[retailer] += (f"|Tile {index + 1} - Name: {name} {weight}, Price: {price}|\n")
                                except Exception as e:
                                    print(f"{retailer} error: {str(e)}")
                           
                            
                        except Exception as e:
                            print(f"{retailer} error: {str(e)}")
        except WebDriverException as e:
                print(f"WebDriverException: {str(e)}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        finally:
            # Set scraping flag to False when scraping is done
            self.scraping = False
            if driver:
                self.update_ui_with_data(product_data)
                driver.quit()
    
    def update_ui_with_data(self, product_data):
            # Update the UI with the scraped data
            self.scraper_output.setPlainText("Scraped Data:\n")
            for retailer, data in product_data.items():
                self.scraper_output.append(f"Retailer: {retailer}\n{data}\n")  
def main():
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
       
def main():
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
    