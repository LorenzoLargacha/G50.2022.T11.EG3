"""MODULE: access_request. Contains the access request class"""
import hashlib
import json
from datetime import datetime


class VaccinePatientRegister:
    """Class representing the register of the patient in the system"""

    def __init__(self, patient_id, full_name, registration_type, phone_number, age):
        # Creamos los atributos
        self.__patient_id = patient_id
        self.__full_name = full_name
        self.__registration_type = registration_type
        self.__phone_number = phone_number
        self.__age = age
        justnow = datetime.utcnow()
        self.__time_stamp = datetime.timestamp(justnow)

        # RF1 -> evitamos que cambie la hora (borrar despues, solo sirve para los tests)
        # self.__time_stamp = 1646300783.846215

        # RF2 -> añadimos el atributo patient_system_id para que se guarde en store_patient
        self.__patient_sys_id = self.patient_system_id

        # PRUEBA
        # dt_object = datetime.fromtimestamp(self.__time_stamp)
        # print(dt_object)
        # dt_object = datetime.fromtimestamp(1646300783.846215)
        # print(dt_object)


    def __str__(self):
        return "VaccinePatientRegister:" + json.dumps(self.__dict__)

    @property
    def full_name(self):
        """Property representing the name and the surname of
        the person who request the registration"""
        return self.__full_name

    @full_name.setter
    def full_name(self, value):
        self.__full_name = value

    @property
    def vaccine_type(self):
        """Property representing the type vaccine"""
        return self.__registration_type

    @vaccine_type.setter
    def vaccine_type(self, value):
        self.__registration_type = value

    @property
    def phone_number(self):
        """Property representing the requester's phone number"""
        return self.__phone_number

    @phone_number.setter
    def phone_number(self, value):
        self.__phone_number = value

    @property
    def patient_id(self):
        """Property representing the requester's UUID"""
        return self.__patient_id

    @patient_id.setter
    def patient_id(self, value):
        self.__patient_id = value

    @property
    def time_stamp(self):
        """Read-only property that returns the timestamp of the request"""
        return self.__time_stamp

    @property
    def patient_system_id(self):
        """Returns the md5 signature"""
        return hashlib.md5(self.__str__().encode()).hexdigest()

    @property
    def patient_sys_id(self):
        """Returns the patient's patient_sys_id"""
        return self.__patient_sys_id

    @property
    def patient_age(self):
        """Returns the patient's age"""
        return self.__age
