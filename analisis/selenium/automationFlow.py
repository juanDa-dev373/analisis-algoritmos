import logging
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from abc import ABC, abstractmethod

logging.basicConfig(level=logging.INFO)

#Clase para la configuración del WebDriver
class WebDriverConfig:
    def __init__(self):
        PATH_DRIVER = 'C:/Users/david/Desktop/UNI/Programas/chromedriver-win64/chromedriver.exe'
        
        # Configurar opciones del navegador
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--start-maximized')
        self.options.add_argument('--disable-extensions')
        self.service = Service(PATH_DRIVER)
        
        # Inicializar el WebDriver
        self.driver = webdriver.Chrome(service=self.service, options=self.options)

    # def __init__(self, opcion):
    #     PATH_DRIVER = 'C:/Users/david/Desktop/UNI/Programas/chromedriver-win64/chromedriver.exe'
    #     self.options= opcion
    #     self.options = webdriver.ChromeOptions()
    #     self.options.add_argument('--start-maximized')
    #     self.options.add_argument('--disable-extensions')
    #     self.options.add_argument('--disable-features=CookiesWithoutSameSiteMustBeSecure')
    #     self.options.add_argument("--allow-running-insecure-content")  # Permite contenido inseguro
    #     self.options.add_argument("--ignore-certificate-errors")  # Ignora errores de certificados
    #     self.options.add_argument("--disable-blink-features=AutomationControlled")  
    #     self.options.add_argument("--incognito")
    #     self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
    #     self.options.add_experimental_option("useAutomationExtension", False)
    #     # Definir el servicio con el path correcto
    #     self.service = Service(PATH_DRIVER)
        
    #     # Inicializar el WebDriver
    #     self.driver = webdriver.Chrome(service=self.service, options=self.options)

    def get_driver(self):
        return self.driver

#Interfaz para interacciones con Selenium
class WebDriverActions(ABC):
    @abstractmethod
    def wait_and_click(self, selector: str, by=By.CSS_SELECTOR, timeout=10):
        pass

    @abstractmethod
    def wait_and_send_keys(self, selector: str, text: str, by=By.CSS_SELECTOR, timeout=10):
        pass

    @abstractmethod
    def move_to_element(self, selector: str, by=By.CSS_SELECTOR):
        pass

#Interfaz para definir estrategias de búsqueda
class SearchStrategy(ABC):
    @abstractmethod
    def search(self, query: str):
        pass

#Estrategia para la descarga de documentos desde un proxy
class SeleniumHelper:
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver
        self.actions = ActionChains(driver)

    def wait_and_click(self, selector: str, by=By.CSS_SELECTOR, timeout=10):
        """ Espera a que el elemento sea clickeable y lo presiona. """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, selector))
            )
            element.click()
        except (TimeoutException, NoSuchElementException):
            logging.warning(f"No se pudo hacer clic en: {selector}")

    def wait_and_send_keys(self, selector: str, text: str, by=By.CSS_SELECTOR, timeout=10):
        """ Espera a que el elemento esté presente y escribe texto en él. """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, selector))
            )
            element.send_keys(text)
        except (TimeoutException, NoSuchElementException):
            logging.warning(f"No se pudo escribir en: {selector}")

    def move_to_element(self, selector: str, by=By.CSS_SELECTOR):
        """ Mueve el cursor al elemento especificado. """
        try:
            element = WebDriverWait(self.driver, 10).until(  # Agregamos un tiempo de espera
                EC.presence_of_element_located((by, selector))
            )
            self.actions.move_to_element(element).perform()
        except TimeoutException:
            logging.warning(f"Tiempo de espera agotado al buscar el elemento: {selector}")
        except NoSuchElementException:
            logging.warning(f"No se encontró el elemento para mover el cursor: {selector}")

    def wait_for_window(self, timeout=2):
        """ Espera a que se abra una nueva ventana. """
        time.sleep(round(timeout / 1000))
        wh_now = self.driver.window_handles
        if hasattr(self, "window_handles"):
            wh_then = self.window_handles
            if len(wh_now) > len(wh_then):
                return set(wh_now).difference(set(wh_then)).pop()
        return None

# Estrategia de búsqueda en la biblioteca
class LibrarySearch:
    def __init__(self, driver: webdriver.Chrome, selenium_helper: SeleniumHelper):
        self.driver = driver
        self.helper = selenium_helper

    def search(self, link: str ,query: str):
        self.driver.get(link)

        self.helper.wait_and_send_keys("#edit-search-form-stacks-external-catalogs-customdescubridor-eds-search-bar-container-query", query)
        self.helper.wait_and_click("#edit-search-form-stacks-external-catalogs-customdescubridor-eds-search-bar-container-actions-submit")

        self.driver.get('https://login.intelproxy.com/v2/conector/google/solicitar?cuenta=7Ah6RNpGWF22jjyq&url=ezp.2aHR0cHM6Ly9zZWFyY2guZWJzY29ob3N0LmNvbS9sb2dpbi5hc3B4PyZkaXJlY3Q9dHJ1ZSZzaXRlPWVkcy1saXZlJmF1dGh0eXBlPWlwJmN1c3RpZD1uczAwNDM2MyZnZW9jdXN0aWQ9Jmdyb3VwaWQ9bWFpbiZwcm9maWxlPWVkcyZicXVlcnk9Y29tcHV0YXRpb25hbCt0aGlua2luZw--')


# Clase para descargar documentos
class LibraryDownload:
    def __init__(self, driver: webdriver.Chrome, selenium_helper: SeleniumHelper):
        self.driver = driver
        self.helper = selenium_helper

    def download(self, page_number: int):

        self.helper.wait_and_click(".osano-cm-button--type_accept", By.CSS_SELECTOR)

        self.put_filter()
        time.sleep(5)
        self.set_total_result()

        self.helper.move_to_element("//span/label/input",By.XPATH)
        self.helper.wait_and_click("//span/label/input", By.XPATH)

        self.helper.wait_and_click("//section/div/div/div/div/div/div", By.XPATH)
        self.modal_download()
        self.helper.move_to_element("//span/label/input",By.XPATH)
        self.helper.wait_and_click("//span/label/input", By.XPATH)

        if page_number >= 2:
            for i in range(2, page_number + 1):
                self.download_page_results(i)

    def modal_download(self):
        self.helper.wait_and_click(".fa-download", By.CSS_SELECTOR)
        self.helper.wait_and_click(".eb-control:nth-child(2) .eb-control__input", By.CSS_SELECTOR)
        self.helper.wait_and_click(".nuc-bulk-download-modal-footer__button:nth-child(2)", By.CSS_SELECTOR)
        self.helper.wait_and_click(".nuc-bulk-download-modal__close-button", By.CSS_SELECTOR)

    def put_filter(self):
        self.helper.wait_and_click(".all-filters-button_all-filters-button__2x61O > span", By.CSS_SELECTOR)
        self.helper.wait_and_click(".facet_facet__item__VfFUI:nth-child(2) span:nth-child(1)", By.CSS_SELECTOR)
        self.helper.wait_and_click(".facet-attribute_facet-attribute__0Sjol:nth-child(1) .eb-control__input", By.CSS_SELECTOR)
        self.helper.wait_and_click("//div[3]/button[2]", By.XPATH)

    def set_total_result(self):
        self.helper.wait_and_click(".results-per-page-dropdown-toggle_results-per-page-dropdown-toggle__label__3e_nO", By.CSS_SELECTOR)
        self.helper.wait_and_click("#results-per-page-dropdown-item-3 > .eb-dropdown__item-label", By.CSS_SELECTOR)

    def download_page_results(self, page_number: int = 1):
        """Navega hasta la página especificada y descarga los resultados."""
        pagination_button = "//div/div[3]/button"
        checkbox_id = f"result-list-page-{page_number}-checkbox"

        self.helper.move_to_element(pagination_button, By.XPATH)
        self.helper.wait_and_click(pagination_button, By.XPATH)

        self.helper.move_to_element(checkbox_id, By.ID)
        self.helper.wait_and_click(checkbox_id, By.ID)

        self.helper.move_to_element("li:nth-child(2) > .eb-tool-button > .eb-button", By.CSS_SELECTOR)
        self.modal_download()
        self.helper.wait_and_click("//div[@id='results-page']/div/section/div/div/div/div/div/div/span/label/input", By.XPATH)


# Clase para descargar documentos
class ScienceDirectDownload:
    def __init__(self, driver: webdriver.Chrome, selenium_helper: SeleniumHelper):
        self.driver = driver
        self.vars= {}
        self.helper = selenium_helper

    def download(self, page_number: int):
        """ Descarga artículos de ScienceDirect """
        self.driver.get('https://www-sciencedirect-com.crai.referencistas.com/search?qs=%22computational%20thinking%22&show=100')
        self.driver.get("https://login.intelproxy.com/v2/conector/google/solicitar?cuenta=7Ah6RNpGWF22jjyq&url=ezp.2aHR0cHM6Ly93d3cuc2NpZW5jZWRpcmVjdC5jb20vc2VhcmNoP3FzPSUyMmNvbXB1dGF0aW9uYWwlMjB0aGlua2luZyUyMiZzaG93PTEwMA--")
        self.modal_download()
        time.sleep(5)
        if page_number >= 2:
            for i in range(2, page_number + 1):
                self.driver.get(f'https://www-sciencedirect-com.crai.referencistas.com/search?qs=%22computational%20thinking%22&show=100&offset={i-1}00')
                self.modal_download()

    def modal_download(self):
        self.helper.wait_and_click(".SelectAllCheckbox .checkbox-check")
        self.helper.wait_and_click(".export-all-link-text")
        self.vars["window_handles"] = self.driver.window_handles
        self.helper.wait_and_click(".button-link:nth-child(5) .button-link-text")

        new_window = self.helper.wait_for_window(2000)
        if new_window:
            self.driver.switch_to.window(new_window)
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])

class AcmDownload:
    def __init__(self, driver: webdriver.Chrome, selenium_helper: SeleniumHelper):
        self.driver = driver
        self.helper = selenium_helper

    def download(self):
        driver.get("https://dl.acm.org")
        time.sleep(5)
        
        self.driver.get('https://dl.acm.org/action/doSearch?AllField=%22computational+thinking%22')
        time.sleep(5)
        self.helper.wait_and_click("#CybotCookiebotDialogBodyButtonDecline")
        time.sleep(5)
        self.helper.wait_and_click("js--selected", By.CLASS_NAME)
        time.sleep(20)
        self.helper.wait_and_click(".item-results__checkbox")
        time.sleep(5)
        self.helper.wait_and_click("//span[contains(.,'Export Citations')]", By.XPATH)
        time.sleep(40)
        self.helper.wait_and_click("//span[contains(.,'All Results')]",By.XPATH)
        time.sleep(10)
        self.helper.wait_and_click("//form/ul/li/div/a",By.XPATH)
        time.sleep(120)
        self.helper.wait_and_click(".searchCiteExport-popup__close")

class IEEEDownload:

    def __init__(self, driver: webdriver.Chrome, selenium_helper: SeleniumHelper):
        self.driver = driver
        self.helper = selenium_helper

    def download(self, page_number: int = 1):
        self.driver.get(f'https://ieeexplore-ieee-org.crai.referencistas.com/search/searchresult.jsp?newsearch=true&queryText=%22computational%20thinking%22&highlight=true&returnFacets=ALL&returnType=SEARCH&matchPubs=true&rowsPerPage=100&pageNumber=1')
        self.driver.get("https://login.intelproxy.com/v2/conector/google/solicitar?cuenta=7Ah6RNpGWF22jjyq&url=ezp.2aHR0cHM6Ly9pZWVleHBsb3JlLmllZWUub3JnL3NlYXJjaC9zZWFyY2hyZXN1bHQuanNwP25ld3NlYXJjaD10cnVlJnF1ZXJ5VGV4dD0lMjJjb21wdXRhdGlvbmFsJTIwdGhpbmtpbmclMjImaGlnaGxpZ2h0PXRydWUmcmV0dXJuRmFjZXRzPUFMTCZyZXR1cm5UeXBlPVNFQVJDSCZtYXRjaFB1YnM9dHJ1ZSZyb3dzUGVyUGFnZT0xMDAmcGFnZU51bWJlcj0x")
        self.helper.wait_and_click(".osano-cm-button--type_save")
        for i in range(1, page_number + 1):
            time.sleep(3)
            self.driver.get(f'https://ieeexplore-ieee-org.crai.referencistas.com/search/searchresult.jsp?newsearch=true&queryText=%22computational%20thinking%22&highlight=true&returnFacets=ALL&returnType=SEARCH&matchPubs=true&rowsPerPage=100&pageNumber={i}')
            self.modal_download()

    def modal_download(self):
        self.helper.wait_and_click(".results-actions-selectall-checkbox")
        self.helper.wait_and_click("xpl-export-search-results > .xpl-btn-primary")
        self.helper.wait_and_click("#ngb-nav-0")
        self.helper.wait_and_click(".col-12:nth-child(1) .d-flex:nth-child(2) > .ng-untouched")
        self.helper.wait_and_click("//section[2]/div/label[2]/input", By.XPATH)
        time.sleep(3)
        self.helper.wait_and_click(".stats-SearchResults_Citation_Download")
        time.sleep(5)
        self.helper.wait_and_click("//ngb-modal-window/div/div/div/div/i", By.XPATH)

# Clase para manejar el inicio de sesión en Google
class GoogleLogin:
    def __init__(self, driver: webdriver.Chrome, selenium_helper: SeleniumHelper):
        self.driver = driver
        self.helper = selenium_helper

    def login(self, email: str, password: str):
        """Realiza el inicio de sesión en Google"""
        self.driver.get('https://accounts.google.com/')

        # Ingresar correo
        self.helper.wait_and_send_keys('input[type="email"]', email)
        self.helper.wait_and_click('#identifierNext')

        # Esperar y escribir contraseña
        self.helper.wait_and_send_keys('input[name="Passwd"]', password, timeout=15)
        self.helper.wait_and_click('#passwordNext')

        print("Inicio de sesión en Google completado.")

#Clase principal que ejecuta el flujo completo
class AutomationFlow:
    def __init__(self, search_strategy: SearchStrategy, 
                 acm_download: AcmDownload, 
                 science_download: ScienceDirectDownload, 
                 ieee_download: IEEEDownload, 
                 google_login: GoogleLogin):
        self.search_strategy = search_strategy
        self.acm_download = acm_download
        self.google_login = google_login
        self.science_download = science_download
        self.ieee_download = ieee_download

    def execute_acm(self):
        self.acm_download.download()

    def execute_science(self, email: str, password: str, number: int = 1):
        self.google_login.login(email, password)
        self.science_download.download(number)

    def execute_ieee(self, email: str, password: str, number: int = 1):
        self.google_login.login(email, password)
        self.ieee_download.download(number)

if __name__ == "__main__":
    EMAIL = os.getenv('EMAIL_GOOGLE')
    PASSWORD = os.getenv('PASSWORD_GOOGLE')

    # Inicialización de dependencias
    driver_config = WebDriverConfig()
    driver = driver_config.get_driver()
    selenium_helper = SeleniumHelper(driver)

    # driver_acm_config = WebDriverConfig(opcion=True)
    # driver_acm = driver_acm_config.get_driver()

    # Inyección de dependencias en las clases
    google_login = GoogleLogin(driver, selenium_helper)
    search_strategy = LibrarySearch(driver, selenium_helper)
    acm_download= AcmDownload(driver_config, selenium_helper) 
    science_download= ScienceDirectDownload(driver, selenium_helper)
    ieee_download= IEEEDownload(driver, selenium_helper)
    automation_flow = AutomationFlow(search_strategy, 
                                    acm_download,
                                    science_download,
                                    ieee_download,
                                    google_login)

    try:
        #Ejecutar la búsqueda y descarga con inicio de sesión en Google
        # automation_flow.execute_science(EMAIL, PASSWORD, 11)
        automation_flow.execute_ieee(EMAIL, PASSWORD, 11)
        # automation_flow.execute_acm()

    finally:
        time.sleep(10)
        driver.quit()
