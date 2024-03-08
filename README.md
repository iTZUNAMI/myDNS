# myDNS > Cloudflare DNS change for dynamic IP

Problem : you have a dynamic IP and you need a service to get your current IP, for VPN,RPD etc

Solution for newbie : pay some service like no-ip or dydns with subscription..

My Solution : Free, you need just one domain and use Cloudflare DNS serice (for free) and use this script to update your IP

Just create a subdomain on Cloudflare and update your subdomain.mydomain.com -> your current IP every time you run this python script

## Configuration

> Create a Cloudflare account and add/use your selected web domain

To update IP of your subdomain.mydomain.com we use Clouflare API requests, and you need:

> Add this Tokens on myconfig.py

[-] get your Bearer id at https://dash.cloudflare.com/profile/api-tokens -> create Token for just a Read DNS (single domain)

[-] get your X-Auth-Email at https://dash.cloudflare.com/profile/api-tokens

[-] get your Auth-Key at https://dash.cloudflare.com/profile/api-tokens

[-] add your subdomain name 

[-] add your main domain id (zone_id) take it from the dashboard of cloudflare

[-] add your subdomain record id (dns_record_id) , you can get it using getInfo.py, just run it with others parametres and you will get the dns_records_id of that subdomain

## Req:

[-] Python 

## Usage with python

> getInfo.py 

[ just a script to get your dns_record_id ]

first set your config on myconfig.py (except dns_record_id)

run it and you will get the dns_record_id of your subdomain, add it to configuration file

> setDns.py

[ main script ]

just run it, it will check and update your current IP to your subdomain if needed.

## Tips

You can run for example on your PC every 10 minutes.

On Ubuntu add it to a cron job

To list all cronjob:

> crontab -e

Add this line to run this script every 10 minutes

> */10 * * * * /your/path/myDNS/bin/python3 /your/path/setDns.py

Make sure to chmod that file

chmod +x /your/path/setDns.py



## Docker Container HUB

> docker push itzunami/mydns:latest

run it for example with 600 = 10 min -d background -t logs bash

docker run -e bearer="QDvC27t_DrMiwIhdRjxSR2NPK42Q0x0tniJPqIAm" -e x_auth_email="email------------" -e x_auth_key="bb3dde5ba242b87c5744f07f081396bd39da0" -e subdomain="mydns.itzunami.net" -e zone_id="348a14063c853cb1ab025e3dd8a130c1" -e dns_record_id="750b78eb031c868105bf7d5e849bab7e" -time_repeat="600"  -t -d  itzunami/mydns


If you want to run it at every system reboo add this code on:

sudo nano /etc/systemd/system/mydns.service


[Unit]

Description=MyDNS Container

Requires=docker.service

After=docker.service



[Service]

ExecStart=/usr/bin/docker run -e bearer="QDvC27t_DrMiwIhdRjxSR2NPK42Q0x0tniJPqIAm" -e x_auth_email="email------------" -e x_auth_key="bb3dde5ba242b87c5744f07f081396bd39da0" -e subdomain="mydns.itzunami.net" -e zone_id="348a14063c853cb1ab025e3dd8a130c1" -e dns_record_id="750b78eb031c868105bf7d5e849bab7e" -t -d itzunami/mydns


[Install]

WantedBy=multi-user.target



>then enable the serivce and start it

sudo systemctl enable mydns.service

sudo systemctl start mydns.service


to check status:

sudo systemctl status mydns.service