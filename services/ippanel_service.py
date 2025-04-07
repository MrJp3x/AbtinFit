from ippanel import Client, Error, HTTPError

class IPPANELService:
    def __init__(self, api_key):
        self.client = Client(api_key)
        self.sender = "+9810001"

    def send_sms(self, recipients, message):
        try:
            response = self.client.send(
                self.sender,
                recipients,
                message,
                "پیام از برنامه ماساژ"
            )
            return response
        except Error as e:
            raise Exception(f"خطای ippanel: {e.message}")
        except HTTPError as e:
            raise Exception(f"خطای شبکه: {str(e)}")