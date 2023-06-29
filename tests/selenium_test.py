# Import necessary modules
import time
import unittest
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions


# Define a test case class
class TestStockBot(unittest.TestCase):
    # Define a base URL for the web application
    base_url = "http://127.0.0.1:5000/"
    # Change browsers: firefox, chrome, edge
    browser = "chrome"

    def setUp(self):
        if self.browser == "firefox":
            options = FirefoxOptions()
            self.driver = webdriver.Firefox(options=options)
        elif self.browser == "chrome":
            options = Options()
            options.add_argument("--start-maximized")
            self.driver = webdriver.Chrome(options=options)
        elif self.browser == "edge":
            options = EdgeOptions()
            self.driver = webdriver.Edge(options=options)

        self.driver.get(self.base_url)
        self.driver.maximize_window()
        time.sleep(1) 

    def test_title_welcome(self):
        self.assertEqual(self.driver.title, "StockBot")
        time.sleep(1)

    def test_acknowledge_button(self):
        # Wait for the page to load and the acknowledge button to become clickable
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "acknowledgeButton")))

        # Click the acknowledge button
        self.driver.find_element(By.ID, "acknowledgeButton").click()
        time.sleep(3)

        # Verify that the acknowledgement message disappears
        acknowledgement_message = self.driver.find_element(By.ID,"acknowledgeButton")
        self.assertFalse(acknowledgement_message.is_displayed())

        # Refresh the page and verify that the acknowledgement message appear
        self.driver.refresh()
        acknowledgement_message = self.driver.find_element(By.ID, "acknowledgeButton")
        self.assertTrue(acknowledgement_message.is_displayed())
        
    def test_dont_show_again_button(self):
        # Wait for the page to load and the acknowledge button to become clickable
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "dontShowAgainCheckbox")))

        # Click the acknowledge button
        self.driver.find_element(By.ID, "dontShowAgainCheckbox").click()
        time.sleep(1)
        self.driver.find_element(By.ID, "acknowledgeButton").click()
        time.sleep(3)

        # Verify that the acknowledgement message disappears
        acknowledgement_message = self.driver.find_element(By.ID,"acknowledgeButton")
        self.assertFalse(acknowledgement_message.is_displayed())

        # Refresh the page and verify that the acknowledgement message doesnt appear
        self.driver.refresh()
        acknowledgement_message = self.driver.find_element(By.ID, "acknowledgeButton")
        self.assertFalse(acknowledgement_message.is_displayed())
            
    def test_send_message_no_login(self):
        self.driver.find_element(By.ID, "acknowledgeButton").click()
        time.sleep(3)
        # Wait for the chat window to appear and the input field to become visible
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".chat-window")))
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".input-form")))

        # Enter a message in the input field and submit it
        input_field = self.driver.find_element(By.CSS_SELECTOR, ".input")
        input_field.send_keys("Hello, StockBot!")
        submit_button = self.driver.find_element(By.CSS_SELECTOR, ".input-form button[type=submit]")
        submit_button.click()
        time.sleep(3)

        # Verify that the message is displayed in the chat window
        chat_window = self.driver.find_element(By.CSS_SELECTOR, ".chat-window")
        message = chat_window.find_element(By.XPATH, ".//div[contains(@class, 'message')][last()]")
        self.assertEqual(message.text, "Hello, StockBot!\nUser not authenticated, your messages will not be saved from this point.\nINFO: The input format was invalid.")

    def test_dark_mode(self):
        self.driver.find_element(By.ID, "acknowledgeButton").click()
        time.sleep(2)
        # Wait for the page to load and the toggle-switch to become clickable
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "toggle-switch")))

        # Check if the dark mode is disabled by default
        toggle_switch = self.driver.find_element(By.ID, "toggle-switch")
        self.assertFalse(toggle_switch.is_selected())

        # Click the toggle-switch to enable dark mode
        toggle_switch.click()
        time.sleep(1)

        # Verify that the body background color is changed to dark mode
        body = self.driver.find_element(By.TAG_NAME, "body")
        background_color = body.value_of_css_property("background-color")
        if self.browser == "firefox":
            self.assertEqual(background_color, "rgb(48, 48, 48)")
        elif self.browser == "chrome":
            self.assertEqual(background_color, "rgba(48, 48, 48, 1)")
        elif self.browser == "edge":
            self.assertEqual(background_color, "rgba(48, 48, 48, 1)")

        # Click the toggle-switch to disable dark mode
        toggle_switch.click()
        time.sleep(1)

        # Verify that the body background color is changed back to light mode
        background_color = body.value_of_css_property("background-color")
        if self.browser == "firefox":
            self.assertEqual(background_color, "rgb(240, 240, 240)")
        elif self.browser == "chrome":
            self.assertEqual(background_color, "rgba(240, 240, 240, 1)")
        elif self.browser == "edge":
            self.assertEqual(background_color, "rgba(240, 240, 240, 1)")
        

    def test_from_home_to_help(self):
        self.driver.find_element(By.ID, "acknowledgeButton").click()
        time.sleep(2)
        # Find and click the "Help" link in the navbar
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Help")))
        self.driver.find_element(By.LINK_TEXT, "Help").click()
        time.sleep(2)

        # Verify that the current URL is the Help page
        self.assertEqual(self.driver.current_url, "http://127.0.0.1:5000/help")  
    
    def test_register_login(self):
        self.driver.find_element(By.ID, "acknowledgeButton").click()
        time.sleep(2)
        # Find and click the "Register" link in the navbar
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Register")))
        self.driver.find_element(By.LINK_TEXT, "Register").click()
        time.sleep(2)

        # Verify that the current URL is the Register page
        self.assertEqual(self.driver.current_url, "http://127.0.0.1:5000/register")  
        username = str(random.randint(100000,999999))
        email = str(random.randint(100000,999999))+"@testmail.com"
        password = "password"

        # Fill out the registration form
        self.driver.find_element(By.NAME, "username").send_keys(username)
        self.driver.find_element(By.NAME, "email").send_keys(email)
        self.driver.find_element(By.NAME, "password").send_keys(password)
        self.driver.find_element(By.NAME, "password2").send_keys(password)
        time.sleep(2)
        self.driver.find_element(By.NAME, "submit").click()
        time.sleep(2)

        # Verify that the user is redirected to the login page
        login_url = self.base_url + "login"
        self.assertEqual(self.driver.current_url, login_url)

        # Log in with wrong credentials
        self.driver.find_element(By.NAME, "username").send_keys("wrong")
        self.driver.find_element(By.NAME, "password").send_keys(password)
        time.sleep(2)
        self.driver.find_element(By.CLASS_NAME, "sub-button").click()
        time.sleep(2)
        self.assertEqual(self.driver.current_url, "http://127.0.0.1:5000/login") 

        # Log in with right credentials
        self.driver.find_element(By.NAME, "username").send_keys(username)
        self.driver.find_element(By.NAME, "password").send_keys(password)
        time.sleep(2)
        self.driver.find_element(By.CLASS_NAME, "sub-button").click()
        time.sleep(2)
        self.assertEqual(self.driver.current_url, "http://127.0.0.1:5000/") 

    def test_send_message_and_new_chat(self):
        # Click the acknowledge button
        self.driver.find_element(By.ID, "dontShowAgainCheckbox").click()
        time.sleep(1)
        self.driver.find_element(By.ID, "acknowledgeButton").click()
        time.sleep(3)

        # Find and click the "Login" link in the navbar
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Login")))
        self.driver.find_element(By.LINK_TEXT, "Login").click()
        time.sleep(2)

        username = "1"
        password = "1"

        # Log in with right credentials
        self.driver.find_element(By.NAME, "username").send_keys(username)
        self.driver.find_element(By.NAME, "password").send_keys(password)
        time.sleep(2)
        self.driver.find_element(By.CLASS_NAME, "sub-button").click()
        time.sleep(2)
        self.assertEqual(self.driver.current_url, "http://127.0.0.1:5000/") 

         # Enter a message in the input field and submit it
        input_field = self.driver.find_element(By.CSS_SELECTOR, ".input")
        input_field.send_keys("Hello, StockBot!")
        self.driver.find_element(By.CSS_SELECTOR, ".input-form button[type=submit]").click()
        time.sleep(3)

        # Verify that the message is displayed in the chat window
        chat_window = self.driver.find_element(By.CSS_SELECTOR, ".chat-window")
        message = chat_window.find_element(By.XPATH, ".//div[contains(@class, 'message')]")
        self.assertEqual(message.text, "Hello, StockBot!\nINFO: The input format was invalid.")

        # Press the "cross" button to start a new chat
        self.driver.find_element(By.ID, "new-chat-button").click()
        time.sleep(2)

        # Verify that the previous message is not present on the screen
        chat_window = self.driver.find_element(By.CSS_SELECTOR, ".chat-window")
        message = chat_window.find_element(By.XPATH, ".//div[contains(@class, 'message')]")
        self.assertEqual(message.text, "")

    def test_login_logout(self):
        # Click the acknowledge button
        self.driver.find_element(By.ID, "dontShowAgainCheckbox").click()
        time.sleep(1)
        self.driver.find_element(By.ID, "acknowledgeButton").click()
        time.sleep(3)

        # Find and click the "Login" link in the navbar
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Login")))
        self.driver.find_element(By.LINK_TEXT, "Login").click()
        time.sleep(2)

        # Verify that the current URL is the Login page
        self.assertEqual(self.driver.current_url, "http://127.0.0.1:5000/login")  
        username = "1"
        password = "1"

        # Fill out the login form
        self.driver.find_element(By.NAME, "username").send_keys(username)
        self.driver.find_element(By.NAME, "password").send_keys(password)
        time.sleep(2)
        self.driver.find_element(By.CLASS_NAME, "sub-button").click()
        time.sleep(2)

        # Verify that the user is redirected to the home page
        home_url = self.base_url 
        self.assertEqual(self.driver.current_url, home_url)
        self.assertFalse(self.is_element_present(By.LINK_TEXT, "Login"))


        # Perform logout
        self.driver.find_element(By.LINK_TEXT, "Logout").click()
        time.sleep(2)

        # Verify that the user is redirected to the login page
        login_url = self.base_url
        self.assertEqual(self.driver.current_url, login_url)
        self.assertFalse(self.is_element_present(By.LINK_TEXT, "Logout"))

    def is_element_present(self, by, locator):
        try:
            self.driver.find_element(by, locator)
            return True
        except NoSuchElementException:
            return False

    def test_messages(self):
        # Click the acknowledge button
        self.driver.find_element(By.ID, "dontShowAgainCheckbox").click()
        time.sleep(1)
        self.driver.find_element(By.ID, "acknowledgeButton").click()
        time.sleep(3)

        # Find and click the "Login" link in the navbar
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Login")))
        self.driver.find_element(By.LINK_TEXT, "Login").click()
        time.sleep(2)

        username = "1"
        password = "1"

        # Log in with right credentials
        self.driver.find_element(By.NAME, "username").send_keys(username)
        self.driver.find_element(By.NAME, "password").send_keys(password)
        time.sleep(2)
        self.driver.find_element(By.CLASS_NAME, "sub-button").click()
        time.sleep(2)

         # Enter a message in the input field and submit it
        input_field = self.driver.find_element(By.CSS_SELECTOR, ".input")
        input_field.send_keys("info:aapl")
        self.driver.find_element(By.CSS_SELECTOR, ".input-form button[type=submit]").click()
        time.sleep(3)

        input_field = self.driver.find_element(By.CSS_SELECTOR, ".input")
        input_field.send_keys("price,current:tsla")
        self.driver.find_element(By.CSS_SELECTOR, ".input-form button[type=submit]").click()
        time.sleep(3)

        input_field = self.driver.find_element(By.CSS_SELECTOR, ".input")
        input_field.send_keys("price,lastyear:v")
        self.driver.find_element(By.CSS_SELECTOR, ".input-form button[type=submit]").click()
        time.sleep(3)

        # Verify that bot replied with info
        chat_window = self.driver.find_element(By.CSS_SELECTOR, ".chat-window")
        message = chat_window.find_element(By.XPATH, ".//div[contains(@class, 'message')]")
        self.assertFalse(any("INFO: The input format was invalid." in line for line in message.text.split("\n")))
    
    def test_search(self):
        # Click the acknowledge button
        self.driver.find_element(By.ID, "dontShowAgainCheckbox").click()
        time.sleep(1)
        self.driver.find_element(By.ID, "acknowledgeButton").click()
        time.sleep(3)

        # Find and click the "Login" link in the navbar
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Login")))
        self.driver.find_element(By.LINK_TEXT, "Login").click()
        time.sleep(2)

        username = "1"
        password = "1"

        # Log in with right credentials
        self.driver.find_element(By.NAME, "username").send_keys(username)
        self.driver.find_element(By.NAME, "password").send_keys(password)
        time.sleep(2)
        self.driver.find_element(By.CLASS_NAME, "sub-button").click()
        time.sleep(2)

        # Find and click the "History" link in the navbar
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "History")))
        self.driver.find_element(By.LINK_TEXT, "History").click()
        time.sleep(2)

        # Enter "aapl" in the search input
        search_input = self.driver.find_element(By.CSS_SELECTOR, "#search-bar input")
        search_input.send_keys("aapl")
        time.sleep(2)

        # Get the search results
        search_results = self.driver.find_elements(By.CSS_SELECTOR, "#search-results .search-result")

        # Check if sent messages are found
        self.assertTrue(len(search_results) > 0)

        # Enter "aapl" in the search input
        search_input = self.driver.find_element(By.CSS_SELECTOR, "#search-bar input")
        search_input.send_keys("a")
        time.sleep(2)

        # Get the search results
        search_results = self.driver.find_elements(By.CSS_SELECTOR, "#search-results .search-result")

        # Check if "aapla" not in the DB are not in history
        self.assertTrue(len(search_results) == 0)

    def tearDown(self):
        self.driver.quit()
        
if __name__ == "__main__":
    unittest.main()