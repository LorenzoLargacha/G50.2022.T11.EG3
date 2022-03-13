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

    def test_request_vaccination_id_ok(self):
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

        # Abrimos el fichero
        with open(file_store, "r", encoding="UTF-8", newline="") as file:
            # Guardamos los datos del fichero en una lista
            data_list = json.load(file)

        # Creamos una variable para guardar si se encuentra un paciente con esos datos
        found = False
        # Recorremos las entradas de fichero
        for item in data_list:
            # Si el patient_id se encuentra en el fichero
            if item["_VaccinePatientRegister__patient_id"] == \
                    paciente['patient_id']:
                # Comprobamos el tipo de registro, el nombre, el numero de telefono y la edad
                if (item["_VaccinePatientRegister__registration_type"] ==
                    paciente['registration_type']) \
                        and (item["_VaccinePatientRegister__full_name"] ==
                             paciente['name']) \
                        and (item["_VaccinePatientRegister__phone_number"] ==
                             paciente['phone_number']) \
                        and (item["_VaccinePatientRegister__age"] ==
                             paciente['age']):
                    found = True

        # Comprobamos si el resultado es el esperado
        self.assertTrue(found)



if __name__ == '__main__':
    unittest.main()
