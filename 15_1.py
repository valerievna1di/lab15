import pandas as pd

# Створення датафрейму із словника
schedule = {
    1: {"route": "Київ – Харків", "arrival": (10, 30), "departure": (10, 50)},
    2: {"route": "Львів – Одеса", "arrival": (12, 15), "departure": (12, 45)},
    3: {"route": "Дніпро – Київ", "arrival": (14, 20), "departure": (14, 35)},
    4: {"route": "Харків – Львів", "arrival": (16, 40), "departure": (17, 0)},
    5: {"route": "Одеса – Дніпро", "arrival": (18, 10), "departure": (18, 25)},
    6: {"route": "Київ – Одеса", "arrival": (19, 50), "departure": (20, 10)},
    7: {"route": "Львів – Київ", "arrival": (21, 15), "departure": (21, 35)},
    8: {"route": "Харків – Одеса", "arrival": (22, 5), "departure": (22, 20)},
    9: {"route": "Одеса – Львів", "arrival": (23, 0), "departure": (23, 20)},
    10: {"route": "Дніпро – Харків", "arrival": (9, 10), "departure": (9, 30)}
}

# Перетворення словника на датафрейм
df = pd.DataFrame.from_dict(schedule, orient='index')
df['arrival'] = df['arrival'].apply(lambda x: f"{x[0]:02}:{x[1]:02}")
df['departure'] = df['departure'].apply(lambda x: f"{x[0]:02}:{x[1]:02}")

# Додавання колонок для зручності аналізу (міста відправлення та прибуття)
df['departure_city'] = df['route'].apply(lambda x: x.split(' – ')[0])
df['arrival_city'] = df['route'].apply(lambda x: x.split(' – ')[1])

# Додавання колонки з номером поїзда для кожного міста прибуття, починаючи з 1
df['train_number'] = df.groupby('arrival_city').cumcount() + 1

# Групування та агрегація даних за містом прибуття
grouped = df.groupby('arrival_city').size().reset_index(name='train_count')

# Зміщення індексу, щоб починати з 1 замість 0
grouped.index += 1

# Виведення результатів
print("Розклад поїздів:")
print(df[['route', 'arrival', 'departure']])

print("\nКількість поїздів для кожного міста прибуття:")
print(grouped)
