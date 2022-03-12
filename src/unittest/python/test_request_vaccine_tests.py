import unittest

from uc3m_care import VaccineManager
from uc3m_care import VaccineManagementException


class MyTestCase(unittest.TestCase):

    """def test_something( self ):
        #self.assertEqual(True, False)
        self.assertEqual(True, True)"""

    def test_request_vaccination_id_ok( self ):
        """Test de la funcion request_vaccination_id"""
        my_request = VaccineManager()

        value = my_request.request_vaccination_id("bb5dbd6f-d8b4-413f-8eb9-dd262cfc54e0", "Regular", "Carmen Carrero",
                                                  "123456789", "22")
        self.assertEqual("3467d3fbe384b32f2629074e7db3dd91", value)




if __name__ == '__main__':
    unittest.main()
