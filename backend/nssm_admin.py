# Admin for NSSM Windows Service

import subprocess
import time
import sys

def win_command(*args):
    try:
        process = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        stdout, stderr = process.communicate()
    except Exception as e:
        print "Error:", e
        time.sleep(5)
        sys.exit()


    return stdout, stderr



# NSSM Path
cmd_nssm = "C:/nssm-2.24/win64/nssm.exe"
# NSSM Service
arg_service = "actualizador_precios2"
# Browser executable
cmd_browser = "C:/Program Files/Google/Chrome/Application/chrome.exe"
# HTTP for browser 
arg_browser = "http://localhost:8080/"


print "\n\n*** Servidor Actualizador de Precios ***\n"


stdout, stderr = win_command(cmd_nssm, "status", arg_service)



if "SERVICE_RUNNING" in stdout:
    print "Servidor corriendo...\n"
    print '1 - Detener'
    print '2 - Abrir estado en navegador'
    print '* - Salir\n'
    opt = raw_input()
    if opt == '1':
        print '\nDeteniendo Servidor...',
        stdout, stderr = win_command(cmd_nssm, "stop", arg_service)
        print '=> Detenido'
        time.sleep(3)
    elif opt == '2':
        print '\nAbriendo Navegador...'            
        stdout, stderr = win_command(cmd_browser, arg_browser)
        if stderr:
            print 'Error:',
            print stderr
            time.sleep(5)

       
        
if "SERVICE_STOPPED" in stdout:
    print "Iniciando Servidor...",
    stdout, stderr = win_command(cmd_nssm, "start", arg_service)
    print '=> Iniciado'
    print '\nAbriendo Navegador...',
    time.sleep(2)    
    stdout, stderr = win_command(cmd_browser, arg_browser)    
    if stderr:
        print 'Error:',
        print stderr
        time.sleep(5)
    

