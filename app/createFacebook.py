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

createfacebook = Blueprint('createfacebook', __name__)

chrome_options = Options()
chrome_options.add_argument("--headless")  # Ejecución sin interfaz gráfica
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = None
login_result = None  # Variable global para almacenar el resultado del inicio de sesión

@createfacebook.route('/api/create', methods=['POST'])
def login():
    global driver, login_result
    # Obtener las credenciales del cuerpo de la solicitud POST
    data = request.get_json()
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    email = data.get('email')
    sexo = data.get('sexo')
    contrasena = data.get('contrasena')

    # Configurar el controlador del navegador (Chrome en este ejemplo)

    driver_service = Service(executable_path='webdriver//chromedriver.exe')
    driver = webdriver.Chrome(service=driver_service)
    # options=chrome_options

    try:
        # Abrir la página de inicio de sesión de Facebook
        driver.get("https://m.facebook.com/reg/?soft=hjk")

        # # Rellenar el formulario de inicio de sesión
        time.sleep(2)
        driver.find_element(By.XPATH,'//*[@id="firstname_input"]').send_keys(nombre, Keys.TAB)
        driver.find_element(By.XPATH,'//*[@id="lastname_input"]').send_keys(apellido, Keys.ENTER)
        driver.find_element(By.XPATH, '//*[@id="mobile-reg-form"]/div[9]/div[2]/button[1]').click()
        # email_field = driver.find_element(By.ID,"//*[@id='firstname_input']").send_keys(email, Keys.ENTER)

        #Ingreso de edad
        time.sleep(2)
        driver.find_element(By.XPATH, '//*[@id="year"]/option[24]').click()
        driver.find_element(By.XPATH, '//*[@id="mobile-reg-form"]/div[9]/div[2]/button[1]').click()
        # Esperar a que se cargue la página
        
        #Ingreso de correo electronico
        time.sleep(2)
        driver.find_element(By.XPATH, '//*[@id="contactpoint_step_input"]').send_keys(email, Keys.ENTER)
        driver.find_element(By.XPATH, '//*[@id="mobile-reg-form"]/div[9]/div[2]/button[1]').click()

        time.sleep(2)
        if sexo == "Mujer":
            driver.find_element(By.XPATH, '//*[@id="Mujer"]').click()
        else:
            driver.find_element(By.XPATH, '//*[@id="Hombre"]').click()

        driver.find_element(By.XPATH, '//*[@id="mobile-reg-form"]/div[9]/div[2]/button[1]').click()

        #Ingreso correo electronico
        driver.find_element(By.XPATH, '//*[@id="password_step_input"]').send_keys(contrasena, Keys.ENTER)
        driver.find_element(By.XPATH, '//*[@id="mobile-reg-form"]/div[9]/div[2]/button[4]').click()

        #error si se ingresa un dato mal //*[@id="registration-error"]

        # Esperar a que se cargue la página
        driver.implicitly_wait(10)

        driver.find_element(By.XPATH, '//*[@id="root"]/div[1]/div/div/div[3]/div[2]/form/div/button').click()

        #se coloca el codigo del correo
        driver.find_element(By.XPATH, '//*[@id="m_conf_cliff_root_id"]/div/div/form/div/input').send_keys(contrasena, Keys.ENTER)

        #Agregar Foto


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
    