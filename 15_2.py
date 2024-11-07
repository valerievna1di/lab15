import pandas as pd
import matplotlib.pyplot as plt

# Застосування стилю ggplot та налаштування розміру фігури
plt.style.use('ggplot')
plt.rcParams['figure.figsize'] = (15, 5)

# Завантаження даних з правильним кодуванням і розпізнаванням дат
data = pd.read_csv('data2009.csv', encoding='latin1', parse_dates=['Date'], dayfirst=True)

# Видалення порожніх стовпців, включаючи 'Unnamed: 1'
data = data.drop(columns=['Unnamed: 1'], errors='ignore')

# Виведення перших п'яти рядків після видалення порожніх стовпців з початковим індексом з 1
print("Перші п'ять рядків даних після завантаження:")
print(data.head(5).reset_index(drop=True).rename(index=lambda x: x + 1))

# Додавання стовпця 'Month'
data['Month'] = data['Date'].dt.month

# Сумування даних з усіх колонок, що представляють кількість велосипедистів
data['Total_Count'] = data[['Berri1', 'Maisonneuve_1', 'Maisonneuve_2', 'Brebeuf']].sum(axis=1)

# Виведення перших п'яти рядків після додавання Total_Count з рахунком рядків з 1
print("\nПерші п'ять рядків з доданим стовпцем Total_Count:")
print(data[['Date', 'Berri1', 'Maisonneuve_1', 'Maisonneuve_2', 'Brebeuf', 'Total_Count']].head(5).reset_index(drop=True).rename(index=lambda x: x + 1))

# Групування даних за місяцями та підрахунок кількості велосипедистів для кожного міста
monthly_city_usage = data.groupby('Month')[['Berri1', 'Maisonneuve_1', 'Maisonneuve_2', 'Brebeuf']].sum()

# Створення повного індексу для місяців і додавання відсутніх місяців з нульовими значеннями
all_months = pd.Index(range(1, 13), name='Month')
monthly_city_usage = monthly_city_usage.reindex(all_months, fill_value=0)

# Маппінг чисел на назви місяців
month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
monthly_city_usage.index = month_names

# Візуалізація даних на лінійному графіку для кожного міста
monthly_city_usage.plot(kind='line', marker='o', linestyle='-')
plt.title('Загальна кількість велосипедистів по місяцях для кожного міста')
plt.xlabel('Місяць')
plt.ylabel('Кількість велосипедистів')
plt.xticks(range(len(month_names)), month_names)  # Відображення всіх місяців на осі X
plt.legend()
plt.grid(True)
plt.show()
