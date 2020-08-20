import subprocess

auth_type = ""
encryp_type = ""
choice = 'static' #or dynamic && get from UI

def get_auth(auth):
    global auth_type
    auth_type= auth[auth.index(':')+2:len(auth)]
    auth_type = auth_type.lower()
    return auth_type
    
def get_encryp(encryp):
    global encryp_type
    encryp_type = encryp[encryp.index(':')+2:len(encryp)-1]
    encryp_type = encryp_type.upper()
    return encryp_type

def connect(SSID,password):
    #password = "0123456789"       #get from UI
    #SSID = 'DYS08'            #get from UI
    
       
    results = subprocess.check_output(["netsh", "wlan", "show", "network", "mode=Bssid"])
    results = results.decode("ascii")
    results = results.replace("\r","")
    ls = results.split("\n")
    i = 0
    while i < len(ls):
        if ls[i].find(SSID) != -1:
            get_auth(ls[i+2])
            get_encryp(ls[i+3])
            break
        i += 1

    profile = '<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">  <name>'+SSID+'</name>  <SSIDConfig>    <SSID>      <name>'+SSID+'</name>    </SSID>    <nonBroadcast>false</nonBroadcast>  </SSIDConfig>  <connectionType>ESS</connectionType>  <connectionMode>auto</connectionMode>  <autoSwitch>false</autoSwitch>  <MSM>    <security>      <authEncryption>        <authentication>'+auth_type+'</authentication>        <encryption>'+encryp_type+'</encryption>        <useOneX>false</useOneX>      </authEncryption>      <sharedKey>        <keyType>networkKey</keyType>        <protected>false</protected>        <keyMaterial>'+password+'</keyMaterial>      </sharedKey>      <keyIndex>0</keyIndex>    </security>  </MSM></WLANProfile>'
    # profile = '<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">  <name>'+SSID+'</name>  <SSIDConfig>    <SSID>      <name>'+SSID+'</name>    </SSID>    <nonBroadcast>false</nonBroadcast>  </SSIDConfig>  <connectionType>ESS</connectionType>  <connectionMode>auto</connectionMode>  <autoSwitch>false</autoSwitch>  <MSM>    <security>      <authEncryption>        <authentication>'+"WPA2PSK"+'</authentication>        <encryption>'+"AES"+'</encryption>        <useOneX>false</useOneX>      </authEncryption>      <sharedKey>        <keyType>passPhrase</keyType>        <protected>false</protected>        <keyMaterial>'+password+'</keyMaterial>      </sharedKey>      <keyIndex>0</keyIndex>    </security>  </MSM></WLANProfile>'
    filename = "profile_"+SSID+".xml"
    f = open(filename,"w+")
    f.write(profile)
    f.close()

    add_profile = 'netsh wlan add profile filename="profile_'+SSID+'.xml"'
    print(add_profile)
    subprocess.call(add_profile,shell=True)
    connect_wifi = 'netsh wlan connect ssid="'+SSID+'" name="'+SSID+'"'
    print(connect_wifi)
    subprocess.call(connect_wifi,shell=True)
    
def IP():
    if choice == 'static':
        print("ask for IP")     #store IP provided by user
    else:
        subprocess.call("netsh interface ip set address \"Wi-Fi\" dhcp")
        results = subprocess.check_output(["ipconfig"])
        results = results.decode("ascii","ignore")
        results = results.replace("\r","")
        ls = results.split("\n")
        results = ls[13]
        dynamic_ip = results[results.index(':')+2:len(results)]         #store dynamic_ip         
        
#if __name__ == '__main__':
#    main()
