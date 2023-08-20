import unittest
from unittest.mock import patch

from cdek_tracking import CdekClient


class TestCdekClient(unittest.TestCase):
    @patch("requests.post")
    def test_authorize_success(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"access_token": "dummy_token"}

        cdek_client = CdekClient()
        access_token = cdek_client.authorize()

        self.assertEqual(access_token, "dummy_token")

    @patch("requests.post")
    def test_authorize_failure(self, mock_post):
        mock_post.return_value.status_code = 400

        cdek_client = CdekClient()
        result = cdek_client.authorize()

        self.assertEqual(result, ("Ошибка при выполнении запроса авторизации:", 400))

    @patch("requests.get")
    def test_get_order_info_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_response_json = {
            "entity": {
                "statuses": [
                    {
                        "city": "City",
                        "date_time": "2023-08-03T12:34:56+0300",
                        "name": "Status",
                    }
                ]
            }
        }
        mock_get.return_value.json.return_value = mock_response_json

        cdek_client = CdekClient()
        cdek_client.access_token = "dummy_token"
        order_info = cdek_client.get_order_info("dummy_cdek_number")

        expected_info = (
            "Информация о заказе:\n"
            "03.08.2023 в 12:34\n"
            "Город/населенный пункт: City\n"
            "Статус заказа: Status"
        )
        self.assertEqual(order_info, expected_info)

    @patch("requests.get")
    def test_get_order_info_failure(self, mock_get):
        mock_get.return_value.status_code = 400
        mock_response_json = {"error": "Some error message"}
        mock_get.return_value.json.return_value = mock_response_json

        cdek_client = CdekClient()
        cdek_client.access_token = "dummy_token"
        result = cdek_client.get_order_info("dummy_cdek_number")

        self.assertEqual(
            result,
            ("Ошибка при получении информации о заказе:", 400, mock_response_json),
        )


if __name__ == "__main__":
    unittest.main()
