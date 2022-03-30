"""Modulos"""
import os
import json
from pathlib import Path
import unittest
import hashlib
from freezegun import freeze_time

from uc3m_care import VaccineManager
# from uc3m_care import VaccinationAppoinment
from uc3m_care import VaccineManagementException


class MyTestCase(unittest.TestCase):
    """ Test Unitest Vaccine Patient """

    @freeze_time("2022-03-03 09:46:23.846215")
    def setUp(self):
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
        my_request.request_vaccination_id("bb5dbd6f-d8b4-413f-8eb9-dd262cfc54e0", "Regular",
                                          "NomTreintacaracteres yunblanco", "+34123456789", "6")

        # Llamamos al metodo get_vaccine_date
        my_request.get_vaccine_date(input_file)

    @freeze_time("2022-03-13 09:46:23.846215")
    def test_1_vaccine_patient_ok(self):
        """ Test valido de la funcion vaccine_patient """
        # Buscamos la ruta en la que se almacena el fichero store_vaccine
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T11.EG3/src/JsonFiles/RF3"
        file_store_vaccine = json_files_path + "/store_vaccine.json"

        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Seleccionamos la clase sobre la que se ejecuta el test
        my_request = VaccineManager()

        # Creamos variable date_signature
        date_signature = "0b47c03009ee76e2c4ce33be4e37e6fb5b913f372a0be70c071f3042025d0987"

        # Llamamos al metodo vaccine_patient
        value = my_request.vaccine_patient(date_signature)

        # Comprobamos si el resultado es el esperado
        self.assertTrue(value)

        # Comprobamos que se guarda la cita en store_vaccine
        try:
            # Intentamos abrir el fichero JSON
            with open(file_store_vaccine, "r", encoding="UTF-8", newline="") as file:
                # Guardamos los datos del fichero en una lista
                data_list = json.load(file)
        except FileNotFoundError as ex:
            # En caso de que el fichero no exista, lanzamos una excepcion
            raise VaccineManagementException("Fichero no creado") from ex
        except json.JSONDecodeError as ex:
            # Si se produce un error al decodificar mostaramos una excepcion
            raise VaccineManagementException(
                "JSON decode error - formato JSON incorrecto") from ex

        # Creamos una variable para guardar si se encuentran los datos de vacunación del paciente
        found_1 = False
        found_2 = False

        # Recorremos las entradas de fichero
        for item in data_list:
            # Si se han guardado todos los datos de vacunación
            if date_signature == item:
                found_1 = True

            if "2022-03-13 09:46:23.846215" == item:
                found_2 = True

        # Comprobamos si el resultado es el esperado
        self.assertTrue(found_1)
        self.assertTrue(found_2)

        # Mostramos el test que se esta ejecutando
        print("test_1")

    @freeze_time("2022-03-13 09:46:23.846215")
    def test_2_no_store_date(self):
        """ Test no valido de la funcion vaccine_patient """

        # Buscamos la ruta en la que se almacena el fichero store_date
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T11.EG3/src/JsonFiles/RF2"
        file_store_date = json_files_path + "/store_date.json"

        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        # Buscamos la ruta en la que se almacena el fichero store_vaccine
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T11.EG3/src/JsonFiles/RF3"
        file_store_vaccine = json_files_path + "/store_vaccine.json"

        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Seleccionamos la clase sobre la que se ejecuta el test
        my_request = VaccineManager()

        # Creamos variable date_signature
        date_signature = "0b47c03009ee76e2c4ce33be4e37e6fb5b913f372a0be70c071f3042025d0987"

        # Llamamos al metodo vaccine_patient
        with self.assertRaises(VaccineManagementException) as vme:
            my_request.vaccine_patient(date_signature)

        # Confirmamos que se lanza la excepcion esperada
        self.assertEqual(vme.exception.message, "Fichero store_date no creado")

        # Comprobamos que el fichero store_vaccine no se crea
        self.assertFalse(os.path.isfile(file_store_vaccine))

        # Mostramos el test que se esta ejecutando
        print("test_2")

    @freeze_time("2022-03-13 09:46:23.846215")
    def test_3_store_date_incorrecto(self):
        """ Test no valido de la funcion vaccine_patient """

        # Buscamos la ruta en la que se almacena el fichero store_date
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T11.EG3/src/JsonFiles/RF2"
        file_store_date = json_files_path + "/store_date.json"

        # Modificamos el fichero para que sea del formato incorrecto
        try:
            # Intentamos abrir el fichero JSON para escribir
            with open(file_store_date, "w", encoding="UTF-8", newline="") as file:
                file.write(".")
        except FileNotFoundError as ex:
            # Si no existe el fichero lanzamos una excepcion
            raise VaccineManagementException(
                "JSON file not found error - fichero o ruta incorrectos") from ex

        # Buscamos la ruta en la que se almacena el fichero store_vaccine
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T11.EG3/src/JsonFiles/RF3"
        file_store_vaccine = json_files_path + "/store_vaccine.json"

        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Seleccionamos la clase sobre la que se ejecuta el test
        my_request = VaccineManager()

        # Creamos variable date_signature
        date_signature = "0b47c03009ee76e2c4ce33be4e37e6fb5b913f372a0be70c071f3042025d0987"

        # Llamamos al metodo vaccine_patient
        with self.assertRaises(VaccineManagementException) as vme:
            my_request.vaccine_patient(date_signature)

        # Confirmamos que se lanza la excepcion esperada
        self.assertEqual(vme.exception.message, "JSON decode error - formato JSON incorrecto")

        # Comprobamos que el fichero store_vaccine no se crea
        self.assertFalse(os.path.isfile(file_store_vaccine))

        # Mostramos el test que se esta ejecutando
        print("test_3")

    @freeze_time("2022-03-13 09:46:23.846215")
    def test_4_no_key(self):
        """ Test no valido de la funcion vaccine_patient """

        # Buscamos la ruta en la que se almacena el fichero store_vaccine
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T11.EG3/src/JsonFiles/RF3"
        file_store_vaccine = json_files_path + "/store_vaccine.json"

        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Seleccionamos la clase sobre la que se ejecuta el test
        my_request = VaccineManager()

        # Creamos variable date_signature para la que no hay ninguna cita
        date_signature = "0b47c03009ee76e2c4ce33be4e37e6fb5b913f372a0be70c071f3042025d0990"

        # Llamamos al metodo vaccine_patient
        with self.assertRaises(VaccineManagementException) as vme:
            my_request.vaccine_patient(date_signature)

        # Confirmamos que se lanza la excepcion esperada
        self.assertEqual(vme.exception.message, "Cita no registrada")

        # Comprobamos que el fichero store_vaccine no se crea
        self.assertFalse(os.path.isfile(file_store_vaccine))

        # Mostramos el test que se esta ejecutando
        print("test_4")

    @freeze_time("2022-03-13 09:46:23.846215")
    def test_5_store_date_vacio(self):
        """ Test no valido de la funcion vaccine_patient """

        # Buscamos la ruta en la que se almacena el fichero store_date
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T11.EG3/src/JsonFiles/RF2"
        file_store_date = json_files_path + "/store_date.json"

        # Modificamos el fichero para que este vacio
        try:
            # Intentamos abrir el fichero JSON para escribir
            with open(file_store_date, "w", encoding="UTF-8", newline="") as file:
                file.write("[]")
        except FileNotFoundError as ex:
            # Si no existe el fichero lanzamos una excepcion
            raise VaccineManagementException(
                "JSON file not found error - fichero o ruta incorrectos") from ex

        # Buscamos la ruta en la que se almacena el fichero store_vaccine
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T11.EG3/src/JsonFiles/RF3"
        file_store_vaccine = json_files_path + "/store_vaccine.json"

        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Seleccionamos la clase sobre la que se ejecuta el test
        my_request = VaccineManager()

        # Creamos variable date_signature
        date_signature = "0b47c03009ee76e2c4ce33be4e37e6fb5b913f372a0be70c071f3042025d0987"

        # Llamamos al metodo vaccine_patient
        with self.assertRaises(VaccineManagementException) as vme:
            my_request.vaccine_patient(date_signature)

        # Confirmamos que se lanza la excepcion esperada
        self.assertEqual(vme.exception.message, "Cita no registrada")

        # Comprobamos que el fichero store_vaccine no se crea
        self.assertFalse(os.path.isfile(file_store_vaccine))

        # Mostramos el test que se esta ejecutando
        print("test_5")

    @freeze_time("2022-03-12 09:46:23.846215")
    def test_6_not_today(self):
        """ Test no valido de la funcion vaccine_patient """

        # Buscamos la ruta en la que se almacena el fichero store_vaccine
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T11.EG3/src/JsonFiles/RF3"
        file_store_vaccine = json_files_path + "/store_vaccine.json"

        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Seleccionamos la clase sobre la que se ejecuta el test
        my_request = VaccineManager()

        # Creamos variable date_signature para la que no hay ninguna cita
        date_signature = "0b47c03009ee76e2c4ce33be4e37e6fb5b913f372a0be70c071f3042025d0987"

        # Llamamos al metodo vaccine_patient
        with self.assertRaises(VaccineManagementException) as vme:
            my_request.vaccine_patient(date_signature)

        # Confirmamos que se lanza la excepcion esperada
        self.assertEqual(vme.exception.message, "Cita no registrada para la fecha de hoy")

        # Comprobamos que el fichero store_vaccine no se crea
        self.assertFalse(os.path.isfile(file_store_vaccine))

        # Mostramos el test que se esta ejecutando
        print("test_6")

    @freeze_time("2022-03-03 09:46:23.846215")
    def setup_test_7(self):
        """ SetUp para tests 7 y 12 """
        json_files_path= str(Path.home()) + "/PycharmProjects/G50.2022.T11.EG3/src/JsonFiles/RF2"
        input_file = json_files_path + "/test_ok_7.json"

        # Seleccionamos la clase sobre la que se ejecuta el test
        my_request = VaccineManager()

        # Llamamos al metodo request_vaccination_id para almacenar el paciente
        my_request.request_vaccination_id("bb5dbd6f-d8b4-413f-8eb9-aa333dbd45c2", "Regular",
                                          "Juan Martinez", "+34666666666", "21")

        # Llamamos al metodo get_vaccine_date
        my_request.get_vaccine_date(input_file)

    @freeze_time("2022-03-13 09:46:23.846215")
    def test7_ok_store_vaccine_with_data(self):
        """ Test valido de la funcion vaccine_patient """
        # Buscamos la ruta en la que se almacena el fichero store_vaccine
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T11.EG3/src/JsonFiles/RF3"
        file_store_vaccine = json_files_path + "/store_vaccine.json"

        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        self.setup_test_7()

        # Seleccionamos la clase sobre la que se ejecuta el test
        my_request = VaccineManager()

        # Llamamos al metodo vaccine_patient para el nuevo paciente
        my_request.vaccine_patient(
            "c5bc7fff26b8d2d98da73ec90147294920d029b53516a0a5d57272b32f790f1c")

        # Creamos variable date_signature
        date_signature = \
            "0b47c03009ee76e2c4ce33be4e37e6fb5b913f372a0be70c071f3042025d0987"

        # Llamamos al metodo vaccine_patient
        value = my_request.vaccine_patient(date_signature)

        # Comprobamos si el resultado es el esperado
        self.assertTrue(value)

        # Comprobamos que se guarda la cita en store_vaccine
        try:
            # Intentamos abrir el fichero JSON
            with open(file_store_vaccine, "r", encoding="UTF-8", newline="") as file:
                # Guardamos los datos del fichero en una lista
                data_list = json.load(file)
        except FileNotFoundError as ex:
            # En caso de que el fichero no exista, lanzamos una excepcion
            raise VaccineManagementException("Fichero no creado") from ex
        except json.JSONDecodeError as ex:
            # Si se produce un error al decodificar mostaramos una excepcion
            raise VaccineManagementException(
                "JSON decode error - formato JSON incorrecto") from ex

        # Creamos una variable para guardar si se encuentran los datos de vacunación del paciente
        found_1 = False
        found_2 = False

        # Recorremos las entradas de fichero
        for item in data_list:
            # Si se han guardado todos los datos de vacunación
            if date_signature == item:
                found_1 = True

            if "2022-03-13 09:46:23.846215" == item:
                found_2 = True

        # Comprobamos si el resultado es el esperado
        self.assertTrue(found_1)
        self.assertTrue(found_2)

        # Mostramos el test que se esta ejecutando
        print("test_7")

    @freeze_time("2022-03-13 09:46:23.846215")
    def test_8_store_vaccine_incorrecto(self):
        """ Test no valido de la funcion vaccine_patient """
        # Buscamos la ruta en la que se almacena el fichero store_vaccine
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T11.EG3/src/JsonFiles/RF3"
        file_store_vaccine = json_files_path + "/store_vaccine.json"

        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Modificamos el fichero para que sea del formato incorrecto
        try:
            # Intentamos abrir el fichero JSON para escribir
            with open(file_store_vaccine, "w", encoding="UTF-8", newline="") as file:
                file.write(".")
        except FileNotFoundError as ex:
            # Si no existe el fichero lanzamos una excepcion
            raise VaccineManagementException(
                "JSON file not found error - fichero o ruta incorrectos") from ex

        # Seleccionamos la clase sobre la que se ejecuta el test
        my_request = VaccineManager()

        # Creamos variable date_signature
        date_signature = "0b47c03009ee76e2c4ce33be4e37e6fb5b913f372a0be70c071f3042025d0987"

        with open(file_store_vaccine, "r", encoding="UTF-8", newline="") as file_org:
            hash_original = hashlib.md5(file_org.__str__().encode()).hexdigest()

        # Llamamos al metodo vaccine_patient
        with self.assertRaises(VaccineManagementException) as vme:
            my_request.vaccine_patient(date_signature)

        # Confirmamos que se lanza la excepcion esperada
        self.assertEqual(vme.exception.message, "JSON decode error - formato JSON incorrecto")

        # Generamos un hash del contenido del fichero después
        with open(file_store_vaccine, "r", encoding="UTF-8", newline="") as file_new:
            hash_new = hashlib.md5(file_new.__str__().encode()).hexdigest()

        # Comprobamos que el contenido no cambia
        self.assertEqual(hash_original, hash_new)

        # Mostramos el test que se esta ejecutando
        print("test_8")

    @freeze_time("2022-03-13 09:46:23.846215")
    def test_9_incorrect_store_vaccine_path(self):
        """ Test no valido de la funcion vaccine_patient """
        # Buscamos la ruta en la que se almacena el fichero store_vaccine
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T11.EG3/src/JsonFiles/RF3"
        file_store_vaccine = json_files_path + "/store_vaccine.json"

        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        # Borramos directorio para que no lo encuentre
        os.rmdir(json_files_path)

        # Seleccionamos la clase sobre la que se ejecuta el test
        my_request = VaccineManager()

        # Creamos variable date_signature
        date_signature = "0b47c03009ee76e2c4ce33be4e37e6fb5b913f372a0be70c071f3042025d0987"

        # Llamamos al metodo vaccine_patient
        with self.assertRaises(VaccineManagementException) as vme:
            my_request.vaccine_patient(date_signature)

        # Confirmamos que se lanza la excepcion esperada
        self.assertEqual(vme.exception.message,
                         "JSON file not found error - fichero o ruta incorrectos")

        # Comprobamos que el fichero store_vaccine no se crea
        self.assertFalse(os.path.isfile(file_store_vaccine))

        # Volvemos a crear directorio
        os.mkdir(json_files_path)

        # Mostramos el test que se esta ejecutando
        print("test_9")

    def test_10_validate_date_signature_ok(self):
        """ Test valido de la funcion validate date signature """
        # Seleccionamos la clase sobre la que se ejecuta el test
        my_request = VaccineManager()

        # Creamos variable date_signature
        date_signature = "0b47c03009ee76e2c4ce33be4e37e6fb5b913f372a0be70c071f3042025d0987"

        # Llamamos al metodo validate_date_signature
        value= my_request.validate_date_signature(date_signature)

        # Comprobamos que el metodo devuleve true
        self.assertTrue(value)

        # Mostramos el test que se esta ejecutando
        print("test_10")

    def test_11_validate_date_signature_nok(self):
        """ Test valido de la funcion validate date signature"""
        # Seleccionamos la clase sobre la que se ejecuta el test
        my_request = VaccineManager()

        # Creamos variable date_signature
        date_signature = "0b47c03009"

        # Llamamos al metodo validate_date_signature
        with self.assertRaises(VaccineManagementException) as vme:
            my_request.validate_date_signature(date_signature)

        # Confirmamos que se lanza la excepcion esperada
        self.assertEqual(vme.exception.message, "Formato del date_signature invalido")

        # Mostramos el test que se esta ejecutando
        print("test_11")

    @freeze_time("2022-03-13 09:46:23.846215")
    def test_12_ok_store_vaccine_with_data_first(self):
        """ Test valido de la funcion vaccine_patient """
        # Buscamos la ruta en la que se almacena el fichero store_vaccine
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T11.EG3/src/JsonFiles/RF3"
        file_store_vaccine = json_files_path + "/store_vaccine.json"

        if os.path.isfile(file_store_vaccine):
            os.remove(file_store_vaccine)

        self.setup_test_7()

        # Seleccionamos la clase sobre la que se ejecuta el test
        my_request = VaccineManager()

        # Llamamos al metodo vaccine_patient para el paciente NomTreintacaracteres yunblanco
        my_request.vaccine_patient(
            "0b47c03009ee76e2c4ce33be4e37e6fb5b913f372a0be70c071f3042025d0987")

        # Creamos variable date_signature
        date_signature = "c5bc7fff26b8d2d98da73ec90147294920d029b53516a0a5d57272b32f790f1c"

        # Llamamos al metodo vaccine_patient para el nuevo paciente (Juan Martinez)
        value = my_request.vaccine_patient(date_signature)

        # Comprobamos si el resultado es el esperado
        self.assertTrue(value)

        # Comprobamos que se guarda la cita en store_vaccine
        try:
            # Intentamos abrir el fichero JSON
            with open(file_store_vaccine, "r", encoding="UTF-8", newline="") as file:
                # Guardamos los datos del fichero en una lista
                data_list = json.load(file)
        except FileNotFoundError as ex:
            # En caso de que el fichero no exista, lanzamos una excepcion
            raise VaccineManagementException("Fichero no creado") from ex
        except json.JSONDecodeError as ex:
            # Si se produce un error al decodificar mostaramos una excepcion
            raise VaccineManagementException(
                "JSON decode error - formato JSON incorrecto") from ex

        # Creamos una variable para guardar si se encuentran los datos de vacunación del paciente
        found_1 = False
        found_2 = False

        # Recorremos las entradas de fichero
        for item in data_list:
            # Si se han guardado todos los datos de vacunación
            if date_signature == item:
                found_1 = True

            if "2022-03-13 09:46:23.846215" == item:
                found_2 = True

        # Comprobamos si el resultado es el esperado
        self.assertTrue(found_1)
        self.assertTrue(found_2)

        # Mostramos el test que se esta ejecutando
        print("test_12")


if __name__ == '__main__':
    unittest.main()
