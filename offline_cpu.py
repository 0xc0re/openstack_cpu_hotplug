from __future__ import print_function
import sys
import os
from enable_cpu_hotplug import modify_vm_xml, catch_nova_db_password, modify_db_vcpu
import MySQLdb

def offline_cpu(domanUUID,offline_cpu_total):
    os.system('virsh setvcpus '+domainUUID+' '+offline_cpu_total+' --guest')
    print('Offline vCPU success')

if __name__ == '__main__':
    domainUUID = sys.argv[1]
    offline_cpu_total = sys.argv[2]
    offline_cpu(domainUUID,offline_cpu_total)
    password = catch_nova_db_password()
    modify_db_vcpu(domainUUID,offline_cpu_total,password)


