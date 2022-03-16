"""Modulos"""
import os
import json
from pathlib import Path
import unittest

from datetime import datetime
from uc3m_care import VaccineManager
from uc3m_care import VaccineManagementException

from freezegun import freeze_time


class MyTestCase(unittest.TestCase):

    """def test_something( self ):
        #self.assertEqual(True, False)
        self.assertEqual(True, True)"""

    def test_1_request_vaccination_id_ok(self):
        """Test valido de la funcion request_vaccination_id"""
        # Buscamos la ruta en la que se almacena el fichero
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T11.EG3/src/JsonFiles"
        file_store = json_files_path + "/store_patient.json"

        # Si el fichero ya existe, lo borramos para no tener datos precargados
        if os.path.isfile(file_store):
            os.remove(file_store)

        # Seleccionamos la clase sobre la que se ejecuta el test
        my_request = VaccineManager()

        # Guardamos los atributos en un diccionario
        paciente = {}
        paciente['patient_id'] = "bb5dbd6f-d8b4-413f-8eb9-dd262cfc54e0"
        paciente['registration_type'] = "Regular"
        paciente['name'] = "Carmen Carrero"
        paciente['phone_number'] = "123456789"
        paciente['age'] = "22"

        # Llamamos al metodo request_vaccination_id
        value = my_request.request_vaccination_id(paciente)
        # Comprobamos si el resultado es el esperado
        self.assertEqual("3467d3fbe384b32f2629074e7db3dd91", value)

        # Llamamos al metodo validate_json_data
        found = my_request.validate_json_data(file_store, paciente)
        # Comprobamos si el resultado es el esperado
        self.assertTrue(found)

    def test_2_request_vaccination_id_ok(self):
        """Test valido de la funcion request_vaccination_id"""
        # Buscamos la ruta en la que se almacena el fichero
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T11.EG3/src/JsonFiles"
        file_store = json_files_path + "/store_patient.json"

        # Si el fichero ya existe, lo borramos para no tener datos precargados
        if os.path.isfile(file_store):
            os.remove(file_store)

        # Seleccionamos la clase sobre la que se ejecuta el test
        my_request = VaccineManager()

        # Guardamos los atributos en un diccionario
        paciente = {}
        paciente['patient_id'] = "bb5dbd6f-d8b4-413f-8eb9-dd262cfc54e0"
        paciente['registration_type'] = "Family"
        paciente['name'] = "Carmen Carrero"
        paciente['phone_number'] = "123456789"
        paciente['age'] = "22"

        # Llamamos al metodo request_vaccination_id
        value = my_request.request_vaccination_id(paciente)
        # Comprobamos si el resultado es el esperado
        self.assertEqual("b7f631c7c29d52a20b965b5ca7ab6c24", value)

        # Llamamos al metodo validate_json_data
        found = my_request.validate_json_data(file_store, paciente)
        # Comprobamos si el resultado es el esperado
        self.assertTrue(found)

    def test_3_request_vaccination_id_nok_uuid(self):
        """Test no valido de la funcion request_vaccination_id, uuid no valido (version 1)"""
        # Buscamos la ruta en la que se almacena el fichero
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T11.EG3/src/JsonFiles"
        file_store = json_files_path + "/store_patient.json"

        # Si el fichero ya existe, lo borramos para no tener datos precargados
        if os.path.isfile(file_store):
            os.remove(file_store)

        # Seleccionamos la clase sobre la que se ejecuta el test
        my_request = VaccineManager()

        # Guardamos los atributos en un diccionario
        paciente = {}
        paciente['patient_id'] = "bb5dbd6f-d8b4-113f-8eb9-dd262cfc54e0"
        paciente['registration_type'] = "Family"
        paciente['name'] = "Carmen Carrero"
        paciente['phone_number'] = "123456789"
        paciente['age'] = "22"

        # Llamamos al metodo request_vaccination_id
        with self.assertRaises(VaccineManagementException) as cm:
            value = my_request.request_vaccination_id(paciente)

        # Comprobamos si el resultado es el esperado
        self.assertEqual("Formato del UUID invalido", cm.exception.message)

        # Llamamos al metodo validate_json_data
        with self.assertRaises(VaccineManagementException) as cm:
            found = my_request.validate_json_data(file_store, paciente)

        # Comprobamos si el resultado es el esperado
        self.assertEqual("Fichero no creado", cm.exception.message)

    def test_parametrized_NOT_valid_request_vaccination_id(self):
        """Test no valido de la funcion request_vaccination_id, uuid no valido (version 1)"""
        # Buscamos la ruta en la que se almacena el fichero
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T11.EG3/src/JsonFiles"
        file_store = json_files_path + "/store_patient.json"

        # Si el fichero ya existe, lo borramos para no tener datos precargados
        if os.path.isfile(file_store):
            os.remove(file_store)

        # Seleccionamos la clase sobre la que se ejecuta el test
        my_request = VaccineManager()

        for p1, p2, p3, p4, p5, p6, p7 in param_list_nok:
            # Guardamos los atributos en un diccionario
            paciente = {}
            paciente['patient_id'] = p1
            paciente['registration_type'] = p2
            paciente['name'] = p3
            paciente['phone_number'] = p4
            paciente['age'] = p5

            with self.subTest():
                with self.assertRaises(VaccineManagementException) as cm:
                    value = my_request.request_vaccination_id(paciente)
                self.assertEqual(cm.exception.message, p6)
                print(p7)

            # Llamamos al metodo validate_json_data
            with self.assertRaises(VaccineManagementException) as cm:
                found = my_request.validate_json_data(file_store, paciente)

            # Comprobamos si el resultado es el esperado
            self.assertEqual("Fichero no creado", cm.exception.message)


param_list_nok = [("bb5dbd6f-d8b4-113f-8eb9-dd262cfc54e0",
                   "Regular", "Carmen Carrero", "123456789", "22", "Formato del UUID invalido", "test_3"),
                  ("bb5dbd6f-d8b4-213f-8eb9-dd262cfc54e0",
                   "Regular", "Carmen Carrero", "123456789", "22", "Formato del UUID invalido", "test_4"),
                  ("bb5dbd6f-d8b4-313f-8eb9-dd262cfc54e0",
                   "Regular", "Carmen Carrero", "123456789", "22", "Formato del UUID invalido", "test_5"),
                  ("bb5dbd6f-d8b4-513f-8eb9-dd262cfc54e0",
                   "Regular", "Carmen Carrero", "123456789", "22", "Formato del UUID invalido", "test_6"),
                  ("zb5dbd6f-d8b4-413f-8eb9-dd262cfc54e0",
                   "Regular", "Carmen Carrero", "123456789", "22", "Formato del UUID invalido", "test_7"),
                  ("bb5dbd6f-d8b4-413f-8eb9-dd262cfc54e0",
                   "Single", "Carmen Carrero", "123456789", "22", "Tipo de vacunacion solicitada incorrecta", "test_8"),
                  ("bb5dbd6f-d8b4-413f-8eb9-dd262cfc54e0",
                   "Regular", "Carmen", "123456789", "22", "Cadena sin separacion entre nombre y apellidos", "test_9"),
                  ("bb5dbd6f-d8b4-413f-8eb9-dd262cfc54e0",
                   "Regular", "Carmen Carrero Rodríguez Fernández Martínez", "123456789", "22",
                   "Cadena de nombre y apellidos mayor de 30 caracteres", "test_10"),
                  ("bb5dbd6f-d8b4-413f-8eb9-dd262cfc54e0",
                   "Regular", "Carmen Carrero", "12345678", "22",
                   "Telefono con menos de 9 digitos", "test_11"),
                  ("bb5dbd6f-d8b4-413f-8eb9-dd262cfc54e0",
                   "Regular", "Carmen Carrero", "1234567899", "22",
                   "Telefono con mas de 9 digitos", "test_12"),



                  ]

if __name__ == '__main__':
    unittest.main()
