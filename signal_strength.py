import subprocess

def withoutspace(variable):
    ssid_without_space = variable[variable.index(':')+2:len(variable)]
    if ssid_without_space == '':
        ssid_without_space = 'Hidden Network'
    return ssid_without_space

def ssid_list():
    results = subprocess.check_output(["netsh", "wlan", "show", "network", "mode=Bssid"])
    results = results.decode("ascii","ignore")
    results = results.replace("\r","")
    ls = results.split("\n")

    temp_ssid = ''
    ssid_dict = []
    keys = ['name','auth','signal']
    temp_list = []
    i = 0
    while i < len(ls):
        if ls[i].find('BSSID') == -1 and ls[i].find('SSID')!=-1:             #checks for SSID in line not BSSID
            ssid_dict.append(dict(zip(keys, temp_list)))
            temp_list = []
            temp_ssid = withoutspace(ls[i])
            # ssid_dict[temp_ssid] = 0
            temp_list.append(temp_ssid)
        elif ls[i].find('Authentication') != -1:
            temp_ssid = withoutspace(ls[i])
            temp_list.append(temp_ssid)
            temp_list.append(0)
        elif ls[i].find('Signal') != -1:                                          #checks for Signal in line
            signal = withoutspace(ls[i]).strip()
            signal = signal[:-1]
            signal = int(signal)
            if len(temp_list) == 3 and signal > temp_list[2]:
                temp_list[2] = signal
        i += 1
    ssid_dict.append(dict(zip(keys, temp_list)))
    ssid_dict.remove(ssid_dict[0])
    # print(ssid_dict)                    #for testing
    return ssid_dict