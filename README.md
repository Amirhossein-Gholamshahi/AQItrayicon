# AQItrayicon
### ابتدا کتابخانه های زیر را نصب کنید
``` pip install winotify ```  
``` pip install pystray ``` \
``` pip install requests ``` \
``` pip install beautifulsoup4 ```


## هدف کلی برنامه اطلاع از مقدار شاخص کیفیت هوای تهران می باشد.

با اجرای چند خط کد **web scrapping** ساده با استفاده از کتابخانه **beautifulsoup4** مقدار شاخص را از سایت [کنترل کیفیت هوا](https://airnow.tehran.ir/) می توان پیدا کرد.

**توجه:** در خطوط ابتدایی برنامه به جز کتابخانه های دکر شده، **import** هایی را می بینید که برای تبدیل کد به **exe** از آن ها استفاده شده است، بنابراین برای اجرای برنامه در کنسول نیازی به این کتابخانه ها نخواهید داشت.
---
اگر برنامه با موفقیت اجرا شود، یه **tray icon** در قسمت پایین سمت راست صفحه خود مشاهده خواهید کرد. با راست کلیک کردن روی لوگو این برنامه، منوی آن باز می شود که شامل گزینه های مختلفی است. مثلا اگر روی **Get current AQI** کلیک کنید، مقدار فعلی شاخص هوای تهران را به صورت یک **Notification** برای شما ارسال می کند.

برای اینکه برنامه همواره اجرا شود، باید هر یک از گزینه های منو را به شکل یک **process** تعریف کرد و با **multiprocessing** به گونه ای عمل کرد که منو همواره در دسترس باشد و با کلیک کردن هر گزینه برنامه تمام نشود.

اگر به هر دلیلی خواستید از برنامه خارج شوید، گزینه Exit تمامی **process** ها را **terminate** می کند و از برنامه خارج می شود.













