"""Module"""
import json
import re
import uuid
from datetime import datetime
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

    @staticmethod
    def validate_patient_system_id(patient_system_id):
        """ Return True si el patient_system_id es correcto, en otro caso Excepcion """
        # Comprobamos que el patient_system_id es una cadena hexadecimal de 32 caracteres
        myregex = re.compile(r'^[0-9A-F]{32}$', re.IGNORECASE)
        res = myregex.fullmatch(patient_system_id)
        if not res:
            raise VaccineManagementException("Formato del patient_system_id invalido")
        return True

    @staticmethod
    def validate_date_signature(date_signature):
        """ Return True si el date_signature es correcto, en otro caso Excepcion """
        # Comprobamos que el date_signature es una cadena hexadecimal de 64 caracteres
        myregex = re.compile(r'^[0-9A-F]{64}$', re.IGNORECASE)
        res = myregex.fullmatch(date_signature)
        if not res:
            raise VaccineManagementException("Formato del date_signature invalido")
        return True

    def request_vaccination_id(self, patient_id, registration_type, name, phone_number, age):
        """ Creamos un nuevo paciente con los atributos pasados como parametro,
        y devolvemos el patient_system_id del paciente """

        # Buscamos la ruta en la que se almacena el fichero store_patient
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T11.EG3/src/JsonFiles/RF1"
        file_store = json_files_path + "/store_patient.json"

        # Comprobamos si los atributos son validos
        if (self.validate_guid(patient_id))\
                and (self.validate_registration_type(registration_type))\
                and (self.validate_name_surname(name))\
                and (self.validate_phone_number(phone_number)) \
                and (self.validate_age(age)):

            # Creamos un objeto tipo paciente (VaccinePatientRegister)
            my_register = VaccinePatientRegister(patient_id,
                                                 name, registration_type, phone_number, age)

            try:
                # Intentamos abrir el fichero JSON para leer
                with open(file_store, "r", encoding="UTF-8", newline="") as file:
                    # Guardamos los datos del fichero en una lista
                    data_list = json.load(file)
            except FileNotFoundError:
                # En caso de que el fichero no exista creamos una lista para almacenar los datos
                data_list = []
            except json.JSONDecodeError as ex:
                # Si se produce un error al decodificar mostramos una excepcion
                raise VaccineManagementException(
                    "JSON decode error - formato JSON incorrecto") from ex

            # Creamos una variable para guardar si se encuentra un paciente con esos datos
            found = False
            # Recorremos las entradas del fichero
            for item in data_list:
                # Si el patient_id se encuentra en el fichero
                if item["_VaccinePatientRegister__patient_id"] == patient_id:
                    # Comprobamos si coincide el tipo de registro que se quiere realizar
                    # y si es del mismo tipo y coincide el nombre registrado found = True
                    if (item["_VaccinePatientRegister__registration_type"] == registration_type)\
                            and (item["_VaccinePatientRegister__full_name"] == name):
                        found = True

            # Si ese paciente no se encuentra en el fichero lo guardamos
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

            # Si ese paciente ya se encuentra en el fichero lanzamos una excepcion
            if found is True:
                raise VaccineManagementException("Paciente ya registrado")

        # Si el paciente se crea correctamente, devolvemos su patient_system_id
        return my_register.patient_system_id

    def get_vaccine_date(self, input_file):
        """ Leemos el fichero de entrada, comprobamos los campos,
        generamos una cita y la almacenamos en un fichero """

        # Intentamos abrir el fichero de entrada y guardamos sus datos
        try:
            # Intentamos abrir el fichero JSON para leer
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

        # Comprobamos la estructura del fichero JSON
        # Si la solicitud no se encuentra en el fichero lanzamos una excepcion
        if len(data_list_input) == 0:
            raise VaccineManagementException("La solicitud no se encontro en el archivo de solicitudes JSON")

        # Recorremos las entradas del fichero para comprobar etiquetas y valores
        for item in data_list_input:
            # Si el fichero JSON solo tiene un item, y el item solo tiene dos etiquetas,
            # y las etiquetas son correctas, entonces comprobamos los valores
            # ------ comprobar que no haya dos etiquetas iguales? o ya lo hace JSONDecodeError ? hay que hacer otro test?
            # ------ debe funcionar para un fichero con muchas solicitudes? no dice nada
            # ------ un mismo paciente puede pedir varias citas? no dice nada
            if len(data_list_input) == 1 and len(item) == 2 \
                    and "PatientSystemID" in item and "ContactPhoneNumber" in item:
                # Comprobamos si los valores son válidos y los guardamos
                if (self.validate_phone_number(item["ContactPhoneNumber"])) \
                        and (self.validate_patient_system_id(item["PatientSystemID"])):
                    patient_system_id = item["PatientSystemID"]
                    phone_number = item["ContactPhoneNumber"]

            # Si la estructura NO es correcta lanzamos una excepcion
            # (si las etiquetas no son correctas)
            else:
                raise VaccineManagementException("Estructura JSON incorrecta")

        # Buscamos la ruta en la que se almacena el fichero store_patient
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T11.EG3/src/JsonFiles/RF1"
        file_store_patient = json_files_path + "/store_patient.json"

        # Intentamos abrir el fichero store_patient y guardar sus datos
        try:
            # Intentamos abrir el fichero JSON para leer
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

        # Recorremos las entradas de fichero
        for item in data_list_patient:
            # Si el patient_system_id se encuentra en el fichero (coincide con los datos)
            if item["_VaccinePatientRegister__patient_sys_id"] == patient_system_id:
                # Como en metodo request_vaccination_id no permite que se guarden
                # dos pacientes iguales, sabemos que el patient_system_id es unico
                found = True
                # Obtenemos el guid del paciente
                patient_id = item["_VaccinePatientRegister__patient_id"]

        if found is True:
            # Creamos un objeto tipo cita (VaccinationAppoinment)
            days = 10
            my_register = VaccinationAppoinment(patient_id, patient_system_id, phone_number, days)

            # Escribimos la cita en el fichero store_date
            # Buscamos la ruta en la que se almacena el fichero store_date
            json_files_path = str(Path.home()) \
                              + "/PycharmProjects/G50.2022.T11.EG3/src/JsonFiles/RF2"
            file_store_date = json_files_path + "/store_date.json"

            try:
                # Intentamos abrir el fichero JSON para leer
                with open(file_store_date, "r", encoding="UTF-8", newline="") as file:
                    # Guardamos los datos del fichero en una lista
                    data_list = json.load(file)
            except FileNotFoundError:
                # En caso de que el fichero no exista creamos una lista para almacenar los datos
                data_list = []
            except json.JSONDecodeError as ex:
                # Si se produce un error al decodificar mostramos una excepcion
                raise VaccineManagementException(
                    "JSON decode error - formato JSON incorrecto") from ex

            # Guardamos los datos de vacunación en la lista
            data_list.append(my_register.__dict__)

            try:
                # Intentamos abrir el fichero JSON para escribir
                with open(file_store_date, "w", encoding="UTF-8", newline="") as file:
                    # Serializamos el objeto y guardamos los datos en el fichero
                    json.dump(data_list, file, indent=2)
            except FileNotFoundError as ex:
                # Si no existe el fichero lanzamos una excepcion
                raise VaccineManagementException(
                    "JSON file not found error - fichero o ruta incorrectos") from ex

        # Si el paciente no está registrado, lanzamos una excepcion
        if found is False:
            raise VaccineManagementException("Paciente no registrado")

        # Si la cita se crea correctamente, devolvemos su vaccination_signature
        return my_register.vaccination_signature

    def vaccine_patient(self, date_signature):
        """ Comprobamos la clave de entrada, buscamos si la cita esta registrada,
        comprobamos que la fecha es para hoy y guardamos los datos de vacunacion en un fichero """

        # Comprobamos que la firma SHA256 sigue el formato esperado
        self.validate_date_signature(date_signature)

        # Buscamos la ruta en la que se almacena el fichero store_date
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T11.EG3/src/JsonFiles/RF2"
        file_store_date = json_files_path + "/store_date.json"

        # Intentamos abrir el fichero store_date y guardar sus datos
        try:
            # Intentamos abrir el fichero JSON
            with open(file_store_date, "r", encoding="UTF-8", newline="") as file:
                # Guardamos los datos del fichero en una lista
                data_list_date = json.load(file)
        except FileNotFoundError as ex:
            # En caso de que el fichero no exista, lanzamos una excepcion
            raise VaccineManagementException("Fichero store_date no creado") from ex
        except json.JSONDecodeError as ex:
            # Si los datos no siguen el formato JSON
            raise VaccineManagementException(
                "JSON decode error - formato JSON incorrecto") from ex

        # Creamos una variable para guardar si se encuentra una cita con esa clave
        found = False

        # Recorremos las entradas de fichero
        for item in data_list_date:
            # Si el date_signature se encuentra en el fichero (cita registrada)
            if item["_VaccinationAppoinment__date_signature"] == date_signature:
                found = True
                # Obtenemos la fecha de la cita
                date_time = item["_VaccinationAppoinment__appoinment_date"]

        # Si la cita no está registrada, lanzamos una excepcion
        if found is False:
            raise VaccineManagementException("Cita no registrada")

        # Guardamos la fecha de hoy
        today = datetime.today().date()
        # Convertimos el timestamp de la cita a fecha
        appoinment_date = datetime.fromtimestamp(date_time).date()

        # Si la fecha registrada en la cita no es hoy, lanzamos una excepcion
        if appoinment_date != today:
            raise VaccineManagementException("Cita no registrada para la fecha de hoy")

        # Escribimos los datos de vacunación en el fichero store_vaccine
        # Buscamos la ruta en la que se almacena el fichero store_vaccine
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T11.EG3/src/JsonFiles/RF3"
        file_store_vaccine = json_files_path + "/store_vaccine.json"

        try:
            # Intentamos abrir el fichero JSON para leer
            with open(file_store_vaccine, "r", encoding="UTF-8", newline="") as file:
                # Guardamos los datos del fichero en una lista
                data_list = json.load(file)
        except FileNotFoundError:
            # En caso de que el fichero no exista creamos una lista para almacenar los datos
            data_list = []
        except json.JSONDecodeError as ex:
            # Si se produce un error al decodificar mostramos una excepcion
            raise VaccineManagementException(
                "JSON decode error - formato JSON incorrecto") from ex

        # Guardamos los datos de vacunación en la lista
        data_list.append(date_signature.__str__())
        data_list.append(datetime.utcnow().__str__())

        try:
            # Intentamos abrir el fichero JSON para escribir
            with open(file_store_vaccine, "w", encoding="UTF-8", newline="") as file:
                # Serializamos el objeto y guardamos los datos en el fichero
                json.dump(data_list, file, indent=2)
        except FileNotFoundError as ex:
            # Si no existe el fichero lanzamos una excepcion
            raise VaccineManagementException(
                "JSON file not found error - fichero o ruta incorrectos") from ex

        # Si la clave y fecha son válidas, devolvemos True
        return True
