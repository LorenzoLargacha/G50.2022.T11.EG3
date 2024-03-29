"""Modulos"""
import os
import json
from pathlib import Path
import unittest
import hashlib
from freezegun import freeze_time

from uc3m_care import VaccineManager
from uc3m_care import VaccineManagementException


class MyTestCase(unittest.TestCase):
    """ Test Unitest Get Vaccine Date """

    @freeze_time("2022-03-03 09:46:23.846215")
    def test_1_get_vaccine_date_ok(self):
        """ Test valido de la funcion get_vaccine_date """
        # Buscamos la ruta en la que se almacena el fichero store_patient
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T11.EG3/src/JsonFiles/RF1"
        file_store_patient = json_files_path + "/store_patient.json"

        # Buscamos la ruta en la que se almacena el fichero de test (solicitud de cita)
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
            # Si se produce un error al decodificar mostramos una excepcion
            raise VaccineManagementException(
                "JSON decode error - formato JSON incorrecto") from ex

        # Creamos una variable para guardar si se encuentra la cita del paciente
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
        print("test_1")

    @freeze_time("2022-03-03 09:46:23.846215")
    def test_parametrized_not_valid_get_vaccine_date(self):
        """ Test 2-70. Tests no validos de la funcion get_vaccine_date (parametrizados) """
        # Buscamos la ruta en la que se almacena el fichero store_patient
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T11.EG3/src/JsonFiles/RF1"
        file_store_patient = json_files_path + "/store_patient.json"

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

        # Seleccionamos la clase sobre la que se ejecuta el test
        my_request = VaccineManager()

        # Llamamos al metodo request_vaccination_id para almacenar el paciente
        my_request.request_vaccination_id(patient_id, registration_type,
                                          name, phone_number, age)

        # Llamamos al metodo get_vaccine_date para precargar una cita
        my_request.get_vaccine_date(json_files_path + "/test_ok.json")

        # Cargamos los parametros de la lista
        for par1, par2, par3 in param_list_nok:
            with self.subTest():
                # Buscamos la ruta en la que se almacena el fichero de test (solicitud de cita)
                json_files_path = str(Path.home()) \
                                  + "/PycharmProjects/G50.2022.T11.EG3/src/JsonFiles/RF2"
                input_file = json_files_path + par1

                # Generamos un hash del contenido del fichero antes
                with open(file_store_date, "r", encoding="UTF-8", newline="") as file_org:
                    hash_original = hashlib.md5(file_org.__str__().encode()).hexdigest()

                # Llamamos al metodo get_vaccine_date
                with self.assertRaises(VaccineManagementException) as vme:
                    my_request.get_vaccine_date(input_file)

                # Confirmamos que se lanza la excepcion esperada
                self.assertEqual(vme.exception.message, par2)

                # Generamos un hash del contenido del fichero después
                with open(file_store_date, "r", encoding="UTF-8", newline="") as file_new:
                    hash_new = hashlib.md5(file_new.__str__().encode()).hexdigest()

                # Comprobamos que el contenido no cambia
                self.assertEqual(hash_original, hash_new)

                # Mostramos el test que se esta ejecutando
                print(par3)

    def test_71_no_store_patient_nok(self):
        """ Test no valido de la funcion get_vaccine_date,
        para comprobar que se lanza excepcion cuando no hay fichero store_patient """
        # Buscamos la ruta en la que se almacena el fichero store_patient
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T11.EG3/src/JsonFiles/RF1"
        file_store_patient = json_files_path + "/store_patient.json"

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

        # Buscamos la ruta en la que se almacena el fichero de test (solicitud de cita)
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T11.EG3/src/JsonFiles/RF2"
        input_file = json_files_path + "/test_ok.json"

        # Llamamos al metodo get_vaccine_date
        with self.assertRaises(VaccineManagementException) as vme:
            my_request.get_vaccine_date(input_file)

        # Confirmamos que se lanza la excepcion esperada
        self.assertEqual(vme.exception.message, "Fichero store_patient no creado")

        # Comprobamos que el fichero store_date no se crea
        self.assertFalse(os.path.isfile(file_store_date))

        # Mostramos el test que se esta ejecutando
        print("test_71")

    @freeze_time("2022-03-03 09:46:23.846215")
    def test_72_get_two_vaccine_date_ok(self):
        """ Test valido de la funcion get_vaccine_date,
        comprobamos que si se piden dos citas seguidas, para dos pacientes distintos,
        estas se crean y almacenan """
        # Buscamos la ruta en la que se almacena el fichero store_patient
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T11.EG3/src/JsonFiles/RF1"
        file_store_patient = json_files_path + "/store_patient.json"

        # Buscamos la ruta en la que se almacena el fichero de test (solicitud de cita)
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T11.EG3/src/JsonFiles/RF2"
        input_file_1 = json_files_path + "/test_ok.json"
        input_file_2 = json_files_path + "/test_ok_2.json"

        # Buscamos la ruta en la que se almacena el fichero store_date
        file_store_date = json_files_path + "/store_date.json"

        # Si el fichero ya existe, lo borramos para no tener datos precargados
        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)
        if os.path.isfile(file_store_date):
            os.remove(file_store_date)

        # Guardamos los atributos en las variables correspondientes
        patient_id_1 = "bb5dbd6f-d8b4-413f-8eb9-dd262cfc54e0"
        registration_type_1 = "Regular"
        name_1 = "NomTreintacaracteres yunblanco"
        phone_number_1 = "+34123456789"
        age_1 = "6"

        patient_id_2 = "bb5dbd6f-d8b4-413f-8eb9-aa333dbd45c2"
        registration_type_2 = "Regular"
        name_2 = "Juan Martinez"
        phone_number_2 = "+34666666666"
        age_2 = "21"

        alg = "SHA-256"
        typ = "DS"

        # Seleccionamos la clase sobre la que se ejecuta el test
        my_request = VaccineManager()

        # Llamamos al metodo request_vaccination_id para almacenar los pacientes
        patient_system_id_1 = my_request.request_vaccination_id(patient_id_1, registration_type_1,
                                                                name_1, phone_number_1, age_1)
        patient_system_id_2 = my_request.request_vaccination_id(patient_id_2, registration_type_2,
                                                                name_2, phone_number_2, age_2)

        # Llamamos al metodo get_vaccine_date
        value_1 = my_request.get_vaccine_date(input_file_1)
        # Comprobamos si el resultado es el esperado
        self.assertEqual("0b47c03009ee76e2c4ce33be4e37e6fb5b913f372a0be70c071f3042025d0987",
                         value_1)

        # Llamamos al metodo get_vaccine_date
        value_2 = my_request.get_vaccine_date(input_file_2)
        # Comprobamos si el resultado es el esperado
        self.assertEqual("c5bc7fff26b8d2d98da73ec90147294920d029b53516a0a5d57272b32f790f1c",
                         value_2)

        # Comprobamos que se guarda la cita en store_date
        try:
            # Intentamos abrir el fichero JSON para leer
            with open(file_store_date, "r", encoding="UTF-8", newline="") as file:
                # Guardamos los datos del fichero en una lista
                data_list = json.load(file)
        except FileNotFoundError as ex:
            # En caso de que el fichero no exista, lanzamos una excepcion
            raise VaccineManagementException("Fichero no creado") from ex
        except json.JSONDecodeError as ex:
            # Si se produce un error al decodificar mostramos una excepcion
            raise VaccineManagementException(
                "JSON decode error - formato JSON incorrecto") from ex

        # Creamos una variable para guardar si se encuentra la cita del paciente 1
        found_1 = False
        # Recorremos las entradas de fichero
        for item in data_list:
            # Si se han guardado todos los atributos de la cita
            if (item["_VaccinationAppoinment__alg"] == alg) \
                    and (item["_VaccinationAppoinment__type"] == typ) \
                    and (item["_VaccinationAppoinment__patient_id"] == patient_id_1) \
                    and (item["_VaccinationAppoinment__patient_sys_id"] == patient_system_id_1) \
                    and (item["_VaccinationAppoinment__phone_number"] == phone_number_1) \
                    and ("_VaccinationAppoinment__issued_at" in item) \
                    and ("_VaccinationAppoinment__appoinment_date" in item):
                found_1 = True

        # Comprobamos si el resultado es el esperado
        self.assertTrue(found_1)

        # Creamos una variable para guardar si se encuentra la cita del paciente 2
        found_2 = False
        # Recorremos las entradas de fichero
        for item in data_list:
            # Si se han guardado todos los atributos de la cita
            if (item["_VaccinationAppoinment__alg"] == alg) \
                    and (item["_VaccinationAppoinment__type"] == typ) \
                    and (item["_VaccinationAppoinment__patient_id"] == patient_id_2) \
                    and (item["_VaccinationAppoinment__patient_sys_id"] == patient_system_id_2) \
                    and (item["_VaccinationAppoinment__phone_number"] == phone_number_2) \
                    and ("_VaccinationAppoinment__issued_at" in item) \
                    and ("_VaccinationAppoinment__appoinment_date" in item):
                found_2 = True

        # Comprobamos si el resultado es el esperado
        self.assertTrue(found_2)

        # Mostramos el test que se esta ejecutando
        print("test_72")


# Parámetros para los test not valid get_vaccine_date
param_list_nok = [("/test_fichero_vacio.json",
                   "JSON decode error - formato JSON incorrecto", "test_2"),
                  ("/test_doble_contenido.json",
                   "JSON decode error - formato JSON incorrecto", "test_3"),
                  ("/test_no_llave_ini.json",
                   "JSON decode error - formato JSON incorrecto", "test_4"),
                  ("/test_doble_llave_ini.json",
                   "JSON decode error - formato JSON incorrecto", "test_5"),
                  ("/test_modif_llave_ini.json",
                   "JSON decode error - formato JSON incorrecto", "test_6"),
                  ("/test_no_datos.json",
                   "La solicitud no se encontro en el archivo de solicitudes JSON", "test_7"),
                  ("/test_doble_datos.json",
                   "JSON decode error - formato JSON incorrecto", "test_8"),
                  ("/test_no_llave_fin.json",
                   "JSON decode error - formato JSON incorrecto", "test_9"),
                  ("/test_doble_llave_fin.json",
                   "JSON decode error - formato JSON incorrecto", "test_10"),
                  ("/test_modif_llave_fin.json",
                   "JSON decode error - formato JSON incorrecto", "test_11"),
                  ("/test_no_campo1.json",
                   "JSON decode error - formato JSON incorrecto", "test_12"),
                  ("/test_doble_campo1.json",
                   "JSON decode error - formato JSON incorrecto", "test_13"),
                  ("/test_no_separador.json",
                   "JSON decode error - formato JSON incorrecto", "test_14"),
                  ("/test_doble_separador.json",
                   "JSON decode error - formato JSON incorrecto", "test_15"),
                  ("/test_modif_separador.json",
                   "JSON decode error - formato JSON incorrecto", "test_16"),
                  ("/test_no_campo2.json",
                   "JSON decode error - formato JSON incorrecto", "test_17"),
                  ("/test_doble_campo2.json",
                   "JSON decode error - formato JSON incorrecto", "test_18"),
                  ("/test_no_etiqueta_dato1.json",
                   "JSON decode error - formato JSON incorrecto", "test_19"),
                  ("/test_doble_etiqueta_dato1.json",
                   "JSON decode error - formato JSON incorrecto", "test_20"),
                  ("/test_no_igualdad1.json",
                   "JSON decode error - formato JSON incorrecto", "test_21"),
                  ("/test_doble_igualdad1.json",
                   "JSON decode error - formato JSON incorrecto", "test_22"),
                  ("/test_modif_igualdad1.json",
                   "JSON decode error - formato JSON incorrecto", "test_23"),
                  ("/test_no_valor_dato1.json",
                   "JSON decode error - formato JSON incorrecto", "test_24"),
                  ("/test_doble_valor_dato1.json",
                   "JSON decode error - formato JSON incorrecto", "test_25"),
                  ("/test_no_etiqueta_dato2.json",
                   "JSON decode error - formato JSON incorrecto", "test_26"),
                  ("/test_doble_etiqueta_dato2.json",
                   "JSON decode error - formato JSON incorrecto", "test_27"),
                  ("/test_no_igualdad2.json",
                   "JSON decode error - formato JSON incorrecto", "test_28"),
                  ("/test_doble_igualdad2.json",
                   "JSON decode error - formato JSON incorrecto", "test_29"),
                  ("/test_doble_igualdad2.json",
                   "JSON decode error - formato JSON incorrecto", "test_30"),
                  ("/test_no_valor_dato2.json",
                   "JSON decode error - formato JSON incorrecto", "test_31"),
                  ("/test_doble_valor_dato2.json",
                   "JSON decode error - formato JSON incorrecto", "test_32"),
                  ("/test_no_comillas1.json",
                   "JSON decode error - formato JSON incorrecto", "test_33"),
                  ("/test_doble_comillas1.json",
                   "JSON decode error - formato JSON incorrecto", "test_34"),
                  ("/test_modif_comillas1.json",
                   "JSON decode error - formato JSON incorrecto", "test_35"),
                  ("/test_no_valor_etiqueta1.json",
                   "Estructura JSON incorrecta", "test_36"),
                  ("/test_doble_valor_etiqueta1.json",
                   "Estructura JSON incorrecta", "test_37"),
                  ("/test_modif_valor_etiqueta1.json",
                   "Estructura JSON incorrecta", "test_38"),
                  ("/test_no_comillas2.json",
                   "JSON decode error - formato JSON incorrecto", "test_39"),
                  ("/test_doble_comillas2.json",
                   "JSON decode error - formato JSON incorrecto", "test_40"),
                  ("/test_modif_comillas2.json",
                   "JSON decode error - formato JSON incorrecto", "test_41"),
                  ("/test_no_comillas3.json",
                   "JSON decode error - formato JSON incorrecto", "test_42"),
                  ("/test_doble_comillas3.json",
                   "JSON decode error - formato JSON incorrecto", "test_43"),
                  ("/test_modif_comillas3.json",
                   "JSON decode error - formato JSON incorrecto", "test_44"),
                  ("/test_no_valor1.json",
                   "Formato del patient_system_id invalido", "test_45"),
                  ("/test_doble_valor1.json",
                   "Formato del patient_system_id invalido", "test_46"),
                  ("/test_modif_valor1.json",
                   "Formato del patient_system_id invalido", "test_47"),
                  ("/test_no_comillas4.json",
                   "JSON decode error - formato JSON incorrecto", "test_48"),
                  ("/test_doble_comillas4.json",
                   "JSON decode error - formato JSON incorrecto", "test_49"),
                  ("/test_modif_comillas4.json",
                   "JSON decode error - formato JSON incorrecto", "test_50"),
                  ("/test_no_comillas5.json",
                   "JSON decode error - formato JSON incorrecto", "test_51"),
                  ("/test_doble_comillas5.json",
                   "JSON decode error - formato JSON incorrecto", "test_52"),
                  ("/test_modif_comillas5.json",
                   "JSON decode error - formato JSON incorrecto", "test_53"),
                  ("/test_no_valor_etiqueta2.json",
                   "Estructura JSON incorrecta", "test_54"),
                  ("/test_doble_valor_etiqueta2.json",
                   "Estructura JSON incorrecta", "test_55"),
                  ("/test_modif_valor_etiqueta2.json",
                   "Estructura JSON incorrecta", "test_56"),
                  ("/test_no_comillas6.json",
                   "JSON decode error - formato JSON incorrecto", "test_57"),
                  ("/test_doble_comillas6.json",
                   "JSON decode error - formato JSON incorrecto", "test_58"),
                  ("/test_modif_comillas6.json",
                   "JSON decode error - formato JSON incorrecto", "test_59"),
                  ("/test_no_comillas7.json",
                   "JSON decode error - formato JSON incorrecto", "test_60"),
                  ("/test_doble_comillas7.json",
                   "JSON decode error - formato JSON incorrecto", "test_61"),
                  ("/test_modif_comillas7.json",
                   "JSON decode error - formato JSON incorrecto", "test_62"),
                  ("/test_no_valor2.json",
                   "Formato del telefono invalido", "test_63"),
                  ("/test_doble_valor2.json",
                   "Formato del telefono invalido", "test_64"),
                  ("/test_modif_valor2.json",
                   "Formato del telefono invalido", "test_65"),
                  ("/test_no_comillas8.json",
                   "JSON decode error - formato JSON incorrecto", "test_66"),
                  ("/test_doble_comillas8.json",
                   "JSON decode error - formato JSON incorrecto", "test_67"),
                  ("/test_modif_comillas8.json",
                   "JSON decode error - formato JSON incorrecto", "test_68"),
                  ("/test_campo3.json",
                   "Estructura JSON incorrecta", "test_69"),
                  ("/test_nok.json",
                   "Fichero input_file no creado", "test_70")]


if __name__ == '__main__':
    unittest.main()
