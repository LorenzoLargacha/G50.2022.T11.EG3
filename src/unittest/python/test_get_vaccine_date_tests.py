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

    @freeze_time("2022-03-08")
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

        # Seleccionamos la clase sobre la que se ejecuta el test
        my_request = VaccineManager()

        # Llamamos al metodo request_vaccination_id para almacenar el paciente
        patient_system_id = my_request.request_vaccination_id("bb5dbd6f-d8b4-413f-8eb9-dd262cfc54e0", "Regular",
                                                              "NomTreintacaracteres yunblanco", "+34123456789", "6")

        # Llamamos al metodo get_vaccine_date
        value = my_request.get_vaccine_date(input_file)

        # Comprobamos si el resultado es el esperado
        self.assertEqual("56f606edfa8914e43ab92ea40e0ccdd7d888d381c4c175cf5172f9b8e4de5e3e", value)

        # Comprobamos que se guarda la cita en store_date


if __name__ == '__main__':
    unittest.main()
