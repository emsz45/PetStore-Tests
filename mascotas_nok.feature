@petstore
Feature: Gestión de mascotas

  Scenario: Crear y buscar mascotas
    Given que abro la página principal
    When accedo a la gestión de mascotas
    And cargo las mascotas
    And añado una mascota llamada "Eva" con estado "available"
    And añado una mascota llamada "Laura" con estado "pending"
    And añado una mascota llamada "Estefania" con estado "sold"
    And busco la mascota "Laura"
    And limpio el buscador
    And busco la mascota "Estefania"
    And busco la mascota por ID "333"
    And vuelvo a inicio
    And pincho en gestión de pedidos
    And creo un pedido con ID "1" con ID mascota "333" con estado "Pendiente"
    And busco pedido con ID "1" y cambio estado a "Aprobado"
    And elimino pedido con ID "1"
    And the current page should be audited for accessibility
    Then cierro la aplicación