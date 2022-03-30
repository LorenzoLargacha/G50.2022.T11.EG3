"""Modulos"""
import os
import json
from pathlib import Path
import unittest
from freezegun import freeze_time

from uc3m_care import VaccineManager
from uc3m_care import VaccineManagementException


class MyTestCase(unittest.TestCase):
    """ Test Unitest Request Vaccination Id """

    @freeze_time("2022-03-03 09:46:23.846215")
    def test_parametrized_valid_request_vaccination_id(self):
        """ Test 1,2,17,19. Tests validos de la funcion request_vaccination_id (parametrizados) """
        # Buscamos la ruta en la que se almacena el fichero
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T11.EG3/src/JsonFiles/RF1"
        file_store = json_files_path + "/store_patient.json"

        # Seleccionamos la clase sobre la que se ejecuta el test
        my_request = VaccineManager()

        # Cargamos los parametros de la lista
        for par1, par2, par3, par4, par5, par6, par7 in param_list_ok:
            with self.subTest():
                # Si el fichero ya existe, lo borramos para no tener datos precargados
                if os.path.isfile(file_store):
                    os.remove(file_store)

                # Guardamos los atributos en las variables correspondientes
                patient_id = par1
                registration_type = par2
                name = par3
                phone_number = par4
                age = par5

                # Llamamos al metodo request_vaccination_id
                value = my_request.request_vaccination_id(patient_id, registration_type,
                                                          name, phone_number, age)
                # Comprobamos si el resultado es el esperado
                self.assertEqual(par6, value)

                # Llamamos al metodo validate_json_data
                found = self.validate_json_data(file_store, patient_id,
                                                registration_type, name, phone_number, age)
                # Comprobamos si el resultado es el esperado
                self.assertTrue(found)

                # Mostramos el test que se esta ejecutando
                print(par7)

    def test_parametrized_not_valid_request_vaccination_id(self):
        """ Test 3-16. Tests no validos de la funcion request_vaccination_id (parametrizados) """
        # Buscamos la ruta en la que se almacena el fichero
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T11.EG3/src/JsonFiles/RF1"
        file_store = json_files_path + "/store_patient.json"

        # Si el fichero ya existe, lo borramos para no tener datos precargados
        if os.path.isfile(file_store):
            os.remove(file_store)

        # Seleccionamos la clase sobre la que se ejecuta el test
        my_request = VaccineManager()

        # Cargamos los parametros de la lista
        for par1, par2, par3, par4, par5, par6, par7 in param_list_nok:
            with self.subTest():
                # Guardamos los atributos en las variables correspondientes
                patient_id = par1
                registration_type = par2
                name = par3
                phone_number = par4
                age = par5

                # Llamamos al metodo request_vaccination_id
                with self.assertRaises(VaccineManagementException) as vme:
                    my_request.request_vaccination_id(patient_id,
                                                      registration_type, name, phone_number, age)
                # Confirmamos que se lanza la excepcion esperada
                self.assertEqual(vme.exception.message, par6)

                # Llamamos al metodo validate_json_data
                with self.assertRaises(VaccineManagementException) as vme:
                    self.validate_json_data(file_store, patient_id,
                                            registration_type, name, phone_number, age)
                # Comprobamos si el resultado es el esperado
                self.assertEqual("Fichero no creado", vme.exception.message)

                # Mostramos el test que se esta ejecutando
                print(par7)

    def test_22_validate_json_data_nok(self):
        """ Test no valido de la funcion validate_json_data,
        los datos no son válidos y no se guardan en el fichero """
        # Buscamos la ruta en la que se almacena el fichero
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T11.EG3/src/JsonFiles/RF1"
        file_store = json_files_path + "/store_patient.json"

        # Si el fichero ya existe, lo borramos para no tener datos precargados
        if os.path.isfile(file_store):
            os.remove(file_store)

        # Seleccionamos la clase sobre la que se ejecuta el test
        my_request = VaccineManager()

        # Guardamos los atributos de un paciente para tener datos precargados
        patient_id = "bb5dbd6f-d8b4-413f-8eb9-dd262cfc54e0"
        registration_type = "Regular"
        name = "Carmen Carrero"
        phone_number = "+34123456789"
        age = "22"

        # Llamamos al metodo request_vaccination_id para que se guarden los datos en el fichero
        my_request.request_vaccination_id(patient_id, registration_type, name, phone_number, age)

        # Guardamos los atributos de un paciente con datos incorrectos
        patient_id = "bb5dbd6f-d8b4-113f-8eb9-dd262cfc54e0"
        registration_type = "Regular"
        name = "Juan Martínez"
        phone_number = "+34666666666"
        age = "37"

        # Llamamos al metodo request_vaccination_id
        with self.assertRaises(VaccineManagementException) as vme:
            my_request.request_vaccination_id(patient_id,
                                              registration_type, name, phone_number, age)
        # Comprobamos si el resultado es el esperado
        self.assertEqual("Formato del UUID invalido", vme.exception.message)

        # Llamamos al metodo validate_json_data
        found = self.validate_json_data(file_store, patient_id,
                                        registration_type, name, phone_number, age)
        # Comprobamos si el resultado es el esperado
        self.assertFalse(found)

        # Mostramos el test que se esta ejecutando
        print("test_22")

    def test_23_validate_json_data_nok(self):
        """ Test no valido de la funcion validate_json_data,
        los datos son válidos y no se guardan en el fichero porque ya estan guardados """
        # Buscamos la ruta en la que se almacena el fichero
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T11.EG3/src/JsonFiles/RF1"
        file_store = json_files_path + "/store_patient.json"

        # Si el fichero ya existe, lo borramos para no tener datos precargados
        if os.path.isfile(file_store):
            os.remove(file_store)

        # Seleccionamos la clase sobre la que se ejecuta el test
        my_request = VaccineManager()

        # Guardamos los atributos de un paciente para tener datos precargados
        patient_id = "bb5dbd6f-d8b4-413f-8eb9-dd262cfc54e0"
        registration_type = "Regular"
        name = "Carmen Carrero"
        phone_number = "+34123456789"
        age = "22"

        # Llamamos al metodo request_vaccination_id para que se guarden los datos en el fichero
        my_request.request_vaccination_id(patient_id,
                                          registration_type, name, phone_number, age)

        # Llamamos al metodo request_vaccination_id de nuevo
        with self.assertRaises(VaccineManagementException) as vme:
            my_request.request_vaccination_id(patient_id,
                                              registration_type, name, phone_number, age)
        # Comprobamos si el resultado es el esperado
        self.assertEqual("Paciente ya registrado", vme.exception.message)

        # Llamamos al metodo validate_json_data
        found = self.validate_json_data(file_store, patient_id,
                                        registration_type, name, phone_number, age)
        # Comprobamos si el resultado es el esperado (ya estaba guardado)
        self.assertTrue(found)

        # Mostramos el test que se esta ejecutando
        print("test_23")

    @staticmethod
    def validate_json_data(file_store, patient_id, registration_type, name, phone_number, age):
        """ Metodo para comprobar si un paciente esta en el fichero Json """
        # Return True si paciente se encuentra en el fichero, False en otro caso
        try:
            # Intentamos abrir el fichero JSON para leer
            with open(file_store, "r", encoding="UTF-8", newline="") as file:
                # Guardamos los datos del fichero en una lista
                data_list = json.load(file)
        except FileNotFoundError as ex:
            # En caso de que el fichero no exista, lanzamos una excepcion
            raise VaccineManagementException("Fichero no creado") from ex
        except json.JSONDecodeError as ex:
            # Si se produce un error al decodificar mostramos una excepcion
            raise VaccineManagementException(
                "JSON decode error - formato JSON incorrecto") from ex

        # Creamos una variable para guardar si se encuentra un paciente con esos datos
        found = False

        # Recorremos las entradas de fichero
        for item in data_list:
            # Si el patient_id se encuentra en el fichero
            if item["_VaccinePatientRegister__patient_id"] == \
                    patient_id:
                # Comprobamos el tipo de registro, el nombre, el numero de telefono y la edad
                if (item["_VaccinePatientRegister__registration_type"] == registration_type) \
                        and (item["_VaccinePatientRegister__full_name"] == name) \
                        and (item["_VaccinePatientRegister__phone_number"] == phone_number) \
                        and (item["_VaccinePatientRegister__age"] == age):
                    found = True
        return found


# Parámetros para los test valid request_vaccination_id
param_list_ok = [("bb5dbd6f-d8b4-413f-8eb9-dd262cfc54e0",
                  "Regular", "NomTreintacaracteres yunblanco", "+34123456789", "6",
                  "0a9d6f313a6355f54caf4cd00a21f2d1", "test_1"),
                 ("bb5dbd6f-d8b4-413f-8eb9-dd262cfc54e0",
                  "Family", "Nombre Veintinueve Caracteres", "+34123456789", "125",
                  "44f07ba85efec0a3429b8d732f3c6284", "test_2"),
                 ("bb5dbd6f-d8b4-413f-8eb9-dd262cfc54e0",
                  "Family", "C C", "+34123456789", "7",
                  "61fabb7e13e3bb7008e9f247fc982417", "test_17"),
                 ("bb5dbd6f-d8b4-413f-8eb9-dd262cfc54e0",
                  "Family", "Carmen Carrero", "+34123456789", "124",
                  "a1c63840bbf5cf066a2c09d05173595a", "test_19")]

# Parámetros para los test not valid request_vaccination_id
param_list_nok = [("bb5dbd6f-d8b4-113f-8eb9-dd262cfc54e0",
                   "Regular", "Carmen Carrero", "+34123456789", "22",
                   "Formato del UUID invalido", "test_3"),
                  ("bb5dbd6f-d8b4-213f-8eb9-dd262cfc54e0",
                   "Regular", "Carmen Carrero", "+34123456789", "22",
                   "Formato del UUID invalido", "test_4"),
                  ("bb5dbd6f-d8b4-313f-8eb9-dd262cfc54e0",
                   "Regular", "Carmen Carrero", "+34123456789", "22",
                   "Formato del UUID invalido", "test_5"),
                  ("bb5dbd6f-d8b4-513f-8eb9-dd262cfc54e0",
                   "Regular", "Carmen Carrero", "+34123456789", "22",
                   "Formato del UUID invalido", "test_6"),
                  ("zb5dbd6f-d8b4-413f-8eb9-dd262cfc54e0",
                   "Regular", "Carmen Carrero", "+34123456789", "22",
                   "El Id recibido no es un UUID", "test_7"),
                  ("zb5dbd6f-d8b4-413f-8eb9-dd262cfc54e01",
                   "Family", "Carmen Carrero", "+34123456789", "22",
                   "El Id recibido no es un UUID", "test_8"),
                  ("zb5dbd6f-d8b4-413f-8eb9-dd262cfc54e",
                   "Family", "Carmen Carrero", "+34123456789", "22",
                   "El Id recibido no es un UUID", "test_9"),
                  ("bb5dbd6f-d8b4-413f-8eb9-dd262cfc54e0",
                   "Single", "Carmen Carrero", "+34123456789", "22",
                   "Tipo de vacunacion solicitada incorrecta", "test_10"),
                  ("bb5dbd6f-d8b4-413f-8eb9-dd262cfc54e0",
                   "Regular", "C", "+34123456789", "22",
                   "Cadena sin separacion entre nombre y apellidos", "test_11"),
                  ("bb5dbd6f-d8b4-413f-8eb9-dd262cfc54e0",
                   "Regular", "Nombre Con Treintayuncaracteres", "+34123456789", "22",
                   "Cadena de nombre y apellidos mayor de 30 caracteres", "test_12"),
                  ("bb5dbd6f-d8b4-413f-8eb9-dd262cfc54e0",
                   "Regular", "", "+34123456789", "22",
                   "Cadena de nombre vacia", "test_13"),
                  ("bb5dbd6f-d8b4-413f-8eb9-dd262cfc54e0",
                   "Regular", "Carmen Carrero", "+3412345678", "22",
                   "Formato del telefono invalido", "test_14"),
                  ("bb5dbd6f-d8b4-413f-8eb9-dd262cfc54e0",
                   "Regular", "Carmen Carrero", "+341234567899", "22",
                   "Formato del telefono invalido", "test_15"),
                  ("bb5dbd6f-d8b4-413f-8eb9-dd262cfc54e0",
                   "Regular", "Carmen Carrero", "teléfono", "22",
                   "Formato del telefono invalido", "test_16"),
                  ("bb5dbd6f-d8b4-413f-8eb9-dd262cfc54e0",
                   "Regular", "Carmen Carrero", "+34123456789", "5",
                   "Edad menor de 6 años", "test_18"),
                  ("bb5dbd6f-d8b4-413f-8eb9-dd262cfc54e0",
                   "Regular", "Carmen Carrero", "+34123456789", "126",
                   "Edad mayor de 125 años", "test_20"),
                  ("bb5dbd6f-d8b4-413f-8eb9-dd262cfc54e0",
                   "Regular", "Carmen Carrero", "+34123456789", "diez",
                   "La edad no es un numero", "test_21")]


if __name__ == '__main__':
    unittest.main()
