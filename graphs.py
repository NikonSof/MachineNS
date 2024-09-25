import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Функция для замены диапазонов на среднее значение
def convert_ranges_to_mean(series):
    def convert_value(value):
        if isinstance(value, str) and '-' in value:
            low, high = map(float, value.split('-'))
            return (low + high) / 2
        try:
            return float(value)
        except ValueError:
            return np.nan  # если значение невозможно преобразовать в число
    return series.apply(convert_value)

# Чтение файлов
df_gripp = pd.read_excel('грипп.xlsx')
df_cov = pd.read_excel('ковид.xlsx')

# Проверка названий столбцов
print("Названия столбцов Грипп:", df_gripp.columns)
print("Названия столбцов Ковид:", df_cov.columns)

# Проверка первых строк
print("Данные Грипп:")
print(df_gripp.head())
print("Данные Ковид:")
print(df_cov.head())

# Преобразование столбцов с диапазонами в числовой формат
columns_to_convert = ['Sаt O2 , % при госпитализации', 'Продолжительность госпитализации']
for col in columns_to_convert:
    df_gripp[col] = convert_ranges_to_mean(df_gripp[col])
    df_cov[col] = convert_ranges_to_mean(df_cov[col])

# Удаление строк с пропусками для ключевых столбцов
df_gripp_clean = df_gripp.dropna(subset=['Возраст'] + columns_to_convert)
df_cov_clean = df_cov.dropna(subset=['Возраст'] + columns_to_convert)

# Проверка размеров очищенных DataFrame
print("Размер Грипп после очистки:", df_gripp_clean.shape)
print("Размер Ковид после очистки:", df_cov_clean.shape)

# Настройка стиля графиков
sns.set(style="whitegrid")

# Функция для построения гистограммы по возрасту
def plot_age(df_gripp, df_cov):
    plt.figure(figsize=(10, 6))
    sns.histplot(df_gripp['Возраст'], color='blue', label='Грипп', kde=True, bins=20)
    sns.histplot(df_cov['Возраст'], color='red', label='Ковид', kde=True, bins=20)
    plt.title("Распределение возраста (Грипп vs Ковид)")
    plt.xlabel("Возраст")
    plt.ylabel("Частота")
    plt.legend()
    plt.show()

# Функция для построения диаграммы распределения по полу
def plot_gender(df_gripp, df_cov):
    plt.figure(figsize=(8, 6))
    gender_data = pd.DataFrame({
        'Грипп': df_gripp['Пол'].value_counts(),
        'Ковид': df_cov['Пол'].value_counts()
    })
    gender_data.plot(kind='bar', stacked=True, color=['blue', 'red'])
    plt.title("Распределение по полу (Грипп vs Ковид)")
    plt.xlabel("Пол")
    plt.ylabel("Количество пациентов")
    plt.show()

# Функция для построения гистограммы продолжительности госпитализации
def plot_hospitalization(df_gripp, df_cov):
    plt.figure(figsize=(10, 6))
    sns.histplot(df_gripp['Продолжительность госпитализации'], color='blue', label='Грипп', kde=True, bins=20)
    sns.histplot(df_cov['Продолжительность госпитализации'], color='red', label='Ковид', kde=True, bins=20)
    plt.title("Распределение продолжительности госпитализации (Грипп vs Ковид)")
    plt.xlabel("Продолжительность госпитализации (дни)")
    plt.ylabel("Частота")
    plt.legend()
    plt.show()

# Функция для построения гистограммы сатурации
def plot_saturation(df_gripp, df_cov):
    plt.figure(figsize=(10, 6))
    sns.histplot(df_gripp['Sаt O2 , % при госпитализации'], color='blue', label='Грипп', kde=True, bins=20)
    sns.histplot(df_cov['Sаt O2 , % при госпитализации'], color='red', label='Ковид', kde=True, bins=20)
    plt.title("Распределение сатурации при госпитализации (Грипп vs Ковид)")
    plt.xlabel("Сатурация O2 (%)")
    plt.ylabel("Частота")
    plt.legend()
    plt.show()

# Функция для построения гистограммы биохимических показателей крови
def plot_blood(df_gripp, df_cov, column_name):
    plt.figure(figsize=(10, 6))
    sns.histplot(df_gripp[column_name], color='blue', label='Грипп', kde=True, bins=20)
    sns.histplot(df_cov[column_name], color='red', label='Ковид', kde=True, bins=20)
    plt.title(f"Распределение {column_name} (Грипп vs Ковид)")
    plt.xlabel(column_name)
    plt.ylabel("Частота")
    plt.legend()
    plt.show()

# Определяем биохимические показатели
blood_columns = ['Эритроциты', 'Лейкоциты', 'Тромбоциты', 'СРБ', 'СОЭ']
for col in blood_columns:
    if col in df_gripp_clean.columns and col in df_cov_clean.columns:
        df_gripp_clean[col] = convert_ranges_to_mean(df_gripp_clean[col])
        df_cov_clean[col] = convert_ranges_to_mean(df_cov_clean[col])

# Визуализация
plot_age(df_gripp_clean, df_cov_clean)
plot_gender(df_gripp_clean, df_cov_clean)
plot_hospitalization(df_gripp_clean, df_cov_clean)
plot_saturation(df_gripp_clean, df_cov_clean)

# Гистограммы для биохимических показателей крови
for col in blood_columns:
    if col in df_gripp_clean.columns and col in df_cov_clean.columns:
        plot_blood(df_gripp_clean, df_cov_clean, col)
