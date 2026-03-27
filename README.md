1) EdgeRT1:
   sys
sysname EdgeRT1

interface GigabitEthernet0/0/0
 ip address 10.1.1.101 255.255.255.252

interface LoopBack50
 ip address 50.1.1.1 255.255.255.255

ospf 1 router-id 50.1.1.1
 area 0
  network 10.1.1.100 0.0.0.3
  network 50.1.1.1 0.0.0.0

aaa
 local-user admin password irreversible-cipher Huawei@123
 local-user admin privilege level 15
 local-user admin service-type terminal telnet ssh

stelnet server enable
telnet server enable
rsa local-key-pair create

user-interface vty 0 4
 authentication-mode aaa
 protocol inbound all
 idle-timeout 10 0

save

2) C1:
   sys
sysname C1

interface GigabitEthernet0/0/0
 ip address 10.1.1.102 255.255.255.252

interface GigabitEthernet0/0/1
 ip address 10.1.1.105 255.255.255.252

interface GigabitEthernet0/0/2
 ip address 10.1.1.109 255.255.255.252

interface LoopBack50
 ip address 50.2.2.2 255.255.255.255

ospf 1 router-id 50.2.2.2
 area 0
  network 10.1.1.100 0.0.0.3
  network 10.1.1.104 0.0.0.3
  network 10.1.1.108 0.0.0.3
  network 50.2.2.2 0.0.0.0

aaa
 local-user admin password irreversible-cipher Huawei@123
 local-user admin privilege level 15
 local-user admin service-type terminal telnet ssh

stelnet server enable
telnet server enable
rsa local-key-pair create

user-interface vty 0 4
 authentication-mode aaa
 protocol inbound all
 idle-timeout 10 0

save
3)D1:
sys
sysname D1

vlan batch 1 10 20 50

stp enable
stp mode mstp

stp region-configuration
 region-name CAMPUS
 revision-level 1
 instance 1 vlan 10
 instance 2 vlan 20
 active region-configuration

stp instance 1 root primary
stp instance 2 root secondary

interface Vlanif1
 ip address 10.1.1.106 255.255.255.252

interface Vlanif10
 ip address 172.16.10.1 255.255.255.0
 vrrp vrid 10 virtual-ip 172.16.10.254
 vrrp vrid 10 priority 120
 vrrp vrid 10 preempt-mode timer delay 20

interface Vlanif20
 ip address 172.16.20.1 255.255.255.0
 vrrp vrid 20 virtual-ip 172.16.20.254
 vrrp vrid 20 priority 90
 vrrp vrid 20 preempt-mode timer delay 20

interface LoopBack50
 ip address 50.3.3.3 255.255.255.255

interface Eth-Trunk1
 mode lacp-static
 port link-type trunk
 port trunk allow-pass vlan 10 20 50

interface GigabitEthernet0/0/3
 eth-trunk 1

interface GigabitEthernet0/0/4
 eth-trunk 1

interface GigabitEthernet0/0/5
 port link-type access
 port default vlan 1

interface GigabitEthernet0/0/1
 port link-type trunk
 port trunk allow-pass vlan 10 20 50

interface GigabitEthernet0/0/2
 port link-type trunk
 port trunk allow-pass vlan 10 20 50

ospf 1 router-id 50.3.3.3
 area 0
  network 10.1.1.104 0.0.0.3
  network 172.16.10.0 0.0.0.255
  network 172.16.20.0 0.0.0.255
  network 50.3.3.3 0.0.0.0

aaa
 local-user admin password irreversible-cipher Huawei@123
 local-user admin privilege level 15
 local-user admin service-type terminal telnet ssh

stelnet server enable
telnet server enable
rsa local-key-pair create

user-interface vty 0 4
 authentication-mode aaa
 protocol inbound all
 idle-timeout 10 0

save
4) D2:
sys
sysname D2

vlan batch 1 10 20 50

stp enable
stp mode mstp

stp region-configuration
 region-name CAMPUS
 revision-level 1
 instance 1 vlan 10
 instance 2 vlan 20
 active region-configuration

stp instance 1 root secondary
stp instance 2 root primary

interface Vlanif1
 ip address 10.1.1.110 255.255.255.252

interface Vlanif10
 ip address 172.16.10.2 255.255.255.0
 vrrp vrid 10 virtual-ip 172.16.10.254
 vrrp vrid 10 priority 90
 vrrp vrid 10 preempt-mode timer delay 20

interface Vlanif20
 ip address 172.16.20.2 255.255.255.0
 vrrp vrid 20 virtual-ip 172.16.20.254
 vrrp vrid 20 priority 120
 vrrp vrid 20 preempt-mode timer delay 20

interface LoopBack50
 ip address 50.4.4.4 255.255.255.255

interface Eth-Trunk1
 mode lacp-static
 port link-type trunk
 port trunk allow-pass vlan 10 20 50

interface GigabitEthernet0/0/3
 eth-trunk 1

interface GigabitEthernet0/0/4
 eth-trunk 1

interface GigabitEthernet0/0/5
 port link-type access
 port default vlan 1

interface GigabitEthernet0/0/1
 port link-type trunk
 port trunk allow-pass vlan 10 20 50

interface GigabitEthernet0/0/2
 port link-type trunk
 port trunk allow-pass vlan 10 20 50

ospf 1 router-id 50.4.4.4
 area 0
  network 10.1.1.108 0.0.0.3
  network 172.16.10.0 0.0.0.255
  network 172.16.20.0 0.0.0.255
  network 50.4.4.4 0.0.0.0

aaa
 local-user admin password irreversible-cipher Huawei@123
 local-user admin privilege level 15
 local-user admin service-type terminal telnet ssh

stelnet server enable
telnet server enable
rsa local-key-pair create

user-interface vty 0 4
 authentication-mode aaa
 protocol inbound all
 idle-timeout 10 0

save
5)A1:
sys
sysname A1

vlan batch 10 20 50

interface GigabitEthernet0/0/1
 port link-type trunk
 port trunk allow-pass vlan 10 20 50

interface GigabitEthernet0/0/2
 port link-type trunk
 port trunk allow-pass vlan 10 20 50

interface Ethernet0/0/1
 port link-type access
 port default vlan 10

interface Ethernet0/0/2
 port link-type access
 port default vlan 20

interface Vlanif50
 ip address 10.1.50.101 255.255.255.252

aaa
 local-user admin password irreversible-cipher Huawei@123
 local-user admin privilege level 15
 local-user admin service-type terminal telnet ssh

stelnet server enable
telnet server enable
rsa local-key-pair create

user-interface vty 0 4
 authentication-mode aaa
 protocol inbound all

save
6)A2:
sys
sysname A2

vlan batch 10 20 50

interface GigabitEthernet0/0/1
 port link-type trunk
 port trunk allow-pass vlan 10 20 50

interface GigabitEthernet0/0/2
 port link-type trunk
 port trunk allow-pass vlan 10 20 50

interface Ethernet0/0/1
 port link-type access
 port default vlan 10

interface Ethernet0/0/2
 port link-type access
 port default vlan 20

interface Vlanif50
 ip address 10.1.50.102 255.255.255.252

aaa
 local-user admin password irreversible-cipher Huawei@123
 local-user admin privilege level 15
 local-user admin service-type terminal telnet ssh

stelnet server enable
telnet server enable
rsa local-key-pair create

user-interface vty 0 4
 authentication-mode aaa
 protocol inbound all

save


