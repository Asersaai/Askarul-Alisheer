Task 1
Для начала зайдите в режим конфигурации маршрутизатора RT1 (команда system-view).
1) Basic device configuration (Базовая настройка)
sysname RT1
interface GigabitEthernet 0/0/0
 ip address 10.1.1.1 255.255.255.252
 quit
interface GigabitEthernet 0/0/1
 ip address 10.2.2.1 255.255.255.252
 quit
interface GigabitEthernet 0/0/2
 ip address 10.3.3.1 255.255.255.252
 quit

2) Configure AAA Scheme (Настройка схем аутентификации и авторизации)
aaa
 authentication-scheme LOCAL
  authentication-mode local
  quit
 authorization-scheme LOCAL
  authorization-mode local
  quit

3) Configure AAA Domain (Настройка домена)
 domain LAB.LOCAL
  authentication-scheme LOCAL
  authorization-scheme LOCAL
  quit

4) Configure Local users (Создание локальных пользователей)
Примечание: В качестве пароля я использую Password@123, вы можете изменить его на свой.
 local-user user1@LAB.LOCAL password cipher Password@123
 local-user user1@LAB.LOCAL privilege level 15
 local-user user1@LAB.LOCAL service-type ssh

 local-user user2@LAB.LOCAL password cipher Password@123
 local-user user2@LAB.LOCAL privilege level 3
 local-user user2@LAB.LOCAL service-type ssh

 local-user user3@LAB.LOCAL password cipher Password@123
 local-user user3@LAB.LOCAL privilege level 1
 local-user user3@LAB.LOCAL service-type ssh
 quit

(Важно: так как мы создали отдельный домен LAB.LOCAL, имена пользователей лучше заводить с указанием этого домена, чтобы они к нему привязались).
5) Configure Remote Access (SSH) (Настройка удаленного доступа)
rsa local-key-pair create
(При запросе длины ключа нажмите Enter, чтобы использовать стандартное значение, например 2048)

stelnet server enable

user-interface vty 0 4
 authentication-mode aaa
 protocol inbound ssh
 quit

Настройка клиентов (Client1, Client2, Client3)
Каждому клиенту нужно задать имя, IP-адрес и разрешить первый SSH-вход.
Для Client1:
system-view
sysname Client1
interface GigabitEthernet 0/0/0
 ip address 10.1.1.2 255.255.255.252
 quit
ssh client first-time enable

Для Client2:
system-view
sysname Client2
interface GigabitEthernet 0/0/0
 ip address 10.2.2.2 255.255.255.252
 quit
ssh client first-time enable

Для Client3:
system-view
sysname Client3
interface GigabitEthernet 0/0/0
 ip address 10.3.3.2 255.255.255.252
 quit
ssh client first-time enable

6) Verification (Проверка)
Чтобы проверить работу конфигурации, вам нужно инициировать SSH-сессию с любого из клиентов на маршрутизатор RT1.
Например, находясь на Client1 (в пользовательском режиме, не в system-view), введите команду:
stelnet 10.1.1.1

 * Вас попросят ввести имя пользователя: вводите user1@LAB.LOCAL
 * Затем пароль: Password@123
 * После успешного входа вы можете ввести команду display user-interface или display users, чтобы убедиться, что вы подключены и имеете уровень привилегий 15.
Аналогично можно проверить с Client2 (stelnet 10.2.2.1 под user2@LAB.LOCAL) и Client3.
Хотите, я подробнее объясню, за что отвечает каждый из созданных уровней привилегий (15, 3 и 1) в системе Huawei?



Task 2: Layer3 Link Aggregation
Здесь нужно объединить два физических интерфейса (GE0/0/1 и GE0/0/2) в один логический (Eth-Trunk 1) в режиме LACP и повесить на него IP-адреса.
Код для Router1:
system-view
sysname Router1

# Создаем интерфейс и задаем режим LACP
interface Eth-Trunk 1
 undo portswitch  # (команда переводит порт в L3-режим, если нужно)
 mode lacp-static
 ip address 10.1.1.101 255.255.255.252
 quit

# Добавляем физические порты в агрегированный канал
interface GigabitEthernet0/0/1
 eth-trunk 1
 quit
interface GigabitEthernet0/0/2
 eth-trunk 1
 quit

Код для Router2:
system-view
sysname Router2

# Создаем интерфейс и задаем режим LACP
interface Eth-Trunk 1
 undo portswitch
 mode lacp-static
 ip address 10.1.1.102 255.255.255.252
 quit

# Добавляем физические порты в агрегированный канал
interface GigabitEthernet0/0/1
 eth-trunk 1
 quit
interface GigabitEthernet0/0/2
 eth-trunk 1
 quit

Несколько полезных команд для пункта 6 (Verification) из первой задачи:
 * display ip interface brief — проверить поднялись ли IP-адреса.
 * display aaa local-user — посмотреть список созданных пользователей.
 * display eth-trunk 1 — проверить статус LACP агрегации (для второго задания).
Подсказать, как настроить клиентские маршрутизаторы (Client1, 2, 3), чтобы протестировать SSH подключение к RT1?


Task 3
Привет! На скриншоте представлена лабораторная работа по настройке удаленного AAA (Authentication, Authorization, Accounting) с использованием протоколов RADIUS и HWTACACS (аналог TACACS+ от Huawei). Судя по синтаксису, это оборудование Huawei (вероятно, эмулятор eNSP).
В текстовых подсказках на твоей картинке (справа) есть несколько опечаток, допущенных автором задания. Например, в блоке --RADIUS-- предлагается создать шаблон hwtacacs-server template RD, что в корне неверно для RADIUS. Я исправлю эти ошибки и напишу для тебя правильные рабочие команды.
Ниже приведена полная конфигурация для маршрутизатора R1. Для R2 настройки будут абсолютно идентичными, изменится только IP-адрес интерфейса.
1. Базовая настройка интерфейса (на примере R1)
Для начала нужно задать IP-адрес интерфейсу, смотрящему в сторону коммутатора, чтобы у роутера была связь с сервером.
system-view
sysname R1
interface GigabitEthernet 0/0/0
 ip address 172.16.128.11 255.255.255.0
 quit

2. Настройка RADIUS (шаблон RD)
Создаем шаблон для подключения к RADIUS-серверу (IP сервера 172.16.128.10, как указано слева на схеме).
radius-server template RD
 radius-server authentication 172.16.128.10 1812
 radius-server accounting 172.16.128.10 1813
 radius-server shared-key cipher Huawei123
 quit

3. Настройка HWTACACS (шаблон HT)
Создаем шаблон для TACACS+ сервера.
hwtacacs-server template HT
 hwtacacs-server authentication 172.16.128.10
 hwtacacs-server authorization 172.16.128.10
 hwtacacs-server accounting 172.16.128.10
 hwtacacs-server shared-key cipher Huawei123
 quit

4. Настройка AAA (Схемы и Домен)
Теперь переходим в режим aaa, создаем схемы и привязываем их к домену.
aaa
 # Создаем схемы для RADIUS
 authentication-scheme RADIUS
  authentication-mode radius local
 accounting-scheme RADIUS
  accounting-mode radius
 quit

 # Создаем схемы для HWTACACS
 authentication-scheme HWTACACS
  authentication-mode hwtacacs local
 authorization-scheme HWTACACS
  authorization-mode hwtacacs local
 accounting-scheme HWTACACS
  accounting-mode hwtacacs
 quit

Настройка домена:
В задании указан домен LAB.LOCAL. Важный момент: чтобы протестировать и RADIUS, и HWTACACS, их нужно по очереди привязать к домену (или создать два разных домена).
Вариант привязки для проверки RADIUS:
 domain LAB.LOCAL
  authentication-scheme RADIUS
  accounting-scheme RADIUS
  radius-server RD
  quit

Если захочешь переключить домен на HWTACACS, команды будут такими:
 domain LAB.LOCAL
  authentication-scheme HWTACACS
  authorization-scheme HWTACACS
  accounting-scheme HWTACACS
  hwtacacs-server HT
  quit

5. Команды для тестирования
После того как серверы на Linux (Debian/Ubuntu) настроены и запущены, ты можешь проверить связь прямо из консоли R1 (в пользовательском режиме):
Для проверки RADIUS:
test-aaa user1 Huawei@123 radius-template RD

Для проверки HWTACACS:
(На картинке в блоке HWTACACS тоже опечатка: там написано radius-template HT, хотя должно быть так):
test-aaa user1 Huawei@123 hwtacacs-template HT

Хочешь, я также подскажу, какие пакеты и конфигурационные файлы нужно настроить на стороне Linux (Ubuntu/Debian) для поднятия самих серверов FreeRADIUS и tacacs+?


