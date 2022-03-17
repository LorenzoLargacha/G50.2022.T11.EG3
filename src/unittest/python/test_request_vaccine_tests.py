"""Modulos"""
import os
import json
from pathlib import Path
import unittest

from uc3m_care import VaccineManager
from uc3m_care import VaccineManagementException


class MyTestCase(unittest.TestCase):

    def test_parametrized_valid_request_vaccination_id(self):
        """Tests validos de la funcion request_vaccination_id (parametrizados)"""
        # Buscamos la ruta en la que se almacena el fichero
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T11.EG3/src/JsonFiles/RF1"
        file_store = json_files_path + "/store_patient.json"

        # Si el fichero ya existe, lo borramos para no tener datos precargados
        if os.path.isfile(file_store):
            os.remove(file_store)

        # Seleccionamos la clase sobre la que se ejecuta el test
        my_request = VaccineManager()

        # Cargamos los parametros de la lista
        for p1, p2, p3, p4, p5, p6, p7 in param_list_ok:
            # Guardamos los atributos en un diccionario
            # Utilizamos un diccionario para reducir el numero de argumentos (pylint)
            paciente = {}
            paciente['patient_id'] = p1
            paciente['registration_type'] = p2
            paciente['name'] = p3
            paciente['phone_number'] = p4
            paciente['age'] = p5

            # Llamamos al metodo request_vaccination_id
            value = my_request.request_vaccination_id(paciente)
            # Comprobamos si el resultado es el esperado
            self.assertEqual(p6, value)

            # Llamamos al metodo validate_json_data
            found = my_request.validate_json_data(file_store, paciente)
            # Comprobamos si el resultado es el esperado
            self.assertTrue(found)

            # Mostramos el test que se esta ejecutando
            print(p7)

    def test_parametrized_not_valid_request_vaccination_id(self):
        """Tests no validos de la funcion request_vaccination_id (parametrizados)"""
        # Buscamos la ruta en la que se almacena el fichero
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T11.EG3/src/JsonFiles/RF1"
        file_store = json_files_path + "/store_patient.json"

        # Si el fichero ya existe, lo borramos para no tener datos precargados
        if os.path.isfile(file_store):
            os.remove(file_store)

        # Seleccionamos la clase sobre la que se ejecuta el test
        my_request = VaccineManager()

        # Cargamos los parametros de la lista
        for p1, p2, p3, p4, p5, p6, p7 in param_list_nok:
            # Guardamos los atributos en un diccionario
            paciente = {}
            paciente['patient_id'] = p1
            paciente['registration_type'] = p2
            paciente['name'] = p3
            paciente['phone_number'] = p4
            paciente['age'] = p5

            # Llamamos al metodo request_vaccination_id
            with self.subTest():
                with self.assertRaises(VaccineManagementException) as cm:
                    my_request.request_vaccination_id(paciente)
                # Confirmamos que se lanza la excepcion esperada
                self.assertEqual(cm.exception.message, p6)

            # Llamamos al metodo validate_json_data
            with self.assertRaises(VaccineManagementException) as cm:
                my_request.validate_json_data(file_store, paciente)
            # Comprobamos si el resultado es el esperado
            self.assertEqual("Fichero no creado", cm.exception.message)

            # Mostramos el test que se esta ejecutando
            print(p7)

    def test_17_validate_json_data_nok(self):
        """Test no valido de la funcion validate_json_data,
        los datos no son válidos y no se guardan en el fichero"""

        # Buscamos la ruta en la que se almacena el fichero
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T11.EG3/src/JsonFiles/RF1"
        file_store = json_files_path + "/store_patient.json"

        # Si el fichero ya existe, lo borramos para no tener datos precargados
        if os.path.isfile(file_store):
            os.remove(file_store)

        # Seleccionamos la clase sobre la que se ejecuta el test
        my_request = VaccineManager()

        # Guardamos los atributos de un paciente para tener datos precargados
        paciente = {}
        paciente['patient_id'] = "bb5dbd6f-d8b4-413f-8eb9-dd262cfc54e0"
        paciente['registration_type'] = "Regular"
        paciente['name'] = "Carmen Carrero"
        paciente['phone_number'] = "123456789"
        paciente['age'] = "22"

        # Llamamos al metodo request_vaccination_id para que se guarden los datos en el fichero
        my_request.request_vaccination_id(paciente)

        # Guardamos los atributos de un paciente con datos incorrectos
        paciente = {}
        paciente['patient_id'] = "bb5dbd6f-d8b4-113f-8eb9-dd262cfc54e0"
        paciente['registration_type'] = "Regular"
        paciente['name'] = "Juan Martínez"
        paciente['phone_number'] = "666666666"
        paciente['age'] = "37"

        # Llamamos al metodo request_vaccination_id
        with self.assertRaises(VaccineManagementException) as cm:
            value = my_request.request_vaccination_id(paciente)
        # Comprobamos si el resultado es el esperado
        self.assertEqual("Formato del UUID invalido", cm.exception.message)

        # Llamamos al metodo validate_json_data
        found = my_request.validate_json_data(file_store, paciente)
        # Comprobamos si el resultado es el esperado
        self.assertFalse(found)

        # Mostramos el test que se esta ejecutando
        print("test_17")

    def test_18_validate_json_data_nok(self):
        """Test no valido de la funcion validate_json_data,
        los datos son válidos y no se guardan en el fichero porque ya estan guardados"""
        # Buscamos la ruta en la que se almacena el fichero
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T11.EG3/src/JsonFiles/RF1"
        file_store = json_files_path + "/store_patient.json"

        # Si el fichero ya existe, lo borramos para no tener datos precargados
        if os.path.isfile(file_store):
            os.remove(file_store)

        # Seleccionamos la clase sobre la que se ejecuta el test
        my_request = VaccineManager()

        # Guardamos los atributos de un paciente para tener datos precargados
        paciente = {}
        paciente['patient_id'] = "bb5dbd6f-d8b4-413f-8eb9-dd262cfc54e0"
        paciente['registration_type'] = "Regular"
        paciente['name'] = "Carmen Carrero"
        paciente['phone_number'] = "123456789"
        paciente['age'] = "22"

        # Llamamos al metodo request_vaccination_id para que se guarden los datos en el fichero
        my_request.request_vaccination_id(paciente)

        # Llamamos al metodo request_vaccination_id de nuevo
        with self.assertRaises(VaccineManagementException) as cm:
            value = my_request.request_vaccination_id(paciente)
        # Comprobamos si el resultado es el esperado
        self.assertEqual("Paciente ya registrado", cm.exception.message)

        # Llamamos al metodo validate_json_data
        found = my_request.validate_json_data(file_store, paciente)
        # Comprobamos si el resultado es el esperado (ya estaba guardado)
        self.assertTrue(found)

        # Mostramos el test que se esta ejecutando
        print("test_18")


# Parametros para los test valid request vaccination id
param_list_ok = [("bb5dbd6f-d8b4-413f-8eb9-dd262cfc54e0",
                  "Regular", "Carmen Carrero", "123456789", "22",
                  "3467d3fbe384b32f2629074e7db3dd91", "test_1"),
                 ("bb5dbd6f-d8b4-413f-8eb9-dd262cfc54e0",
                  "Family", "Carmen Carrero", "123456789", "22",
                  "b7f631c7c29d52a20b965b5ca7ab6c24", "test_2")]

# Parametros para los test not valid request vaccination id
param_list_nok = [("bb5dbd6f-d8b4-113f-8eb9-dd262cfc54e0",
                   "Regular", "Carmen Carrero", "123456789", "22",
                   "Formato del UUID invalido", "test_3"),
                  ("bb5dbd6f-d8b4-213f-8eb9-dd262cfc54e0",
                   "Regular", "Carmen Carrero", "123456789", "22",
                   "Formato del UUID invalido", "test_4"),
                  ("bb5dbd6f-d8b4-313f-8eb9-dd262cfc54e0",
                   "Regular", "Carmen Carrero", "123456789", "22",
                   "Formato del UUID invalido", "test_5"),
                  ("bb5dbd6f-d8b4-513f-8eb9-dd262cfc54e0",
                   "Regular", "Carmen Carrero", "123456789", "22",
                   "Formato del UUID invalido", "test_6"),
                  ("zb5dbd6f-d8b4-413f-8eb9-dd262cfc54e0",
                   "Regular", "Carmen Carrero", "123456789", "22",
                   "El Id recibido no es un UUID", "test_7"),
                  ("bb5dbd6f-d8b4-413f-8eb9-dd262cfc54e0",
                   "Single", "Carmen Carrero", "123456789", "22",
                   "Tipo de vacunacion solicitada incorrecta", "test_8"),
                  ("bb5dbd6f-d8b4-413f-8eb9-dd262cfc54e0",
                   "Regular", "Carmen", "123456789", "22",
                   "Cadena sin separacion entre nombre y apellidos", "test_9"),
                  ("bb5dbd6f-d8b4-413f-8eb9-dd262cfc54e0",
                   "Regular", "Carmen Carrero Rodríguez Fernández Martínez", "123456789", "22",
                   "Cadena de nombre y apellidos mayor de 30 caracteres", "test_10"),
                  ("bb5dbd6f-d8b4-413f-8eb9-dd262cfc54e0",
                   "Regular", "Carmen Carrero", "12345678", "22",
                   "Telefono con menos de 9 digitos", "test_11"),
                  ("bb5dbd6f-d8b4-413f-8eb9-dd262cfc54e0",
                   "Regular", "Carmen Carrero", "1234567899", "22",
                   "Telefono con mas de 9 digitos", "test_12"),
                  ("bb5dbd6f-d8b4-413f-8eb9-dd262cfc54e0",
                   "Regular", "Carmen Carrero", "teléfono", "22",
                   "Telefono no es un numero", "test_13"),
                  ("bb5dbd6f-d8b4-413f-8eb9-dd262cfc54e0",
                   "Regular", "Carmen Carrero", "123456789", "5",
                   "Edad menor de 6 años", "test_14"),
                  ("bb5dbd6f-d8b4-413f-8eb9-dd262cfc54e0",
                   "Regular", "Carmen Carrero", "123456789", "126",
                   "Edad mayor de 125 años", "test_15"),
                  ("bb5dbd6f-d8b4-413f-8eb9-dd262cfc54e0",
                   "Regular", "Carmen Carrero", "123456789", "diez",
                   "La edad no es un numero", "test_16")]


if __name__ == '__main__':
    unittest.main()
