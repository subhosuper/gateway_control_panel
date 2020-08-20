import subprocess
def connected_ssid():
    result = subprocess.check_output("netsh wlan show interfaces")
    result = result.decode("ascii","ignore")
    result = result.replace("\r","")
    list_form = result.split("\n")
    if result.find("SSID") == -1:
        return "127.0.0.1_NoT_CoNnEcTeD"
    i = 0
    while i < len(list_form):
        if list_form[i].find("SSID") != -1:
            connected_ssid = list_form[i][list_form[i].index(':')+2:len(list_form[i])]
            return connected_ssid
        i += 1