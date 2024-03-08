import os

# configuration file

# get your Bearer id at https://dash.cloudflare.com/profile/api-tokens -> create Token for just a Read DNS (single domain)
# get your X-Auth-Email at https://dash.cloudflare.com/profile/api-tokens
# get your Auth-Key at https://dash.cloudflare.com/profile/api-tokens


# take input from docker , or set manually writing the default value
# example bearer = os.environ.get('BEARER', 'QDvC27t_DrMiwIhdRjxSR2NPK42Q0x0tniJPqIAm')

bearer = os.environ.get('bearer', '')
x_auth_email= os.environ.get('x_auth_email', '')
x_auth_key= os.environ.get('x_auth_key', '')



# your subdomain in which we change ip
subdomain = os.environ.get('subdomain', '')
# your current general zone_id of your main account
zone_id= os.environ.get('zone_id', '')

# the id of your subdomain record
# getInfo.py  > get dns_record_id from for the selected subdomain 
dns_record_id = os.environ.get('dns_record_id', '')

# default 10 min
time_repeat = os.environ.get('time_repeat', '600')








