from __future__ import print_function
import sys
import os
from enable_cpu_hotplug import modify_vm_xml, catch_nova_db_password, modify_db_vcpu
import MySQLdb

def online_cpu(domanUUID,online_cpu_total):
    os.system('virsh setvcpus '+domainUUID+' '+online_cpu_total+' --guest')
    print('Online vCPU success')

if __name__ == '__main__':
    domainUUID = sys.argv[1]
    online_cpu_total = sys.argv[2]
    online_cpu(domainUUID,online_cpu_total)
    password = catch_nova_db_password()
    modify_db_vcpu(domainUUID,online_cpu_total,password)

