import json
import os

# Проверяем существование файла
file_path = "sample-data.json"
if not os.path.exists(file_path):
    raise FileNotFoundError(f"Файл {file_path} не найден. Проверьте путь.")

# Открываем JSON-файл
with open(file_path) as file:
    data = json.load(file)

# Выбираем нужные данные (предполагаем, что они находятся в "imdata")
interfaces = data.get("imdata", [])

# Заголовок
print("Interface Status")
print("=" * 50)
print(f"{'DN':<50} {'Description':<20} {'Speed':<10} {'MTU'}")
print("-" * 50)

# Вывод данных
for item in interfaces:
    attributes = item.get("l1PhysIf", {}).get("attributes", {})
    dn = attributes.get("dn", "N/A")
    description = attributes.get("descr", "")
    speed = attributes.get("speed", "inherit")
    mtu = attributes.get("mtu", "N/A")
    
    print(f"{dn:<50} {description:<20} {speed:<10} {mtu}")
