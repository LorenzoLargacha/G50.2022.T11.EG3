"""Module"""
import json
import re
# import uuid
from pathlib import Path

from .vaccine_patient_register import VaccinePatientRegister
from .vaccine_management_exception import VaccineManagementException


class VaccineManager:
    """Class for providing the methods for managing the vaccination process"""
    def __init__(self):
        pass

    @staticmethod
    def validate_guid(guid):
        """RETURN TRUE IF THE GUID v4 IS RIGHT, OR FALSE IN OTHER CASE"""
        try:
            # my_uuid = uuid.UUID(guid)
            myregex = re.compile(r'^[0-9A-F]{8}-[0-9A-F]{4}-4[0-9A-F]{3}-[89AB][0-9A-F]{3}-'
                                 r'[0-9A-F]{12}$',
                                 re.IGNORECASE)
            res = myregex.fullmatch(guid)
            if not res:
                raise VaccineManagementException("Invalid UUID v4 format")
        except ValueError as ex:
            raise VaccineManagementException("Id received is not a UUID") from ex
        return True

    # def request_vaccination_id(self, patient_id, registration_type, name, phone_number, age):
    def request_vaccination_id(self, paciente):
        """Creamos un nuevo paciente con los atributos pasdos como parametro,
        y devolvemos el paciente"""
        # Obtenemos las variables del diccionario
        patient_id = paciente['patient_id']
        registration_type = paciente['registration_type']
        name = paciente['name']
        # phone_number = paciente['phone_number']
        # age = paciente['age']

        # Buscamos la ruta en la que se almacena el fichero
        json_files_path = str(Path.home()) + "/PycharmProjects/G50.2022.T11.EG3/src/JsonFiles"
        file_store = json_files_path + "/store_patient.json"

        # Comprobamos si el guid es valido
        if self.validate_guid(patient_id):
            # Creamos un objeto tipo paciente
            my_register = VaccinePatientRegister(paciente)

            try:
                # Intenamos abrir el fichero JSON
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
                    if (item["_VaccinePatientRegister__registration_type"] == registration_type) \
                            and (item["_VaccinePatientRegister__full_name" == name]):
                        found = True

            # Si ese paciente no se ecuentra en el fichero lo guardamos
            if found is False:
                # Almacenamos sus datos en la lista
                data_list.append(my_register.__dict__)

                try:
                    # Intenamos abrir el fichero JSON para escribir
                    with open(file_store, "w", encoding="UTF-8", newline="") as file:
                        # Serializamos el objeto y guardamos los datos en el fichero
                        json.dump(data_list, file, indent=2)
                except FileNotFoundError as ex:
                    # Si no existe el fichero mostramos una excepcion
                    raise VaccineManagementException(
                        "JSON file not found error - fichero o ruta incorrectos") from ex

            # Si ese paciente ya se ecuentra en el fichero mostramos una excepcion
            if found is True:
                raise VaccineManagementException("Paciente ya registrado")

        # Si el paciente no estaba en el fichero, lo devolvemos
        return my_register.patient_system_id
