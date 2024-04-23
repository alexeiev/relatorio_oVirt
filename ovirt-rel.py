#!/usr/bin/env python3.6
'''
Definições:
necessario gerar relatório das vms hospedadas nos dois clusters oVirt
e devem conter a seguinte informação:

Nome; CPU; RAM; OS; DISCO


Ref.: https://www.ovirt.org/documentation/doc-Python_SDK_Guide/#Installing_the_Software_Development_Kit

'''
import sys
import os
import csv

import ovirtsdk4 as sdk
from dotenv import load_dotenv

load_dotenv()

## Validando as variáveis no ficheiro .env
try: 
    USERNAME = os.environ["USERNAME"]
    PASSWORD = os.environ["PASSWORD"]
    SITE     = os.environ["SITE"]
    FILE     = os.environ["FILE"]
except:
    print(f"[ERROR]: Validar ficheiro com as variáveis")
    sys.exit(1)

if os.path.isfile(FILE):
    print(f"O ficheiro {FILE} já existe na diretoria local")
    sN = input("Deseja sobrescrever? [sN] ")
    if sN.upper() == "N":
        FILE = input("Digite o nome do fichero: ")


#Criando conexão com o oVirt
try:
    connection = sdk.Connection(
    url=f"https://{SITE}/ovirt-engine/api",
    username=USERNAME,
    password=PASSWORD,
    ca_file='ca.pem',
    )
except:
    print("[ERROR] Problema na conexão com o oVirt")
    sys.exit(1)

vms_service = connection.system_service().vms_service()

#buscando lista de vms
vms = vms_service.list()
#vms = vms_service.list(search='name=ultvvi6*', max=30)


count_vms = 0

#Print cabeçalho
TITLE = [ 'Nome', 'CPU_sockets',  'CPU_cores', 'Memory(M)', 'Sistema', 'Disco(G)', 'Status']

with open(FILE, 'w') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=";")
    csvwriter.writerow(TITLE)
    for vm in vms:
        #Coletando informacao do disco
        vm_service = vms_service.vm_service(vm.id)
        disk_attachments = vm_service.disk_attachments_service().list()
        disk_size = 0
        for disk in disk_attachments:
            #print(f"[DEBUG] - Nome: {disk}")
            disk = connection.follow_link(disk.disk)
            if disk.provisioned_size is not None:
                disk_size += disk.provisioned_size
        
        #validando variaveis
        #verificando se o host tem informações do SO
        if vm.guest_operating_system is not None:
            sistema = f"{vm.guest_operating_system.distribution} {vm.guest_operating_system.version.full_version}"
        else:
            sistema = "None"

        # print(
        #     f"{vm.name};{vm.cpu.topology.sockets };"
        #     f"{vm.cpu.topology.cores };{int(vm.memory/1024/1024)};"
        #     f"{sistema};{int(disk_size/1024/1024/1024)};{vm.status}"
        # )
        memory = int(vm.memory/1024/1024)
        disk   = int(disk_size/1024/1024/1024)
        ROW = [vm.name, vm.cpu.topology.sockets, vm.cpu.topology.cores, 
                memory, sistema, disk, vm.status
            ]
        csvwriter.writerow(ROW)
            
        count_vms += 1

print(f"Total de vms listadas: {count_vms} no ambiente {SITE}")
connection.close()