import http.client
import sys
import json
import myconfig

# input your main zone_id
# output the id of your zone_id (just limited to your Bearer token or for all yours dns zone) 


def getInfo(zone_id,subdomain):

    conn = http.client.HTTPSConnection("api.cloudflare.com")



    bearer ="QDvC27t_DrMiwIhdRjxSR2NPK42Q0x0tniJPqIAm"
    x_auth_email= "cinerip@ymail.com"
    x_auth_key= "bb3dde5ba242b87c5744f07f081396bd39da0"

    headers = {
    'Content-Type': "application/json",
    'Authorization': "Bearer "+ bearer,
    'X-Auth-Email': x_auth_email,
    'X-Auth-Key': x_auth_key

    }
   
    # dns_record_id

    # ALL ZONE DNS Records (generic)
    # conn.request("GET", "/client/v4/zones/"+zone_id, headers=headers)

    # SINGLE ZONE DNS Records
    # Structure
    # https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records

    conn.request("GET", "/client/v4/zones/"+zone_id+"/dns_records", headers=headers)
    res = conn.getresponse()
    json_data = res.read()
    #print(json_data.decode("utf-8")+"\n\n")
    # output Json Pretty Print
    json_object = json.loads(json_data)
    
    # all output
    json_formatted_str = json.dumps(json_object, indent=2)
    print("\n\n********** Start Json output for other info **********")
    print(json_formatted_str)
    print("\n\n********** End Json output **********\n\n")


    # output just the record results> id where name = 'your subdomain name'

    for result in json_object["result"]:
         if result["name"] == subdomain:
            print("ID for your subdomain "+subdomain+ ":", result["id"]+"\n")
            print ("Use this ID for setDns.py to update your dns record for "+subdomain+"\n")
            print ("Current IP for "+subdomain+" :  "+result["content"]+"\n")
            break
    else:
            print("No subdomain name found for "+ subdomain +"\n")



    return




if __name__ == "__main__":
    if ( not myconfig.bearer or not myconfig.x_auth_email or not myconfig.x_auth_key or not myconfig.subdomain or not myconfig.zone_id):
        print("Configuration Error : missing some configuration, check myconfig.py and add bearer/x_auth_email/x_auth_key/subdomain/zone_id tokens")
        sys.exit(-1)
    else:
        print("[+] Requesting all dns info for your zone_id and subdomain ...\n")
        getInfo(myconfig.zone_id,myconfig.subdomain)