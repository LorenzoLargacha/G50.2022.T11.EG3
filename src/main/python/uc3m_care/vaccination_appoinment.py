"""Contains the class Vaccination Appoinment"""
from datetime import datetime
import hashlib

class VaccinationAppoinment():
    """Class representing an appoinment  for the vaccination of a patient"""

    def __init__( self, guid, patient_sys_id, patient_phone_number, days ):
        self.__alg = "SHA-256"
        self.__type = "DS"
        self.__patient_id = guid
        self.__patient_sys_id = patient_sys_id
        self.__phone_number = patient_phone_number
        justnow = datetime.utcnow()
        self.__issued_at = datetime.timestamp(justnow)
        if days == 0:
            self.__appoinment_date = 0
        else:
            #timestamp is represneted in seconds.microseconds
            #age must be expressed in senconds to be added to the timestap
            self.__appoinment_date = self.__issued_at + (days * 24 * 60 * 60)

    def __signature_string(self):
        """Composes the string to be used for generating the key for the date"""
        return "{alg:" + self.__alg +",typ:" + self.__type +",patient_sys_id:" + self.__patient_sys_id + ",issuedate:" + self.__issued_at + ",vaccinationtiondate:" + self.__appoinment_date + "}"

    @property
    def patient_id( self ):
        """Property that represents the guid of the patient"""
        return self.__patient_id

    @patient_id.setter
    def patient_id( self, value ):
        self.__patient_id = value

    @property
    def patient_sys_id(self):
        """Property that represents the patient_sys_id of the patient"""
        return self.__patient_sys_id
    @patient_sys_id.setter
    def patient_sys_id(self, value):
        self.__patient_sys_id = value

    @property
    def phone_number( self ):
        """Property that represents the phone number of the patient"""
        return self.__phone_number

    @phone_number.setter
    def phone_number( self, value ):
        self.__phone_number = value

    @property
    def vaccination_signature( self ):
        """Returns the sha256 signature of the date"""
        return hashlib.sha256(self.__signature_string().encode()).hexdigest()

    @property
    def issued_at(self):
        """Returns the issued at value"""
        return self.__issued_at

    @issued_at.setter
    def issued_at( self, value ):
        self.__issued_at = value

    @property
    def appoinment_date( self ):
        """Returns the vaccination date"""
        return self.__appoinment_date