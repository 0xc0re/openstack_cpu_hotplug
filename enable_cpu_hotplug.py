from __future__ import print_function
import xml.etree.ElementTree as ET
import sys
import libvirt
import os
import MySQLdb

def connect():##Connect to qemu
    connect = libvirt.open('qemu:///system')
    if connect == None:
        print('Failed to open connection to qemu:///system', file=sys.stderr)
        exit(1)
    else:
        conn = connect
        print('connect success')
        return conn

def re_define_domain(conn, domainUUID, conf_file):## destroy xml, undefine xml and define xml
    domain = conn.lookupByUUIDString(domainUUID)
    if (domain.destroy()) == -1:
        print('Destroy domain failed')
        exit(1)
    else:
        print('Destroy domain Success')

    f = open(conf_file)
    xml = f.read()
    if (conn.defineXML(xml)) == None:
        print('Failed to define a domain from an XML definition.', file=sys.stderr)
        exit(1)
	f.close()
    else:
        print('Define a domain from an XML definition success.')

    if (conn.createXML(xml)) == None:
        print('Failed to create a domain from an XML definition.', file=sys.stderr)
        exit(1)
	f.close()
    else:
        print('Boot a domain success.')
        f.close()


def disconnect(conn):##disconnect qemu
    conn.close()
    exit(0)


def modify_vm_xml(conf_file, current_cpu):
    init_current_cpu = current_cpu
    tree = ET.parse(conf_file)
    root = tree.getroot()
    nova_cpu  = tree.findall('metadata/{http://openstack.org/xmlns/libvirt/nova/1.0}instance/')
    flavor_nova_cpu = nova_cpu[3].find('{http://openstack.org/xmlns/libvirt/nova/1.0}vcpus')
    cpu = tree.findall("vcpu")
    cpu[0].attrib = {"placement":"static","current":init_current_cpu}
    flavor_nova_cpu.attrib = {"placement":"static","current":init_current_cpu}
    tree.write(conf_file);


def catch_nova_db_password():
    f = open("/etc/nova/nova.conf", "r")
    for line in f:
        if "nova:" in line:
            temp = line
            temp1 = temp.split(':')[2]
            password = temp1.split('@')[0]
            return password
        else:
            continue
    f.close()


def modify_db_vcpu(domainUUID,current_cpu,password):
    try:
        db = MySQLdb.connect(host="localhost", user="nova", passwd=password, db="nova")
        cursor = db.cursor()
        command = "update instances set vcpus='"+current_cpu+"\'"+" where uuid='"+domainUUID+"\';"
        cursor.execute(command)
        db.commit()
	db.close()
    except Error as e:
        print(e)
	db.close()
    

if __name__ == '__main__':
    domainUUID = sys.argv[1]
    current_cpu = sys.argv[2]
    conf_file = '/var/lib/nova/instances/'+domainUUID+'/libvirt.xml'  
    conn = connect()
    modify_vm_xml(conf_file, current_cpu)
    re_define_domain(conn,domainUUID,conf_file)
    password=catch_nova_db_password()
    modify_db_vcpu(domainUUID,current_cpu,password)
    disconnect(conn)
