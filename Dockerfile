FROM python:3.8

# Copia lo script Python all'interno del container
COPY getInfo.py /app/getInfo.py
COPY setDns_docker.py /app/setDns_docker.py
COPY myconfig_docker.py /app/myconfig_docker.py
COPY requirements.txt /app/requirements.txt

# Verifica che il file requirements.txt sia stato copiato correttamente
RUN ls /app

# Installa le dipendenze Python se necessario
RUN pip install -r /app/requirements.txt

# Definisci il comando predefinito per eseguire lo script Python
CMD ["python", "/app/setDns_docker.py"]

# example run
# docker run -e bearer="QDvC27t_DrMiwIhdRjxSR2NPK42Q0x0tniJPqIAm" -e x_auth_email="cinerip@ymail.com" -e x_auth_key="bb3dde5ba242b87c5744f07f081396bd39da0" -e subdomain="mydns.itzunami.net" -e zone_id="348a14063c853cb1ab025e3dd8a130c1" -e dns_record_id="750b78eb031c868105bf7d5e849bab7e" -e time_repeat="60" mydns-app 