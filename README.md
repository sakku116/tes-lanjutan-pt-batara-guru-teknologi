# URL Shortner
## how to run the server
- jangan lupa install semua requirements yang ada di requirements.txt
- jalankan migrate.bat,
- jalankan shell.bat,
- pada shell, paste kode dibawah
```
from django.contrib.contenttypes.models import ContentType
ContentType.objects.all().delete()
quit()
```
- jalankan loaddata.bat
- terakhir, jalankan server dengan `python manage.py runserver` 

## default accounts
- admin:admin
- demo:demo123