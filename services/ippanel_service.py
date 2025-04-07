from ippanel import Client, Error, HTTPError
import re

class IPPANELService:
    def __init__(self, api_key):
        self.client = Client(api_key)
        # self.sender = "+985000404223"
        self.sender = "+983000505"
        self.description = "description"

    def _validate_phone(self, phone):
        """اعتبارسنجی شماره تلفن"""
        return re.match(r'^(\+98|0)?9\d{9}$', phone)

    def _format_phone(self, phone):
        """تبدیل شماره به فرمت بین‌المللی"""
        if phone.startswith('0'):
            return phone[1:]  # حذف صفر ابتدایی
        elif phone.startswith('+98'):
            return phone[3:]  # حذف کد کشور
        return phone

    def send_sms(self, recipients, message):
        """
        ارسال پیامک با اعتبارسنجی کامل
        """
        try:
            # اعتبارسنجی و فرمت‌دهی شماره‌ها
            validated_numbers = []
            for phone in recipients:
                if not self._validate_phone(phone):
                    raise ValueError(f"شماره نامعتبر: {phone}")
                validated_numbers.append(self._format_phone(phone))
            print(validated_numbers)

            # تبدیل به رشته با جداکننده کاما
            # validated_numbers = ",".join(validated_numbers)

            print(self.sender)

            response = self.client.send(
                self.sender,
                validated_numbers,
                message,
                self.description
            )
            print(response)
            return {
                'status': 'success',
                'message_id': response
            }
        except ValueError as e:
            return {
                'status': 'error',
                'code': 'VALIDATION_ERROR',
                'message': str(e)
            }
        except Error as e:
            return {
                'status': 'error',
                'code': 'IPPANEL_ERROR',
                'message': f"خطای ippanel: {e.message}"
            }
        except Exception as e:
            return {
                'status': 'error',
                'code': 'UNKNOWN_ERROR',
                'message': f"خطای ناشناخته: {str(e)}"
            }