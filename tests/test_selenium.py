import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class FleboVetTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.base_url = "http://127.0.0.1:8000"
        self.wait = WebDriverWait(self.driver, 10)

    def test_lista_deseos(self):
        """Prueba la funcionalidad de la lista de deseos"""
        try:
            self.driver.get(f"{self.base_url}/productos/")
            print("\n=== Prueba de Lista de Deseos ===")

            # Primero verificamos si hay que hacer login
            login_icon = self.wait.until(
                EC.element_to_be_clickable((By.CLASS_NAME, "nav-icon"))
            )
            login_icon.click()
            print("✓ Acceso a login")

            # Verificar botones de lista de deseos
            wishlist_buttons = self.wait.until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "btn-wishlist"))
            )
            if wishlist_buttons:
                print(f"✓ {len(wishlist_buttons)} botones de lista de deseos encontrados")

                # Intentar añadir a lista de deseos
                wishlist_buttons[0].click()
                print("✓ Click en botón de lista de deseos realizado")

        except Exception as e:
            print(f"✕ Error en lista de deseos: {str(e)}")
            raise

    def test_detalle_producto(self):
        """Prueba la vista de detalle de producto"""
        try:
            self.driver.get(f"{self.base_url}/productos/")
            print("\n=== Prueba de Detalle de Producto ===")

            # Encontrar y hacer clic en el primer botón "Ver Detalles"
            ver_detalles = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "btn-ver"))
            )
            nombre_producto = self.driver.find_element(
                By.CLASS_NAME, "product-content"
            ).find_element(By.TAG_NAME, "h2").text
            print(f"✓ Producto encontrado: {nombre_producto}")

            ver_detalles.click()
            print("✓ Click en Ver Detalles realizado")

            # Verificar página de detalle
            detalle_titulo = self.wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "h1"))
            )
            print(f"✓ Página de detalle cargada para: {detalle_titulo.text}")

        except Exception as e:
            print(f"✕ Error en detalle de producto: {str(e)}")
            raise

    def test_formulario_contacto(self):
        """Prueba el formulario de contacto"""
        try:
            self.driver.get(f"{self.base_url}/contacto/")
            print("\n=== Prueba de Formulario de Contacto ===")

            # Datos de prueba
            datos_prueba = {
                'nombre': 'Usuario Prueba',
                'email': 'prueba@ejemplo.com',
                'mensaje': 'Este es un mensaje de prueba automatizada.'
            }

            # Rellenar formulario
            for campo, valor in datos_prueba.items():
                input_field = self.wait.until(
                    EC.presence_of_element_located((By.NAME, campo))
                )
                input_field.clear()
                input_field.send_keys(valor)
                print(f"✓ Campo {campo} completado")

            # Buscar el botón de envío
            submit_button = self.driver.find_element(
                By.CSS_SELECTOR, "button[type='submit']"
            )
            print("✓ Botón de envío encontrado")

        except Exception as e:
            print(f"✕ Error en formulario de contacto: {str(e)}")
            raise

    def tearDown(self):
        if hasattr(self, 'driver'):
            self.driver.quit()

if __name__ == "__main__":
    unittest.main(verbosity=2)
