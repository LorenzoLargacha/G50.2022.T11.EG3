"""Module"""
import json
import re
import uuid
from pathlib import Path

from .vaccine_patient_register import VaccinePatientRegister
from .vaccination_appoinment import VaccinationAppoinment
from .vaccine_management_exception import VaccineManagementException


class VaccineManager:
    """ Class for providing the methods for managing the vaccination process """

    def __init__(self):
        pass

    @staticmethod
    def validate_guid(guid):
        """ RETURN TRUE IF THE GUID v4 IS RIGHT, OR EXCEPTION IN OTHER CASE """
        try:
            uuid.UUID(guid)
            myregex = re.compile(r'^[0-9A-F]{8}-[0-9A-F]{4}-4[0-9A-F]{3}-[89AB][0-9A-F]{3}-'
                                 r'[0-9A-F]{12}$',
                                 re.IGNORECASE)
            res = myregex.fullmatch(guid)
            if not res:
                raise VaccineManagementException("Formato del UUID invalido")
        except ValueError as ex:
            raise VaccineManagementException("El Id recibido no es un UUID") from ex
        return True

    @staticmethod
    def validate_registration_type(registration_type):
        """ Return True si el registration_type es correcto, en otro caso Excepcion """
        if registration_type in ("Regular", "Family"):
            return True
        raise VaccineManagementException("Tipo de vacunacion solicitada incorrecta")

    @staticmethod
    def validate_name_surname(name):
        """ Return True si el name es correcto, en otro caso Excepcion """
        if len(name) > 30:
            raise VaccineManagementException("Cadena de nombre y apellidos mayor de 30 caracteres")

        if len(name) < 1:
            raise VaccineManagementException("Cadena de nombre vacia")

        # La funcion find encuentra el primer espacio que haya en la cadena,
        # si no hay ninguno devuelve un -1,
        # si lo encuentra al principio o al final
        # tambien sera incorrecto ya que debe estar entre medias

        if (name.find(" ") == -1) or (name.find(" ") == 0) or (name.find(" ") == len(name)-1):
            raise VaccineManagementException("Cadena sin separacion entre nombre y apellidos")
        return True

    @staticmethod
    def validate_phone_number(phone_number):
        """ Return True si el phone_number es correcto, en otro caso Excepcion """
        # Comprobamos que el numero de telefono sigue el formato +__ y otros 9 digitos
        myregex = re.compile(r'^(\+)[0-9]{11}')
        res = myregex.fullmatch(phone_number)
        if not res:
            raise VaccineManagementException("Formato del telefono invalido")

        return True

    @staticmethod
    def validate_age(age):
        """ Return True si age es correcto, en otro caso Excepcion """
        # para comprobar si la edad son solo digitos,
        # lo pasamos a numero entero
        # si no se puede convertir lanzamoa una excepcion
        try:
            age_int = int(age)
        except ValueError as ex:
            raise VaccineManagementException("La edad no es un numero") from ex

        if age_int < 6:
            raise VaccineManagementException("Edad menor de 6 años")
        if age_int > 125:
            raise VaccineManagementException("Edad mayor de 125 años")
        return True

    def request_vaccination_id(self, patient_id, registration_type, name, phone_number, age):
        """ Creamos un nuevo paciente con los atributos pasados como parametro,
        y devolvemos el patient_system_id del paciente """

        # Buscamos la ruta en la que se almacena el fichero
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T11.EG3/src/JsonFiles/RF1"
        file_store = json_files_path + "/store_patient.json"

        # Comprobamos si los atributos son validos
        if (self.validate_guid(patient_id))\
                and (self.validate_registration_type(registration_type))\
                and (self.validate_name_surname(name))\
                and (self.validate_phone_number(phone_number)) \
                and (self.validate_age(age)):
            # Creamos un objeto tipo paciente
            my_register = VaccinePatientRegister(patient_id,
                                                 name, registration_type, phone_number, age)

            try:
                # Intentamos abrir el fichero JSON
                with open(file_store, "r", encoding="UTF-8", newline="") as file:
                    # Guardamos los datos del fichero en una lista
                    data_list = json.load(file)
            except FileNotFoundError:
                # En caso de que el fichero no exista creamos una lista para almacenar los datos
                data_list = []
            except json.JSONDecodeError as ex:
                # Si se produce un error al decodificar mostaramos una excepcion
                raise VaccineManagementException(
                    "JSON decode error - formato JSON incorrecto") from ex

            # Creamos una variable para guardar si se encuentra un paciente con esos datos
            found = False
            # Recorremos las entradas de fichero
            for item in data_list:
                # Si el patient_id se encuentra en el fichero
                if item["_VaccinePatientRegister__patient_id"] == patient_id:
                    # Comprobamos si coincide el tipo de registro que se quiere realizar
                    # y si es del mismo tipo y coincide el nombre registrado found = True
                    if (item["_VaccinePatientRegister__registration_type"] == registration_type)\
                            and (item["_VaccinePatientRegister__full_name"] == name):
                        found = True

            # Si ese paciente no se ecuentra en el fichero lo guardamos
            if found is False:
                # Almacenamos sus datos en la lista
                data_list.append(my_register.__dict__)

                try:
                    # Intentamos abrir el fichero JSON para escribir
                    with open(file_store, "w", encoding="UTF-8", newline="") as file:
                        # Serializamos el objeto y guardamos los datos en el fichero
                        json.dump(data_list, file, indent=2)
                except FileNotFoundError as ex:
                    # Si no existe el fichero lanzamos una excepcion
                    raise VaccineManagementException(
                        "JSON file not found error - fichero o ruta incorrectos") from ex

            # Si ese paciente ya se ecuentra en el fichero lanzamos una excepcion
            if found is True:
                raise VaccineManagementException("Paciente ya registrado")

        # Si el paciente no estaba en el fichero, lo devolvemos
        return my_register.patient_system_id

    def get_vaccine_date(self, input_file):
        """ Leemos el fichero de entrada, validamos los campos, generamos una cita y la almacenamos """

        # Intentamos abrir el fichero de entrada y guardamos sus datos
        try:
            # Intentamos abrir el fichero JSON
            with open(input_file, "r", encoding="UTF-8", newline="") as file:
                # Guardamos los datos del fichero en una lista
                data_list_input = json.load(file)
        except FileNotFoundError as ex:
            # En caso de que el fichero no exista, lanzamos una excepcion
            raise VaccineManagementException("Fichero input_file no creado") from ex
        except json.JSONDecodeError as ex:
            # Si los datos no siguen el formato JSON
            raise VaccineManagementException(
                "JSON decode error - formato JSON incorrecto") from ex

        # Recorremos las entradas de fichero
        for item in data_list_input:
            # Si el patient_system_id se encuentra en el fichero lo guardamos
            if item["PatientSystemID"] and item["ContactPhoneNumber"]:
                patient_system_id = item["PatientSystemID"]
                phone_number = item["ContactPhoneNumber"]
            # Si las etiquetas no son correctas lanzamos una excepcion
            else:
                pass

        # Comprobamos si los atributos son validos


        # Buscamos la ruta en la que se almacena el fichero store_patient
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T11.EG3/src/JsonFiles/RF1"
        file_store_patient = json_files_path + "/store_patient.json"

        # Intentamos abrir el fichero store_patient y guardamos sus datos
        try:
            # Intentamos abrir el fichero JSON
            with open(file_store_patient, "r", encoding="UTF-8", newline="") as file:
                # Guardamos los datos del fichero en una lista
                data_list_patient = json.load(file)
        except FileNotFoundError as ex:
            # En caso de que el fichero no exista, lanzamos una excepcion
            raise VaccineManagementException("Fichero store_patient no creado") from ex
        except json.JSONDecodeError as ex:
            # Si los datos no siguen el formato JSON
            raise VaccineManagementException(
                "JSON decode error - formato JSON incorrecto") from ex

        # Creamos una variable para guardar si se encuentra un paciente con esos datos
        found = False

        # patient_id = VaccinePatientRegister.patient_system_id
        """
        # Recorremos las entradas de fichero
        for item in data_list_patient:
            # Si el patient_system_id se encuentra en el fichero
            if item["_VaccinePatientRegister__patient_id"] == \
                        patient_id:
                # Comprobamos el tipo de registro, el nombre, el numero de telefono y la edad
                if (item["_VaccinePatientRegister__registration_type"] == registration_type) \
                        and (item["_VaccinePatientRegister__full_name"] == name) \
                        and (item["_VaccinePatientRegister__phone_number"] == phone_number) \
                        and (item["_VaccinePatientRegister__age"] == age):
                    found = True"""

        if found is True:
            pass
            # Creamos un objeto tipo cita
            # my_register = VaccinationAppoinment(guid, patient_sys_id, patient_phone_number, days)


        return "prueba"
