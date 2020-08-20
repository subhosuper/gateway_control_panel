import subprocess

def withoutspace(variable):
    ssid_without_space = variable[variable.index(':')+2:len(variable)]
    if ssid_without_space == '':
        ssid_without_space = 'Hidden Network'
    return ssid_without_space

def ssid_list1():
    results = subprocess.check_output(["netsh", "wlan", "show", "network", "mode=Bssid"])
    results = results.decode("ascii","ignore")
    results = results.replace("\r","")
    ls = results.split("\n")

    temp_ssid = ''
    ssid_dict = {}
    i = 0
    while i < len(ls):
        if ls[i].find('Signal') != -1:                                          #checks for Signal in line
            signal = withoutspace(ls[i]).strip()
            signal = signal[:-1]
            signal = int(signal)
            if signal > ssid_dict[temp_ssid]:
                ssid_dict[temp_ssid] = signal
        elif ls[i].find('BSSID') == -1 and ls[i].find('SSID')!=-1:              #checks for SSID in line not BSSID
            temp_ssid = withoutspace(ls[i])
            ssid_dict[temp_ssid] = 0
        i += 1
    print(ssid_dict)                    #for testing
    # return ssid_dict
ssid_list1()