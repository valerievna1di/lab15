import pandas as pd
import matplotlib.pyplot as plt

# Застосування стилю ggplot та налаштування розміру фігури
plt.style.use('ggplot')
plt.rcParams['figure.figsize'] = (15, 5)

# Налаштування відображення всіх колонок і рядків в pandas та розширення виводу таблиці
pd.set_option('display.max_columns', None)  # Відображення всіх колонок
pd.set_option('display.max_rows', None)  # Відображення всіх рядків (опціонально)
pd.set_option('display.expand_frame_repr', False)  # Відображення всіх колонок в одному блоці

# Завантаження даних з правильним кодуванням і розпізнаванням дат
data = pd.read_csv('data2009.csv', encoding='latin1', parse_dates=['Date'], dayfirst=True)

# Видалення порожніх стовпців, включаючи 'Unnamed: 1'
data = data.drop(columns=['Unnamed: 1'], errors='ignore')

# Додавання стовпця 'Month'
data['Month'] = data['Date'].dt.month

# Сумування даних з усіх колонок, що представляють кількість велосипедистів
data['Total_Count'] = data[['Berri1', 'Maisonneuve_1', 'Maisonneuve_2', 'Brebeuf']].sum(axis=1)

# Групування даних за місяцями та підрахунок загальної кількості велосипедистів
monthly_usage = data.groupby('Month')['Total_Count'].sum()

# Маппінг чисел на назви місяців
month_names = ['січень', 'лютий', 'березень', 'квітень', 'травень', 'червень', 'липень', 'серпень', 'вересень', 'жовтень', 'листопад', 'грудень']
monthly_usage.index = monthly_usage.index.map(lambda x: month_names[x - 1])

# Визначення місяця з найбільшою кількістю велосипедистів
most_popular_month = monthly_usage.idxmax()
print(f"Найпопулярніший місяць серед велосипедистів: {most_popular_month}")

# Фільтрація даних для рядків лише з найбільш популярного місяця
popular_month_data = data[data['Month'] == month_names.index(most_popular_month) + 1]

# Виведення рядків даних для найбільш популярного місяця
print("\nРядки даних для найбільш популярного місяця:")
print(popular_month_data.reset_index(drop=True).rename(index=lambda x: x + 1))

# Підрахунок загальної суми Total_Count для найбільш популярного місяця
total_count_sum = popular_month_data['Total_Count'].sum()
print(f"\nЗагальна сума Total_Count для найбільш популярного місяця: {total_count_sum}")

# Візуалізація даних на лінійному графіку для кожного місяця по містах
monthly_city_usage = data.groupby('Month')[['Berri1', 'Maisonneuve_1', 'Maisonneuve_2', 'Brebeuf']].sum()

# Створення повного індексу для місяців і додавання відсутніх місяців з нульовими значеннями
all_months = pd.Index(range(1, 13), name='Month')
monthly_city_usage = monthly_city_usage.reindex(all_months, fill_value=0)

# Встановлення назв місяців як індексу
monthly_city_usage.index = month_names

# Візуалізація загальної кількості велосипедистів по місяцях для кожного міста
monthly_city_usage.plot(kind='line', marker='o', linestyle='-')
plt.title('Загальна кількість велосипедистів по місяцях для кожного міста')
plt.xlabel('Місяць')
plt.ylabel('Кількість велосипедистів')
plt.xticks(range(len(month_names)), month_names)  # Відображення всіх місяців на осі X
plt.legend()
plt.grid(True)
plt.show()
