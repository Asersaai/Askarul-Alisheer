Держи полный код по устройствам, интерфейс за интерфейсом. Без лирики, потому что железки и так достаточно капризные. Основа та же, что в лабе Huawei: отдельный management VLAN для AP, отдельный service VLAN для клиентов, DHCP для AP на AC, DHCP для STA на распределительном устройстве, и direct forwarding в VAP.  ￼  ￼

⸻

1) AC

system-view
sysname AC

vlan batch 43 200

dhcp enable

ip pool AP
 network 10.1.43.0 mask 255.255.255.0
 gateway-list 10.1.43.254
 excluded-ip-address 10.1.43.254
 excluded-ip-address 10.1.43.1 10.1.43.100
 quit

interface Vlanif43
 ip address 10.1.43.254 255.255.255.0
 dhcp select global
 quit

interface Vlanif200
 quit

interface GigabitEthernet0/0/10
 port link-type trunk
 port trunk allow-pass vlan 43 200
 quit

wlan
 ap-group name ap-group1
 quit

 regulatory-domain-profile name default
 country-code KZ
 quit

 ap-group name ap-group1
 regulatory-domain-profile default
 quit

 ap auth-mode mac-auth

 ap-id 0 ap-mac XXXX-XXXX-XXXX
  ap-name AP1
  ap-group ap-group1
  quit

 ap-id 1 ap-mac YYYY-YYYY-YYYY
  ap-name AP2
  ap-group ap-group1
  quit

 security-profile name WLAN-Guest
  security wpa-wpa2 psk pass-phrase Huawei@123 aes
  quit

 ssid-profile name WLAN-Guest
  ssid Guest-WiFi
  quit

 vap-profile name WLAN-Guest
  forward-mode direct-forward
  service-vlan vlan-id 200
  security-profile WLAN-Guest
  ssid-profile WLAN-Guest
  quit

 ap-group name ap-group1
  vap-profile WLAN-Guest wlan 1 radio all
  quit
 quit

capwap source interface Vlanif43

save


⸻

2) D1

system-view
sysname D1

vlan batch 43 200

dhcp enable

ip pool STA
 network 192.168.200.0 mask 255.255.255.0
 gateway-list 192.168.200.254
 excluded-ip-address 192.168.200.254
 excluded-ip-address 192.168.200.1 192.168.200.10
 quit

interface Vlanif43
 quit

interface Vlanif200
 ip address 192.168.200.254 255.255.255.0
 dhcp select global
 quit

interface LoopBack50
 ip address 50.1.1.1 255.255.255.255
 quit

interface GigabitEthernet0/0/10
 port link-type trunk
 port trunk allow-pass vlan 43 200
 quit

interface GigabitEthernet0/0/13
 port link-type trunk
 port trunk allow-pass vlan 43 200
 quit

interface GigabitEthernet0/0/14
 port link-type trunk
 port trunk allow-pass vlan 43 200
 quit

save


⸻

3) A1

system-view
sysname A1

vlan batch 43 200

interface Vlanif43
 quit

interface Vlanif200
 quit

interface GigabitEthernet0/0/1
 port link-type trunk
 port trunk allow-pass vlan 43 200
 quit

interface GigabitEthernet0/0/4
 port link-type trunk
 port trunk pvid vlan 43
 port trunk allow-pass vlan 43 200
 quit

save


⸻

4) A2

system-view
sysname A2

vlan batch 43 200

interface Vlanif43
 quit

interface Vlanif200
 quit

interface GigabitEthernet0/0/1
 port link-type trunk
 port trunk allow-pass vlan 43 200
 quit

interface GigabitEthernet0/0/4
 port link-type trunk
 port trunk pvid vlan 43
 port trunk allow-pass vlan 43 200
 quit

save


⸻

5) Если нужен вариант как в display current-configuration

AC

#
sysname AC
#
vlan batch 43 200
#
dhcp enable
#
ip pool AP
 gateway-list 10.1.43.254
 network 10.1.43.0 mask 255.255.255.0
 excluded-ip-address 10.1.43.254
 excluded-ip-address 10.1.43.1 10.1.43.100
#
interface Vlanif43
 ip address 10.1.43.254 255.255.255.0
 dhcp select global
#
interface GigabitEthernet0/0/10
 port link-type trunk
 port trunk allow-pass vlan 43 200
#
capwap source interface Vlanif43
#
wlan
 ap-group name ap-group1
 regulatory-domain-profile name default
 country-code KZ
 ap auth-mode mac-auth
 ap-id 0 ap-mac XXXX-XXXX-XXXX
  ap-name AP1
  ap-group ap-group1
 ap-id 1 ap-mac YYYY-YYYY-YYYY
  ap-name AP2
  ap-group ap-group1
 security-profile name WLAN-Guest
  security wpa-wpa2 psk pass-phrase Huawei@123 aes
 ssid-profile name WLAN-Guest
  ssid Guest-WiFi
 vap-profile name WLAN-Guest
  forward-mode direct-forward
  service-vlan vlan-id 200
  security-profile WLAN-Guest
  ssid-profile WLAN-Guest
 ap-group name ap-group1
  regulatory-domain-profile default
  vap-profile WLAN-Guest wlan 1 radio all
#
return

D1

#
sysname D1
#
vlan batch 43 200
#
dhcp enable
#
ip pool STA
 gateway-list 192.168.200.254
 network 192.168.200.0 mask 255.255.255.0
 excluded-ip-address 192.168.200.254
 excluded-ip-address 192.168.200.1 192.168.200.10
#
interface Vlanif200
 ip address 192.168.200.254 255.255.255.0
 dhcp select global
#
interface LoopBack50
 ip address 50.1.1.1 255.255.255.255
#
interface GigabitEthernet0/0/10
 port link-type trunk
 port trunk allow-pass vlan 43 200
#
interface GigabitEthernet0/0/13
 port link-type trunk
 port trunk allow-pass vlan 43 200
#
interface GigabitEthernet0/0/14
 port link-type trunk
 port trunk allow-pass vlan 43 200
#
return

A1

#
sysname A1
#
vlan batch 43 200
#
interface GigabitEthernet0/0/1
 port link-type trunk
 port trunk allow-pass vlan 43 200
#
interface GigabitEthernet0/0/4
 port link-type trunk
 port trunk pvid vlan 43
 port trunk allow-pass vlan 43 200
#
return

A2

#
sysname A2
#
vlan batch 43 200
#
interface GigabitEthernet0/0/1
 port link-type trunk
 port trunk allow-pass vlan 43 200
#
interface GigabitEthernet0/0/4
 port link-type trunk
 port trunk pvid vlan 43
 port trunk allow-pass vlan 43 200
#
return


⸻

6) Что заменить обязательно

На AC вот это:

ap-id 0 ap-mac XXXX-XXXX-XXXX
ap-id 1 ap-mac YYYY-YYYY-YYYY

Нужно поменять на реальные MAC твоих AP. Без этого AP не поднимутся нормально в mac-auth, потому что техника любит бессмысленно страдать. В гайде AP импортируются на AC по MAC или SN, после чего добавляются в группу AP и получают конфиг.  ￼

⸻

7) Команды проверки

На AC

display ap all
display station all
display ap unauthorized all

На STA

ipconfig
ping 50.1.1.1

По гайду именно это и проверяют: STA должен получить адрес, пинговать loopback, а на AC должен отображаться через display station all.  ￼

Если надо, следующим сообщением дам тебе ещё более жёсткую версию: по устройствам в порядке ввода в eNSP, без единого лишнего слова.
