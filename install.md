#just random note

install visual studio code
install python -y
force re-install if needed python -m pip install --upgrade --force-reinstall pip
Windows venv 
and /script/activate or Ubuntu source
install mongodb for windows or ubuntu

        Ubuntu
        sudo apt install python3-venv -y

        python3 -m venv vvv
        source vvv/bin/activate
        (replace vvv with your path)

        sudo apt-get install -y mongodb-org
        sudo systemctl start mongod
        # start MongoDB
        mongo or mongod
        # install pymongo
        python3 -m pip install pymongo -y

On Visual Studio code change the Env to the current path /myDNS/bin/ otherwise you will get some error importing pymongo etc
when venv in terminal is activated load all module 
pip install -r requirements.txt
try manually if getInfo.py and setInfo.py works on terminal (inside visual studio code) 

FOR CRONJOB on ubuntu
install nano editor (should already exist)
first chmod file
chmod +x /percorso/dello/script.py

to edit the cron list
crontab -e
*/10 * * * * /your/path/myDNS/bin/python3 /your/path/setDns.py
note : use pyhon3 of your venv not the generic

for debug append >> out.txt  2>&1
for example 1 min
*/1 * * * * /your/path/myDNS/bin/python3 /your/path/setDns.py >> out.txt  2>&1
with out.txt on home dir log 

//for docker
venv activate
pip freeze > requirements.txt
Dockerfile same dir
docker build -t mydns-app .
docker tag mydns-app:latest itzunami/mydns:latest
docker push itzunami/mydns:latest

down
docker pull itzunami/mydns
run example 600 = 10 min -d background -t logs bash
docker run -e bearer="QDvC27t_DrMiwIhdRjxSR2NPK42Q0x0tniJPqIAm" -e x_auth_email="email------------" -e x_auth_key="bb3dde5ba242b87c5744f07f081396bd39da0" -e subdomain="mydns.itzunami.net" -e zone_id="348a14063c853cb1ab025e3dd8a130c1" -e dns_record_id="750b78eb031c868105bf7d5e849bab7e" -time_repeat="600"  -t -d  itzunami/mydns

docker serivice for at startup
sudo nano /etc/systemd/system/mydns.service
[Unit]
Description=MyDNS Container
Requires=docker.service
After=docker.service

[Service]
Restart=always
ExecStart=/usr/bin/docker run -e bearer="QDvC27t_DrMiwIhdRjxSR2NPK42Q0x0tniJPqIAm" -e x_auth_email="email@ymail.com" -e x_auth_key="bb3dde5ba242b87c5744f07f081396bd39da0" -e subdomain="mydns.itzunami.net" -e zone_id="348a14063c853cb1ab025e3dd8a130c1" -e dns_record_id="750b78eb031c868105bf7d5e849bab7e" -t -d itzunami/mydns

[Install]
WantedBy=multi-user.target

sudo systemctl enable mydns.service

sudo systemctl start mydns.service
sudo systemctl status mydns.service