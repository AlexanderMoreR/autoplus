from flask import Flask, request, Blueprint
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import json

loginfacebook = Blueprint('logingfacebook', __name__)

chrome_options = Options()
chrome_options.add_argument("--headless")  # Ejecución sin interfaz gráfica
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = None
login_result = None  # Variable global para almacenar el resultado del inicio de sesión

@loginfacebook.route('/api/login', methods=['POST'])
def login():
    global driver, login_result
    # Obtener las credenciales del cuerpo de la solicitud POST
    data = request.get_json() 
    email = data.get('email')

    # Configurar el controlador del navegador (Chrome en este ejemplo)

    driver_service = Service(executable_path='webdriver//chromedriver.exe')
    driver = webdriver.Chrome(service=driver_service)
    # options=chrome_options

    try:
        # Abrir la página de inicio de sesión de Facebook
        driver.get("https://m.facebook.com/login/identify/?")

        # # Rellenar el formulario de inicio de sesión
        email_field = driver.find_element(By.ID,"identify_search_text_input").send_keys(email, Keys.ENTER)

        # Esperar a que se cargue la página
        time.sleep(2)

        try:
            driver.find_element(By.XPATH, '//*[@id="contact_point_selector_form"]/div[4]/a').click()
        except Exception as e:
            print("Paso: No existe Otra manera 1.")
            pass
            
        try:
            driver.find_element(By.XPATH, '//*[@id="contact_point_selector_form"]/div[3]/a').click()
        except Exception as e:
            print("Paso: No existe Otra manera 2.")
            pass

        # Esperar a que se cargue la página
        driver.implicitly_wait(10)

        # Extraer el método para obtener el código de verificación usando BeautifulSoup
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        method_element = soup.find("form", id="contact_point_selector_form")  
        # Aquí necesitarías inspeccionar el elemento específico en la página para encontrar el método

        
        # Crear una lista para almacenar los textos de las etiquetas
        metodos = []

        if method_element:
            labels = method_element.find_all('label')
            inputs = method_element.find_all('input')[2:]

            for label, input_tag in zip(labels, inputs):
                if input_tag.get("value") == "send_email" or (input_tag.get("value").startswith("send_sms")):
                    text_parts = []
                    for div in label.find_all("div"):
                        text_parts.append(div.text.strip())
                    text = " : ".join(text_parts)
                    input_text = input_tag.get("value")
                    metodos.append({
                            "label": text,
                            "input": input_text
                    })

        # Almacenar el resultado en la variable global
        login_result = metodos
        
        # Devolver el resultado en formato JSON
        return json.dumps(login_result, ensure_ascii=False)
    
    except Exception as e:
        #driver.quit()
        return f'Error en el inicio de sesión: {str(e)}'
    
@loginfacebook.route('/api/login/metodo', methods=['POST'])
def other_method():
    global login_result, driver
    # Utilizar el resultado del inicio de sesión almacenado en la variable global

    data = request.get_json()
    input = data.get('input')

    if login_result is not None:
        # Resto del código para utilizar el resultado del inicio de sesión en el nuevo método
        value = login_result[input]['input']
        driver.find_element(By.XPATH, '//*[@value="'+value+'"]').click()
        # revisar que el boton aplique para todos los metodos
        driver.find_element(By.XPATH, '//*[@id="contact_point_selector_form"]/div[1]/button').click()
        return "Se envio el codigo correctamente: " + value + ". 1. Para continuar, Ingresa el codigo que llega al correo y Acepta la sesion desde el ultimo dispositivo donde ingresastes a facebook."
    else:
        return "El resultado del inicio de sesión no está disponible."

@loginfacebook.route('/api/login/code', methods=['POST'])
def code():
    global login_result, driver
    # Utilizar el resultado del inicio de sesión almacenado en la variable global

    data = request.get_json()
    code = data.get('code')
    newpass = data.get('newpass')
    

    if driver is not None:
        # Resto del código para utilizar el resultado del inicio de sesión en el nuevo método
        driver.find_element(By.XPATH, '//*[@data-sigil="code-input"]').send_keys(code, Keys.ENTER)
        # revisar que el boton aplique para todos los metodos
        driver.find_element(By.XPATH, '//*[@name="password_new"]').send_keys(newpass, Keys.ENTER)
        
        
        try:
            driver.implicitly_wait(10)
            driver.find_element(By.XPATH, '//*[@id="m_check_list_aria_label"]/input').click()
            driver.find_element(By.XPATH, '//*[@id="checkpointSubmitButton-actual-button"]').click()
            # Esperar a que se cargue la página
            driver.implicitly_wait(10)

            # revisar que el boton aplique para todos los metodos
            driver.find_element(By.XPATH, '//*[@id="checkpointSubmitButton-actual-button"]').click()
            driver.find_element(By.XPATH, '//*[@id="checkpointSubmitButton-actual-button').click()
        except Exception as e:
            print("No hubo GEOLOCALIZACION 1")
            pass
            
        try:
            driver.implicitly_wait(10)
            driver.find_element(By.XPATH, '//*[@id="checkpointSubmitButton-actual-button"]').click()
            # Esperar a que se cargue la página
            driver.implicitly_wait(10)

            # revisar que el boton aplique para todos los metodos
            driver.find_element(By.XPATH, '//*[@id="m_check_list_aria_label"]/input').click()
            driver.find_element(By.XPATH, '//*[@id="checkpointSubmitButton-actual-button').click()
        except Exception as e:
            print("No hubo GEOLOCALIZACION 2")
            pass

        try:
            driver.implicitly_wait(10)
            driver.find_element(By.XPATH, '//*[@id="checkpointSubmitButton-actual-button"]').click()
            # Esperar a que se cargue la página
            driver.implicitly_wait(10)

            # revisar que el boton aplique para todos los metodos
            driver.find_element(By.XPATH, '//*[@id="m_check_list_aria_label"]/input').click()
            driver.find_element(By.XPATH, '//*[@id="checkpointSubmitButton-actual-button').click()
        except Exception as e:
            print("No hubo GEOLOCALIZACION 3")
            pass

        try:
            driver.find_element(By.XPATH, '//*[@id="nux-nav-button"]').click()
        except:
            print("Cuenta nueva de Facebook")
            pass
        
        try:
            print("entro")
            element_present = EC.presence_of_element_located((By.XPATH, '//*[@id="viewport"]/h1'))
            WebDriverWait(driver, 140).until(element_present)
            #driver.quit()
            return """
            Sincronización con Exito. 
            1. Puede continuar en Star-BOT"
            """
            
        except:
            #driver.quit()
            return "Sincronizacion no Exitosa!, Intenta de nuevo en el 1.1."


        
    else:
        return "El resultado del inicio de sesión no está disponible."