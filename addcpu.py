from __future__ import print_function
import xml.etree.ElementTree as ET
import sys
from enable_cpu_hotplug import connect, disconnect, modify_vm_xml, catch_nova_db_password, modify_db_vcpu
import os
import MySQLdb
import time

def hot_add(conn, domainUUID, add_cpu):
    domain = conn.lookupByUUIDString(domainUUID)
    if (domain.setVcpus(int(add_cpu))) == -1:
        print('Hot add cpu fail.', file=sys.stderr)
        exit(1)
    else:
        print('Hot add cpu success.')
	time.sleep(10)
	os.system('virsh setvcpus '+domainUUID+' '+add_cpu+' --guest')

if __name__ == '__main__':
    domainUUID = sys.argv[1]
    add_cpu = sys.argv[2]
    conf_file = '/var/lib/nova/instances/'+domainUUID+'/libvirt.xml'  
    conn = connect()
    hot_add(conn,domainUUID,add_cpu)  
    modify_vm_xml(conf_file, add_cpu)
    password = catch_nova_db_password()
    modify_db_vcpu(domainUUID,add_cpu,password)
    disconnect(conn)
