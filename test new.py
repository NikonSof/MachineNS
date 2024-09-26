import pandas as pd
import matplotlib.pyplot as plt

# Загрузка данных
file_path = 'LIST2 test.xlsx'
data = pd.read_excel(file_path, sheet_name='Лист2')

# Очистка данных
data_cleaned = data.dropna(how='all', axis=1).dropna(how='all', axis=0)

# Приведение столбца "Шифр" к строковому типу и приведение к верхнему регистру для точного поиска
data_cleaned['Шифр'] = data_cleaned['Шифр'].astype(str).str.upper()

# Разделение на коронавирус и грипп по колонке 'Шифр'
coronavirus_data = data_cleaned[data_cleaned['Шифр'].str.contains('КФ', na=False)]
flu_data = data_cleaned[data_cleaned['Шифр'].str.contains('Г', na=False)]

# Подсчет количества случаев
coronavirus_count = coronavirus_data.shape[0]
flu_count = flu_data.shape[0]

# Анализ: распределение по возрасту, полу, пневмонии и патологиям для каждой категории
coronavirus_age_dist = coronavirus_data['Код возраста'].value_counts()
flu_age_dist = flu_data['Код возраста'].value_counts()

coronavirus_gender_dist = coronavirus_data['Пол'].value_counts()
flu_gender_dist = flu_data['Пол'].value_counts()

coronavirus_pneumonia_dist = coronavirus_data['пневмония'].value_counts()
flu_pneumonia_dist = flu_data['пневмония'].value_counts()

coronavirus_pathology_dist = coronavirus_data['Категория сопутствующей патологии'].value_counts()
flu_pathology_dist = flu_data['Категория сопутствующей патологии'].value_counts()

# Визуализация
fig, axs = plt.subplots(4, 2, figsize=(10, 15))

# 1. График для распределения возрастов (Коронавирус)
axs[0, 0].bar(coronavirus_age_dist.index.astype(str), coronavirus_age_dist.values, color='lightblue')
axs[0, 0].set_title('Коронавирус (КФ): Распределение по возрасту')
axs[0, 0].set_xlabel('Возрастная группа')
axs[0, 0].set_ylabel('Количество случаев')

# 2. График для распределения возрастов (Грипп)
axs[0, 1].bar(flu_age_dist.index.astype(str), flu_age_dist.values, color='lightgreen')
axs[0, 1].set_title('Грипп (Г): Распределение по возрасту')
axs[0, 1].set_xlabel('Возрастная группа')
axs[0, 1].set_ylabel('Количество случаев')

# 3. График для распределения пола (Коронавирус)
axs[1, 0].bar(coronavirus_gender_dist.index.astype(str), coronavirus_gender_dist.values, color='lightblue')
axs[1, 0].set_title('Коронавирус (КФ): Распределение по полу')
axs[1, 0].set_xlabel('Пол')
axs[1, 0].set_ylabel('Количество случаев')

# 4. График для распределения пола (Грипп)
axs[1, 1].bar(flu_gender_dist.index.astype(str), flu_gender_dist.values, color='lightgreen')
axs[1, 1].set_title('Грипп (Г): Распределение по полу')
axs[1, 1].set_xlabel('Пол')
axs[1, 1].set_ylabel('Количество случаев')

# 5. График для распределения пневмонии (Коронавирус)
axs[2, 0].bar(coronavirus_pneumonia_dist.index.astype(str), coronavirus_pneumonia_dist.values, color='lightblue')
axs[2, 0].set_title('Коронавирус (КФ): Распределение по пневмонии')
axs[2, 0].set_xlabel('Пневмония')
axs[2, 0].set_ylabel('Количество случаев')

# 6. График для распределения пневмонии (Грипп)
axs[2, 1].bar(flu_pneumonia_dist.index.astype(str), flu_pneumonia_dist.values, color='lightgreen')
axs[2, 1].set_title('Грипп (Г): Распределение по пневмонии')
axs[2, 1].set_xlabel('Пневмония')
axs[2, 1].set_ylabel('Количество случаев')

# 7. График для распределения патологий (Коронавирус)
axs[3, 0].bar(coronavirus_pathology_dist.index.astype(str), coronavirus_pathology_dist.values, color='lightblue')
axs[3, 0].set_title('Коронавирус (КФ): Сопутствующие патологии')
axs[3, 0].set_xlabel('Патология')
axs[3, 0].set_ylabel('Количество случаев')

# 8. График для распределения патологий (Грипп)
axs[3, 1].bar(flu_pathology_dist.index.astype(str), flu_pathology_dist.values, color='lightgreen')
axs[3, 1].set_title('Грипп (Г): Сопутствующие патологии')
axs[3, 1].set_xlabel('Патология')
axs[3, 1].set_ylabel('Количество случаев')

plt.tight_layout()
plt.show()

# Вывод результатов по категориям
print(f"Количество случаев коронавируса (КФ): {coronavirus_count}")
print(f"Количество случаев гриппа (Г): {flu_count}")