
# Coolyer Scraper UI (Product Price Scraper)

Coolyer Scraper UI is a Python application that allows you to easily scrape product prices from various retailers. This user-friendly interface builds upon the original Coolyer Scraper script by adding new features, including a theme changer for a customized user experience.

## Prerequisites

-   Python 3.x
-   Firefox, Chrome, or Edge browser (depending on your choice)
-   GeckoDriver for Firefox, ChromeDriver for Chrome, or EdgeDriver for Edge (automatically installed via `webdriver_manager`)
-   PyQt5 library (installed via `requirements.txt`)

## Installation

1.  Clone the repository:
    
   ```bash 
    git clone https://github.com/coolyer/coolyerScraperUI 
   ```
    
2.  Install the required Python packages:
    
  ```  bash
   pip install -r requirements.txt
   ```
    

## Usage

1.  Run the Python script:
   ``` bash 
    python main.py
   ```
    
2.  On startup, a popup will inform you that scraping may freeze the program. Please wait for the scraper to complete.
    
3.  Choose your preferred browser (Firefox, Chrome, or Edge) by selecting the respective radio button.
    
4.  Enter your estimated website loading time based on your connection speed in seconds.
    
5.  Provide the product name you want to search for in the input field.
    
6.  The script will display the scraped prices and item names from various retailers in a user-friendly interface.
    
7.  You can't edit the scraper output; it's for display purposes only.
    
8.  After displaying the results, you will have the option to search for another product or exit the program.
    

## Theme Changer

The Coolyer Scraper UI allows you to customize the appearance of the application with the theme changer feature. You can change the text color, button color, and background color to suit your preferences.

## Supported Retailers

The script supports scraping from the following retailers:

-   Tesco
-   Asda
-   B&M
-   Sainsburys
-   Poundland
-   Poundshop
-   Morrisons
-   Aldi

## License

This project is licensed under the [MIT License](LICENSE).

## Disclaimer

Please note that web scraping might be against the terms of service of some websites. Use this script responsibly and make sure to review the terms of service of the websites you are scraping data from.

## Acknowledgments

The script uses [Selenium](https://www.selenium.dev/) for browser automation and [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) for web scraping. Special thanks to the developers of these excellent libraries.

## Future Features

This project aims to continually improve and expand its functionality. Here are some planned features for future updates:

-   Expanded Browser Support: Future versions will include support for more web browsers, such as Brave and Opera, providing users with even more choices for their scraping needs.
    
-   Code Optimization: Ongoing work will focus on optimizing and refining the codebase for improved performance and efficiency.
    
-   Increased Retailer Coverage: We aim to expand the list of supported websites, offering users access to an even broader range of online stores for price scraping.

-   Cross-Platform Accessibility: My goal is to ensure a seamless and user-friendly experience for all. Once we achieve this, we will embark on the journey of transforming our application into a versatile and accessible iOS and Android app.


   

We are dedicated to maintaining and enhancing this product scraper to meet the evolving needs of our users. Your feedback and suggestions are valuable to us, so please share your ideas for additional features or improvements. Together, we can make this tool even more powerful and user-friendly. Thank you for using Coolyer Scraper UI!

## Web-Based Version (Idea/soon?)


My vision for CoolyerScraper extends beyond desktop applications. We're actively working on creating a web-based version of our product that will allow you to access and utilize our scraper directly through your web browser. With this approach, there's no need for downloads or installations. Simply visit our website, input your preferences, and let the scraping begin.

Here's a sneak peek at what you can look forward to:

- Instant Access: Say goodbye to the hassle of installations. Our web-based version will be accessible instantly, saving you time and effort.

- Cross-Platform Compatibility: Whether you're on a Windows PC, Mac, Linux, or even a mobile device, you'll be able to use CoolyerScraper from your preferred web browser.

- Seamless Updates: We'll handle all updates and maintenance on our end, ensuring you always have access to the latest features and website compatibility.

- User-Friendly Interface: We're designing the web-based version with user convenience in mind, making it intuitive and easy to navigate.

This is just a Idea as I want to expand this and make it easy and free to use. 

## The Team

**Main Programmer: Josh**

# Bugs

- Please report any bugs found.
