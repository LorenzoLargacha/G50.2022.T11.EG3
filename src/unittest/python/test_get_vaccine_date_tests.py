"""Modulos"""
import os
import json
from pathlib import Path
import unittest
from freezegun import freeze_time

from uc3m_care import VaccineManager
# from uc3m_care import VaccinationAppoinment
from uc3m_care import VaccineManagementException


class MyTestCase(unittest.TestCase):
    """ Test Unitest Get Vaccine Date """

    @freeze_time("2022-03-03 09:46:23.846215")
    def test_get_vaccine_date_ok(self):
        """ Tests ok """
        # Buscamos la ruta en la que se almacena el fichero store_patient
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T11.EG3/src/JsonFiles/RF1"
        file_store_patient = json_files_path + "/store_patient.json"

        # Buscamos la ruta en la que se almacena el fichero de test
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T11.EG3/src/JsonFiles/RF2"
        input_file = json_files_path + "/test_ok.json"

        # Buscamos la ruta en la que se almacena el fichero store_date
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T11.EG3/src/JsonFiles/RF2"
        file_store_date = json_files_path + "/store_date.json"

        # Si el fichero ya existe, lo borramos para no tener datos precargados
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        # Guardamos los atributos en las variables correspondientes
        patient_id = "bb5dbd6f-d8b4-413f-8eb9-dd262cfc54e0"
        registration_type = "Regular"
        name = "NomTreintacaracteres yunblanco"
        phone_number = "+34123456789"
        age = "6"
        alg = "SHA-256"
        typ = "DS"

        # Seleccionamos la clase sobre la que se ejecuta el test
        my_request = VaccineManager()

        # Llamamos al metodo request_vaccination_id para almacenar el paciente
        patient_system_id = my_request.request_vaccination_id(patient_id, registration_type,
                                                              name, phone_number, age)

        # Llamamos al metodo get_vaccine_date
        value = my_request.get_vaccine_date(input_file)

        # Comprobamos si el resultado es el esperado
        self.assertEqual("0b47c03009ee76e2c4ce33be4e37e6fb5b913f372a0be70c071f3042025d0987", value)

        # Comprobamos que se guarda la cita en store_date
        try:
            # Intentamos abrir el fichero JSON
            with open(file_store_date, "r", encoding="UTF-8", newline="") as file:
                # Guardamos los datos del fichero en una lista
                data_list = json.load(file)
        except FileNotFoundError as ex:
            # En caso de que el fichero no exista, lanzamos una excepcion
            raise VaccineManagementException("Fichero no creado") from ex
        except json.JSONDecodeError as ex:
            # Si se produce un error al decodificar mostaramos una excepcion
            raise VaccineManagementException(
                "JSON decode error - formato JSON incorrecto") from ex

        # Creamos una variable para guardar si se encuentra un paciente con esos datos
        found = False

        # Recorremos las entradas de fichero
        for item in data_list:
            # Si se han guardado todos los atributos de la cita
            if (item["_VaccinationAppoinment__alg"] == alg) \
                    and (item["_VaccinationAppoinment__type"] == typ) \
                    and (item["_VaccinationAppoinment__patient_id"] == patient_id) \
                    and (item["_VaccinationAppoinment__patient_sys_id"] == patient_system_id) \
                    and (item["_VaccinationAppoinment__phone_number"] == phone_number) \
                    and ("_VaccinationAppoinment__issued_at" in item) \
                    and ("_VaccinationAppoinment__appoinment_date" in item):
                found = True

        # Comprobamos si el resultado es el esperado
        self.assertTrue(found)

        # Mostramos el test que se esta ejecutando
        print("test_ok")


if __name__ == '__main__':
    unittest.main()
