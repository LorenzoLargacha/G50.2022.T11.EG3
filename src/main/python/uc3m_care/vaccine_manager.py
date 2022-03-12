"""Module """
from .vaccine_patient_register import VaccinePatientRegister
from .vaccine_management_exception import VaccineManagementException

# import json
import re
import uuid



class VaccineManager:
    """Class for providing the methods for managing the vaccination process"""
    def __init__(self):
        pass

    @staticmethod
    def validate_guid(guid):
        """RETURN TRUE IF THE GUID v4 IS RIGHT, OR FALSE IN OTHER CASE"""
        try:
            my_uuid = uuid.UUID(guid)
            myregex = re.compile(r'^[0-9A-F]{8}-[0-9A-F]{4}-4[0-9A-F]{3}-[89AB][0-9A-F]{3}-'r'[0-9A-F]{12}$',
                                 re.IGNORECASE)
            res = myregex.fullmatch(guid)
            if not res:
                raise VaccineManagementException("Invalid UUID v4 format")
        except ValueError:
            raise VaccineManagementException("Id received is not a UUID")
        return True

    def request_vaccination_id(self, patient_id, registration_type, name, phone_number, age):
        """Creamos un nuevo paciente con los atributos pasdos como parametro, solo si el guid es valido"""
        if self.validate_guid(patient_id):
            my_register = VaccinePatientRegister(patient_id, name, registration_type, phone_number, age)

        return my_register.patient_system_id
