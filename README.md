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

