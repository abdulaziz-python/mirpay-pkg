# MirPay Python Klienti

MirPay to'lov API bilan ishlash uchun professional, samarali va foydalanishga qulay Python paketi. Ushbu paket dasturchilarga balansni olish va to'lov callback'larini qayta ishlashni soddalashtiradi, mustahkam xato boshqaruvi va batafsil logging tizimi bilan.

## Xususiyatlar
- **Balans so'rovi**: MirPay API orqali hisob balansini tezkor olish.
- **To'lov callback'lari**: Muvaffaqiyatli va muvaffaqiyatsiz to'lov natijalarini xavfsiz qayta ishlash.
- **Xato boshqaruvi**: HTTP, ulanish, timeout va ma'lumot format xatolari uchun aniq ishlov berish.
- **Batafsil logging**: Har bir so'rov va xato uchun aniq log qaydlar.
- **Moslashuvchanlik**: Timeout va callback URL sozlamalari bilan moslashuvchan interfeys.

## O'rnatish

### Python Paketi sifatida
PyPI orqali o'rnatish (agar nashr qilingan bo'lsa):
```bash
pip install mirpay
```

Yoki fayllarni qo'lda o'rnatish:
1. Quyidagi fayllarni `mirpay-pkg` jildiga joylashtiring:
   - `mirpay/__init__.py`
   - `mirpay/client.py`
   - `setup.py`
   - `README.md`
   - `.gitignore`
2. Jildga o'ting va paketni o'rnating:
```bash
cd mirpay-pkg
python setup.py sdist bdist_wheel
pip install dist/mirpay-1.5.0-py3-none-any.whl
```

### GitHub Repositoriy sifatida
1. Repositoriyni klonlash:
```bash
git clone https://github.com/abdulaziz-python/mirpay-pkg.git
cd mirpay-python
```
2. Paketni o'rnatish:
```bash
python setup.py install
```

## Talablar
- Python 3.7 yoki undan yuqori
- `requests` kutubxonasi (>=2.28.0)
- MirPay API tokeni (dashboarddan oling)
- (Ixtiyoriy) To'lov natijalari uchun callback URL

## Foydalanish

### 1. Klientni ishga tushirish
```python
from mirpay import MirPayClient
client = MirPayClient(
    token="sizning-api-tokeningiz",
    callback_url="https://sizning-callback-url.com",
    timeout=15
)
```

### 2. Balansni olish
```python
try:
    balance = client.get_balance()
    print(balance)
except MirPayError as e:
    print(f"Xato: {e}")
```

### 3. To'lov callback'ini qayta ishlash
```python
callback_data = {
    "payid": "12345",
    "summa": "100.00",
    "status": "success",
    "comment": "To'lov yakunlandi",
    "chek": "check123",
    "fiskal": "fiscal456",
    "sana": "2025-07-15T22:00:00"
}
try:
    result = client.handle_payment_callback(callback_data)
    print(result)
except MirPayError as e:
    print(f"Xato: {e}")
```

### 4. Klientni yopish
```python
client.close()
```

## Sozlash
1. **API Token**: MirPay dashboardidan Bearer tokenini oling.
2. **Callback URL**: MirPay dashboardidagi "Kassa ma'lumotlarini tahrirlash" bo'limida muvaffaqiyatli va muvaffaqiyatsiz to'lovlar uchun callback URL'larni sozlang.
3. **Logging**: Debugging uchun loggingni sozlang:
```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.logHandler('mirpay.log', when='midnight', backupCount=7)
    ]
)
```

## Logging
- **DEBUG**: So'rovlarning boshlanishi va batafsil ma'lumotlar.
- **INFO**: Muvaffaqiyatli amallar (masalan, balans olish, callback qayta ishlash).
- **WARNING**: Noto'g'ri, lekin davom etish mumkin bo'lgan holatlar (masalan, noto'g'ri status).
- **ERROR**: Xatolar (HTTP, ulanish, format xatolari).
- Loglar `mirpay.log` fayliga yoziladi va har kuni yangilanadi.

## Eslatmalar
- **Balans so'rovi**: API hech qanday javob tanasini qaytarmaydi (dokumentatsiyaga ko'ra).
- **Callback vaqtlari**: Muvaffaqiyatli to'lovlar 1 daqiqada, muvaffaqiyatsizlar 15 daqiqada yuboriladi.
- **To'lov muddati**: To'lovlar 15 daqiqadan so'ng avtomatik bekor qilinadi, havola yaroqsiz bo'ladi.

## Xato Boshqaruvi
- **MirPayError**: API so'rovlaridagi barcha xatolar uchun maxsus xato klassi.
- **Xato turlari**:
  - HTTP xatolari (masalan, 401, 500) va ularning matni.
  - Timeout xatolari (so'rov vaqti tugashi).
  - Ulanish xatolari (serverga ulanib bo'lmaslik).
  - Ma'lumot format xatolari (summa yoki sana noto'g'ri bo'lsa).
- Barcha xatolar log fayliga yoziladi.

## Telegram Kanal
Python yangiliklari, maslahatlar va yangilanishlar uchun [**@pytthonnews_uzbekistan**](https://t.me/pytthonnews_uzbekistan) Telegram kanaliga obuna bo'ling!

## Litsenziya
MIT Litsenziyasi

## Hissa Qo'shish
Hissa qo'shmoqchi bo'lsangiz, GitHub'da pull request yuboring yoki muammo oching: [mirpay-python](https://github.com/abdulaziz-python/mirpay-pkg).

## Qo'llab-quvvatlash
Muammolar bo'yicha: https://t.me/ablaze_coder
Rasmiy hujjatlar: [MirPay API Hujjatlari](https://documenter.getpostman.com/view/37255689/2sAXjM3BTW)
