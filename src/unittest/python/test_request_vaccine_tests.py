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


if __name__ == '__main__':
    unittest.main()
