У тебя AC-конфиг почти нормальный, но есть одна жирная проблема и пара подозрительных мест. Из-за этого display station all показывает Total: 0. То есть ни один клиент реально не ассоциировался с Wi-Fi. Не “пинг не идёт”, а именно STA вообще не сел на SSID.

Разберём по факту.

Главная ошибка

У тебя на AC настроен Vlanif200 с IP 192.168.200.254/24 и dhcp select global:

interface Vlanif200
 ip address 192.168.200.254 255.255.255.0
 dhcp select global

А по логике этой лабки при direct forwarding:
	•	AC должен быть DHCP-сервером только для AP management VLAN
	•	другое устройство должно быть DHCP-сервером и шлюзом для STA service VLAN
	•	сервисный трафик клиентов идёт напрямую, не через AC  ￼  ￼

В официальной лабе это прямо так и сделано:
	•	AC раздаёт IP для AP
	•	S1 раздаёт IP для STA
	•	service VLAN живёт не на AC, а на другом устройстве  ￼  ￼

Что это значит у тебя

Если у тебя по схеме D1 должен быть шлюзом клиентов 192.168.200.254, то на AC этот же адрес вообще не должен стоять.
Иначе получается человеческая классика: два устройства лезут в одну и ту же роль, а потом все удивляются, почему сеть обиделась.

⸻

Что ещё вижу

1. В vap-profile WLAN-Guest у тебя нет явной строки:

forward-mode direct-forward

Иногда direct forwarding по умолчанию, но лучше прописать явно, чтобы не играть в “а вдруг прошивка решила жить своей жизнью”.
В гайде VAP для этой лабы использует direct forwarding и service VLAN привязывается именно там.  ￼

2. display station all = 0

Это значит одно из двух:
	•	клиент не видит / не подключается к SSID
	•	AP не вещает VAP как надо
	•	либо пароль/безопасность не совпадают
	•	либо AP онлайн, но WLAN-профиль не применился корректно

По гайду после настройки надо проверить:
	•	STA подключился к WLAN
	•	получил IP
	•	на AC видно через display station all  ￼

Если station all пусто, проблема раньше DHCP, чаще всего на этапе ассоциации к SSID.

⸻

Что исправить прямо сейчас

Вариант правильный для твоей схемы

Если у тебя D1 является шлюзом и DHCP для клиентов, то на AC убери VLANIF200 совсем.

На AC:

system-view
interface Vlanif200
 undo ip address
 undo dhcp select global
 quit

Лучше вообще оставить на AC только:
	•	Vlanif43
	•	DHCP pool для AP
	•	trunk на GE0/0/10
	•	CAPWAP source on Vlanif43
	•	WLAN profiles

⸻

Исправь VAP profile явно

system-view
wlan
 vap-profile name WLAN-Guest
  forward-mode direct-forward
  service-vlan vlan-id 200
  ssid-profile WLAN-Guest
  security-profile WLAN-Guest
 quit
quit


⸻

Как должен выглядеть AC в твоём случае

Вот исправленный AC-конфиг:

system-view
sysname AC

vlan batch 43 200

dhcp enable

ip pool AP
 gateway-list 10.1.43.254
 network 10.1.43.0 mask 255.255.255.0
 excluded-ip-address 10.1.43.1 10.1.43.100
 quit

interface Vlanif43
 ip address 10.1.43.254 255.255.255.0
 dhcp select global
 quit

interface GigabitEthernet0/0/10
 port link-type trunk
 port trunk allow-pass vlan 43 200
 quit

capwap source interface Vlanif43

wlan
 regulatory-domain-profile name default
  country-code KZ
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
  ssid-profile WLAN-Guest
  security-profile WLAN-Guest
 quit

 ap-group name ap-group1
  radio 0
   vap-profile WLAN-Guest wlan 1
  radio 1
   vap-profile WLAN-Guest wlan 1
  radio 2
   vap-profile WLAN-Guest wlan 1
 quit

 ap auth-mode mac-auth

 ap-id 0 ap-mac 60f1-8a9c-2b40
  ap-name AP1
  ap-group ap-group1
 quit

 ap-id 1 ap-mac b4fb-f9b7-de40
  ap-name AP2
  ap-group ap-group1
 quit

 provision-ap
quit
save


⸻

И D1 должен быть таким

system-view
sysname D1

vlan batch 43 200

dhcp enable

ip pool STA
 gateway-list 192.168.200.254
 network 192.168.200.0 mask 255.255.255.0
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

Что проверить после исправления

1. AP вообще онлайн?

На AC:

display ap all

Они должны быть в состоянии normal. В гайде именно это считается признаком, что AP работают правильно.  ￼

2. SSID реально виден?

На телефоне/ноуте должен появиться:
	•	Guest-WiFi

Если SSID не видно, значит проблема не в DHCP, а в VAP/AP-group/radio binding.

3. STA подключается?

После подключения:

display station all

Если всё ок, тут появится MAC клиента, AP, VLAN, IP, SSID. По гайду это финальная проверка.  ￼

4. IP на клиенте

На STA:

ipconfig

Должен получить:
	•	192.168.200.x
	•	gateway 192.168.200.254

5. Пинг

ping 50.1.1.1


⸻

Если после этого всё ещё Total: 0

Тогда мне нужны ровно эти выводы, не роман, а команды:

display ap all
display wlan vap all
display current-configuration interface GigabitEthernet 0/0/10
display current-configuration | include vap-profile
display current-configuration | include service-vlan

И ещё конфиг D1, A1, A2. Потому что сейчас больше всего похоже на то, что:
	•	либо AC зря держит VLAN 200
	•	либо service VLAN 200 где-то не проходит по trunk
	•	либо SSID не доставлен на радио AP

Короче, первый фикс: убери Vlanif200 с AC и явно пропиши forward-mode direct-forward. Это самый вероятный корень проблемы.
