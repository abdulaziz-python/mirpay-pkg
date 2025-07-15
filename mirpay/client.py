import requests
from typing import Dict, Optional, Any
import logging
from urllib.parse import urlencode
from datetime import datetime

# Maxsus xato klassi MirPay API bilan ishlashda xatolarni boshqarish uchun
class MirPayError(Exception):
    pass

# MirPay API bilan ishlash uchun asosiy klient klassi
class MirPayClient:
    # API asosiy manzili
    BASE_URL = "https://mirpay.uz/api"

    def __init__(self, token: str, callback_url: Optional[str] = None, timeout: int = 10):
        """
        MirPay klientini ishga tushiradi.

        Args:
            token (str): API autentifikatsiyasi uchun Bearer token.
            callback_url (Optional[str]): To'lov natijalari uchun callback URL (ixtiyoriy).
            timeout (int): HTTP so'rovlar uchun kutish vaqti (sekundlarda).
        """
        # Tokenning to'g'ri ekanligini tekshirish
        if not token or not isinstance(token, str):
            raise MirPayError("Token bo'sh yoki noto'g'ri formatda")

        self.token = token
        self.callback_url = callback_url
        self.timeout = timeout
        # HTTP sessiya yaratish va sarlavhalarni sozlash
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "MirPayPythonClient/1.5.0"
        })
        # Logging sozlash
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"MirPayClient ishga tushdi: token={token[:4]}..., callback_url={callback_url}")

    def get_balance(self) -> Dict[str, Any]:
        """
        Hisob balansini olish uchun MirPay API ga so'rov yuboradi.

        Returns:
            Dict[str, Any]: API javobi, holat va vaqt belgisi.

        Raises:
            MirPayError: Agar so'rov muvaffaqiyatsiz bo'lsa.
        """
        try:
            self.logger.debug("Balans so'rovi yuborilmoqda")
            response = self.session.get(f"{self.BASE_URL}/balans", timeout=self.timeout)
            response.raise_for_status()
            self.logger.info("Balans muvaffaqiyatli olindi")
            return {
                "status": "success",
                "data": response.json() if response.text else {},
                "timestamp": datetime.now().isoformat()
            }
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTP xatosi: status={e.response.status_code}, xabar={e.response.text}")
            raise MirPayError(f"HTTP xatosi: {e.response.status_code} - {e.response.text}")
        except requests.exceptions.Timeout:
            self.logger.error("So'rov vaqti tugadi")
            raise MirPayError("API so'rovi vaqti tugadi")
        except requests.exceptions.ConnectionError:
            self.logger.error("Ulanish xatosi: API serveriga ulanib bo'lmadi")
            raise MirPayError("API bilan ulanishda xato")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"API so'rovida umumiy xato: {str(e)}")
            raise MirPayError(f"API so'rovida xato: {str(e)}")

    def handle_payment_callback(self, callback_data: Dict[str, str]) -> Dict[str, Any]:
        """
        MirPay dan kelgan to'lov callback ma'lumotlarini qayta ishlaydi.

        Args:
            callback_data (Dict[str, str]): MirPay tomonidan yuborilgan callback ma'lumotlari.

        Returns:
            Dict[str, Any]: Qayta ishlangan ma'lumotlar va vaqt belgisi.

        Raises:
            MirPayError: Agar majburiy maydonlar yetishmasa yoki format xato bo'lsa.
        """
        # Majburiy maydonlarni tekshirish
        required_fields = ["payid", "summa", "status", "comment", "chek", "fiskal", "sana"]
        missing_fields = [field for field in required_fields if field not in callback_data or not callback_data[field]]
        if missing_fields:
            self.logger.error(f"Yetiqmayotgan maydonlar: {missing_fields}")
            raise MirPayError(f"Yetiqmayotgan maydonlar: {missing_fields}")

        # Ma'lumotlar formatini tekshirish
        try:
            float(callback_data["summa"])
            datetime.fromisoformat(callback_data["sana"].replace("Z", "+00:00"))
            if callback_data["status"] not in ["success", "failed"]:
                self.logger.warning(f"Noto'g'ri status qiymati: {callback_data['status']}")
        except ValueError as e:
            self.logger.error(f"Ma'lumot formati xato: {str(e)}")
            raise MirPayError(f"Ma'lumot formati xato: {str(e)}")

        self.logger.info(f"To'lov callback'i qayta ishlandi: payid={callback_data['payid']}, status={callback_data['status']}")
        return {
            "status": "processed",
            "data": {field: callback_data[field] for field in required_fields},
            "timestamp": datetime.now().isoformat()
        }

    def close(self):
        """HTTP sessiyani yopadi va resurslarni tozalaydi."""
        self.session.close()
        self.logger.info("MirPayClient sessiyasi yopildi")
