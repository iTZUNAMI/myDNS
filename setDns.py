import requests
import http.client
import sys
from datetime import datetime
import sqlite3
import json
import myconfig


# connection db [table ips]
conn = sqlite3.connect('ip_database.db')
c = conn.cursor()

# new table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS ip_table (
                id INTEGER PRIMARY KEY,
                local_ip TEXT
            )''')
conn.commit()


def get_public_ip():
    try:
        response = requests.get('https://httpbin.org/ip')
        data = response.json()
        public_ip = data['origin']
        return public_ip
    except Exception as e:
        print("Error getting your public ip:", e)
        return None
   

def updateDNS(ip,zone_id,dns_record_id,x_auth_email,x_auth_key):

   
    conn = http.client.HTTPSConnection("api.cloudflare.com")
    subdomain = "mydns"
    # datetime object containing current date and time > add to comments/note on clouflare
    now = datetime.now()
    # dd/mm/YY H:M:S
    comment = now.strftime("%d/%m/%Y %H:%M:%S")

    # payload : content : new_ip  name : mydns(.domain.com) > just subdomain mydns
    payload = "{\n  \"content\": \" "+ip+" \",\n  \"name\": \""+subdomain+"\",\n  \"proxied\": false,\n  \"type\": \"A\",\n  \"comment\": \"Last update on : "+comment+"\",\n  \"ttl\": 3600\n}"

  

    headers = {
        'Content-Type': "application/json",
        'X-Auth-Email': x_auth_email,
        'X-Auth-Key': x_auth_key

        } 
    
    # tech info : https://developers.cloudflare.com/api/operations/dns-records-for-a-zone-update-dns-record
    # APIs > https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{dns_record_id}

    conn.request("PUT", "/client/v4/zones/"+zone_id+"/dns_records/"+dns_record_id+"", payload, headers)

    res = conn.getresponse()
    json_data = res.read()
    json_object = json.loads(json_data)

    
    if json_object['success'] == True:
        print ("CloudFlare response API : success")

    else:
        print ("CloudFlare response API : error")
        # all output in case of errors
        json_formatted_str = json.dumps(json_object, indent=2)
        #print("\n\n********** API response **********")
        print(json_formatted_str)

    return



def initialize_ip(ip):
    c.execute('SELECT * FROM ip_table')
    existing_document = c.fetchone()
    if existing_document:
        print("SQLite > Document already in the database, nothing to do")
        return
    # insert
    c.execute('INSERT INTO ip_table (local_ip) VALUES (?)', (ip,))
    conn.commit()
    print("SQLite > New IP address inserted successfully")



def read_ip():
    c.execute('SELECT * FROM ip_table')
    document = c.fetchone()
    if document:
        return document[1]  # return IP
    else:
        print("SQLite > Document not found")
        return None


def update_ip(new_ip):
    # update
    c.execute('UPDATE ip_table SET local_ip = ?', (new_ip,))
    conn.commit()
    print("SQLite > IP address updated successfully with : "+new_ip)

    
def clear_collection():
    c.execute('DELETE FROM ip_table')
    conn.commit()
    print("SQLite > All documents deleted")

if __name__ == "__main__":
    print ("\n[-] myDNS \n")
    if (not myconfig.bearer or not myconfig.x_auth_email or not myconfig.x_auth_key or not myconfig.subdomain or not myconfig.zone_id or not myconfig.dns_record_id ):
        print("Configuration Error : missing some configuration, check myconfig.py")
        print("Probably you need to insert dns_record_id. get from -> getInfo.py")
        sys.exit(-1)
    else:
        # first db and a random ip
        initialize_ip('0.0.0.0')

        # my last public ip saved locally (on SQLite)
        last_public_ip=read_ip()
    
        # to empty db collection if needed
        #clear_collection()
        
        # actual public ip of my current connection > using https://httpbin.org/ip service
        current_public_ip = get_public_ip()    
        # for manual/change/test use fixed/random ip
        #current_public_ip = "115.1.3.145" 
        
        # first init
        if last_public_ip == None :
            # save current IP to DB
            update_ip(current_public_ip)
            # and save it also on cloudflare the first time
            updateDNS(current_public_ip,myconfig.zone_id,myconfig.dns_record_id,myconfig.x_auth_email,myconfig.x_auth_key)

        # main controller
        if current_public_ip:
            print("Your current Public IP:", current_public_ip)
            print ("SQLite > Last public IP saved locally:", last_public_ip)
            # if current public ip of my connection is different from last updated ip
            # we have to force a new update on cloudflare
            if (current_public_ip != last_public_ip):
                print ("Updating DNS from old "+last_public_ip+" > " +current_public_ip)
                update_ip(current_public_ip)
                updateDNS(current_public_ip,myconfig.zone_id,myconfig.dns_record_id,myconfig.x_auth_email,myconfig.x_auth_key)
            else:
                print ("No need to update/make new cloudflare request")
        
    conn.close()
else:
        print("Error 404 - Impossible to found your Public IP")


 