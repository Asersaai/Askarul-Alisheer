) PPPoE

R7

ip pool POOL1
 network 172.16.1.0 mask 24
 gateway-list 172.16.1.1

interface Virtual-Template 1
 ip address 172.16.1.1 24
 ppp authentication-mode chap
 remote address pool POOL1

aaa
 local-user user1 password cipher user@123
 local-user user1 service-type ppp

interface GigabitEthernet 0/0/0
 pppoe-server bind virtual-template 1

R8

dialer-rule
 dialer-rule 1 ip permit

interface Dialer 1
 dialer user u1
 dialer-group 1
 dialer bundle 1
 ppp chap user user1
 ppp chap password cipher user@123
 ip address ppp-negotiate

interface GigabitEthernet 0/0/0
 pppoe-client dial-bundle-number 1

ip route-static 0.0.0.0 0.0.0.0 Dialer 1


⸻

5) GRE Tunnel

RT1

interface GigabitEthernet 0/0/0
 ip address 192.168.11.1 24

interface LoopBack 0
 ip address 50.1.1.1 30

ip route-static 0.0.0.0 0.0.0.0 192.168.11.2

interface Tunnel 0/0/1
 tunnel-protocol gre
 source GigabitEthernet 0/0/0
 destination 192.168.12.1
 ip address 10.0.1.1 24

ospf 1 router-id 50.1.1.1
 area 0
  network 10.0.1.0 0.0.0.255
  network 50.1.1.1 0.0.0.0

RT2

interface GigabitEthernet 0/0/1
 ip address 192.168.12.1 24

interface LoopBack 0
 ip address 50.2.2.2 30

ip route-static 0.0.0.0 0.0.0.0 192.168.12.2

interface Tunnel 0/0/1
 tunnel-protocol gre
 source GigabitEthernet 0/0/1
 destination 192.168.11.1
 ip address 10.0.1.2 24

ospf 1 router-id 50.2.2.2
 area 0
  network 10.0.1.0 0.0.0.255
  network 50.2.2.2 0.0.0.0

ISP

interface GigabitEthernet 0/0/0
 ip address 192.168.11.2 24

interface GigabitEthernet 0/0/1
 ip address 192.168.12.2 24



