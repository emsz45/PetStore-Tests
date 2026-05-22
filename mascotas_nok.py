from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from behave import given, when, then
import time


# =========================
# GIVEN
# =========================

@given("que abro la página principal")
def abrir_pagina_principal(context):
    context.wait = WebDriverWait(context.driver, 10)
    context.driver.get("http://127.0.0.1:5500/index.html")


# =========================
# WHEN
# =========================

@when("accedo a la gestión de mascotas")
def acceder_gestion_mascotas(context):
    enlace_mascotas = context.wait.until(
        EC.element_to_be_clickable(
            (By.LINK_TEXT, "Gestión de Mascotas")
        )
    )
    enlace_mascotas.click()


@when("cargo las mascotas")
def cargar_mascotas(context):
    boton = context.wait.until(
        EC.element_to_be_clickable((By.ID, "btnLoad"))
    )
    boton.click()
    time.sleep(2)


@when('añado una mascota llamada "{nombre}" con estado "{estado}"')
def crear_mascota(context, nombre, estado):
    nombre_input = context.wait.until(
        EC.visibility_of_element_located((By.ID, "petName"))
    )
    nombre_input.clear()
    nombre_input.send_keys(nombre)

    select_estado = Select(
        context.driver.find_element(By.ID, "petStatus")
    )
    select_estado.select_by_value(estado)

    context.driver.find_element(
        By.CSS_SELECTOR, "#formCreate button[type='submit']"
    ).click()

    time.sleep(2)


@when('busco la mascota "{nombre}"')
def buscar_mascota(context, nombre):
    buscador = context.wait.until(
        EC.visibility_of_element_located((By.ID, "searchInput"))
    )
    buscador.clear()
    buscador.send_keys(nombre)

    boton_buscar = context.wait.until(
        EC.element_to_be_clickable((By.ID, "btnSearch"))
    )

@when('busco la mascota por ID "{id_mascota}"')
def buscar_mascota_por_id(context, id_mascota):

    buscador = context.wait.until(
        EC.visibility_of_element_located((By.ID, "searchInput"))
    )
    buscador.clear()
    buscador.send_keys(id_mascota)

    boton_buscar = context.wait.until(
        EC.presence_of_element_located((By.ID, "btnSearch"))
    )

    # Scroll para evitar problemas de viewport
    context.driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});",
        boton_buscar
    )

    context.wait.until(
        EC.element_to_be_clickable((By.ID, "btnSearch"))
    )

    boton_buscar.click()


@when("limpio el buscador")
def limpiar_buscador(context):
    buscador = context.driver.find_element(By.ID, "searchInput")
    buscador.clear()

@when("vuelvo a gestión de mascotas")
def volver_a_gestion_mascotas(context):

    boton_mascotas = context.wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'a[href="pets.html"]')
        )
    )

    # 🔑 Forzar scroll real hasta el centro de la pantalla
    context.driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});",
        boton_mascotas
    )

    # 🔑 Esperar a que sea realmente clickable
    context.wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'a[href="pets.html"]')
        )
    )
    time.sleep(0.3)  # micro-pausa para estabilidad
    boton_mascotas.click()


@when("vuelvo a inicio")
def volver_a_inicio(context):
    # Navegación directa para evitar bloqueo del navegador
    context.driver.get("http://127.0.0.1:5500/index.html")


@when("pincho en gestión de pedidos")
def click_gestion_pedidos(context):
    # 🚨 Navegación directa para evitar bloqueo por validación HTML
    context.driver.get("http://127.0.0.1:5500/store.html")

@when('creo un pedido con ID "{id}" con ID mascota "{id_pet}" con estado "{estado}"')
def crear_pedidos(context, id, id_pet, estado):
    input_pedido = context.wait.until(
        EC.visibility_of_element_located((By.ID, "orderId"))
    )
    input_pedido.clear()
    input_pedido.send_keys(id)

    input_mascota = context.wait.until(
        EC.visibility_of_element_located((By.ID, "orderPetId"))
    )
    input_mascota.clear()
    input_mascota.send_keys(id_pet)

    select_estado = Select(
        context.driver.find_element(By.ID, "orderStatus")
    )
    select_estado.select_by_visible_text(estado)
    boton_crear = context.driver.find_element(By.CSS_SELECTOR, "#formCreateOrder button")
    boton_crear.click()
    alert = context.wait.until(EC.alert_is_present())
    alert.accept()

    time.sleep(2)

@when('busco pedido con ID "{id}" y cambio estado a "{nuevo_estado}"')
def buscar_pedido(context, id, nuevo_estado):

    # Introducir ID del pedido
    input_buscar = context.wait.until(
        EC.visibility_of_element_located((By.ID, "searchOrderId"))
    )
    input_buscar.clear()
    input_buscar.send_keys(id)

    boton_buscar = context.wait.until(
        EC.presence_of_element_located((By.ID, "btnSearchOrder"))
    )

    # 🔑 SCROLL PARA EVITAR CLICK INTERCEPTED
    context.driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});",
        boton_buscar
    )

    context.wait.until(
        EC.element_to_be_clickable((By.ID, "btnSearchOrder"))
    )

    time.sleep(0.3)
    boton_buscar.click()

    # Aceptar alert tras buscar (si aparece)
    try:
        alert = context.wait.until(EC.alert_is_present())
        alert.accept()
    except:
        pass

    # Cambiar estado
    select_edit_estado = context.wait.until(
        EC.visibility_of_element_located((By.ID, "editStatus"))
    )
    Select(select_edit_estado).select_by_visible_text(nuevo_estado)

    boton_guardar = context.wait.until(
        EC.presence_of_element_located((By.ID, "btnUpdateOrder"))
    )

    context.driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});",
        boton_guardar
    )

    context.wait.until(
        EC.element_to_be_clickable((By.ID, "btnUpdateOrder"))
    )

    time.sleep(0.3)
    boton_guardar.click()

    # Alert tras guardar
    alert = context.wait.until(EC.alert_is_present())
    alert.accept()

    time.sleep(1)

@when('elimino pedido con ID "{id}"')
def eliminar_pedido(context, id):

    input_eliminar = context.wait.until(
        EC.visibility_of_element_located((By.ID, "deleteOrderId"))
    )
    input_eliminar.clear()
    input_eliminar.send_keys(id)

    boton_eliminar = context.driver.find_element(By.ID, "btnDeleteOrder")
    boton_eliminar.click()

    time.sleep(2)
# =========================
# THEN
# =========================

@then("cierro la aplicación")
def cerrar_aplicacion(context):
    time.sleep(3)