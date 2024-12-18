import unittest
from mock import patch, MagicMock
from app import app, tabla, precios


class TestFlaskAPI(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    @patch('app.tabla')
    def test_index_route(self, mock_tabla):
        # Mock tabla to avoid actual DBF file operations
        mock_tabla.__len__.return_value = 5
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'PRUEBA.DBF', response.data)
        self.assertIn(b'5', response.data)

    @patch('app.tabla')
    def test_buscar_route_found(self, mock_tabla):
        # Mock tabla to simulate a record found
        record_mock = MagicMock()
        record_mock.NUMERO = "123"
        record_mock.DESCRI = "Test Product"
        record_mock.P_VENTA = 100.0
        record_mock._recnum = 0
        mock_tabla.__iter__.return_value = iter([record_mock])

        response = self.client.get('/buscar/123')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'"codigo":"123"', response.data)
        self.assertIn(b'"descripcion":"Test Product"', response.data)
        self.assertIn(b'"precio":100.0', response.data)

    @patch('app.tabla')
    def test_buscar_route_not_found(self, mock_tabla):
        # Mock tabla to simulate no matching record
        mock_tabla.__iter__.return_value = iter([])

        response = self.client.get('/buscar/999')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'"status":"Not found"', response.data)

    @patch('app.tabla')
    def test_cambiar_route_success(self, mock_tabla):
        # Mock tabla to simulate updating a record
        record_mock = MagicMock()
        record_mock.P_VENTA = 100.0
        record_mock.NUMERO = "123"
        record_mock.DESCRI = "Test Product"
        record_mock._recnum = 1

        mock_tabla.__getitem__.return_value = record_mock
        mock_tabla.__len__.return_value = 1

        response = self.client.put('/cambiar/1/200.0')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'"status":"success"', response.data)
        self.assertIn(b'"precio":200.0', response.data)

        # Check that the price update was logged in the global "precios"
        self.assertEqual(len(precios), 1)
        self.assertEqual(precios[0][4], 200.0)

    @patch('app.tabla')
    def test_cambiar_route_failure(self, mock_tabla):
        # Mock tabla to raise an exception
        mock_tabla.__getitem__.side_effect = Exception("Record not found")

        response = self.client.put('/cambiar/99/200.0')
        self.assertEqual(response.status_code, 500)
        self.assertIn(b'"status":"error"', response.data)
        self.assertIn(b'Record not found', response.data)

if __name__ == '__main__':
    unittest.main()
