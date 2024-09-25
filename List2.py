import pandas as pd
import matplotlib.pyplot as plt

# Загружаем файл Excel
file_path = 'Болезни.xlsm'
df = pd.read_excel(file_path, sheet_name='Лист2')

# Очистка данных от пустых строк
df_clean = df.dropna(how='all')

# Удаление столбцов с названием Unnamed
df_clean = df_clean.loc[:, ~df_clean.columns.str.contains('^Unnamed')]

# Удаление лишних пробелов из названий столбцов
df_clean.columns = df_clean.columns.str.strip()

# Фильтрация умерших пациентов
df_filtered = df_clean[~df_clean['Шифр'].str.contains('смерть', na=False, case=False)]

# Разделение на две группы: грипп (Г) и ковид (U07)
df_gripp = df_filtered[df_filtered['Шифр'].str.contains('Г', na=False)]
df_cov = df_filtered[df_filtered['Шифр'].str.contains('кф', na=False)]

# Проверка названий столбцов
print("Названия столбцов в DataFrame:\n", df_gripp.columns.tolist())

# Проверка количества данных в каждой группе
print("Грипп:", df_gripp.shape)
print("Ковид:", df_cov.shape)

if df_gripp.empty:
    print("Предупреждение: В группе гриппа нет данных.")
if df_cov.empty:
    print("Предупреждение: В группе ковида нет данных.")

# Сохраняем отфильтрованные данные в новые Excel файлы
df_gripp.to_excel('грипп лист2.xlsx', index=False)
df_cov.to_excel('ковид лист2.xlsx', index=False)

# Загружаем уже отфильтрованные данные
df_gripp = pd.read_excel('грипп лист2.xlsx')
df_cov = pd.read_excel('ковид лист2.xlsx')


# Очистка столбца сатурации
def clean_saturation_column(df):
    df['Степень тяжести'] = pd.to_numeric(df['Степень тяжести'], errors='coerce')


# Очистка столбца сатурации
clean_saturation_column(df_gripp)
clean_saturation_column(df_cov)


# Функция анализа возраста
def analyze_age(df, group_name):
    if 'Возраст' in df.columns:
        avg_age = df['Возраст'].mean()
        print(f"{group_name} - Средний возраст: {avg_age:.2f} лет")
    else:
        print(f"{group_name} - Столбец 'Возраст' не найден.")


# Функция анализа пола
def analyze_gender(df, group_name):
    if 'Пол' in df.columns:
        gender_counts = df['Пол'].value_counts()
        print(f"{group_name} - Распределение по полу:\n{gender_counts}")
    else:
        print(f"{group_name} - Столбец 'Пол' не найден.")


# Функция анализа госпитализации
def analyze_hospitalization(df, group_name):
    if 'Дата госпитал.' in df.columns and 'Дата выписки' in df.columns:
        df['Длительность госпитализации'] = (
                    pd.to_datetime(df['Дата выписки']) - pd.to_datetime(df['Дата госпитал.'])).dt.days
        avg_hospitalization = df['Длительность госпитализации'].mean()
        print(f"{group_name} - Средняя длительность госпитализации: {avg_hospitalization:.2f} дней")
    else:
        print(f"{group_name} - Необходимые столбцы для анализа госпитализации не найдены.")


# Анализ сатурации
def analyze_saturation(df, group_name):
    saturation_column = 'Sat O2'
    if saturation_column in df.columns:
        avg_saturation = df[saturation_column].mean()
        print(f"{group_name} - Средняя сатурация при госпитализации: {avg_saturation:.2f}")

        # Построение графика
        plt.figure()
        df[saturation_column].hist(bins=10, edgecolor='black')
        plt.title(f'Сатурация пациентов при госпитализации ({group_name})')
        plt.xlabel('Сатурация (%)')
        plt.ylabel('Количество пациентов')
        plt.grid(False)
        plt.savefig(f'{group_name}_сатурация.png')
        plt.show()  # Отобразить график
        plt.close()
        print(f"График сатурации сохранен: {group_name}_сатурация.png")
    else:
        print(f"{group_name} - Столбец '{saturation_column}' не найден в данных.")


# Анализ сопутствующих заболеваний
def analyze_comorbidities(df, group_name):
    print(f"Анализ сопутствующих заболеваний для группы: {group_name}")
    if 'Категория сопутствующей патологии' in df.columns:
        diabetes_count = df['Категория сопутствующей патологии'].str.contains('Диабет',
                                                                              na=False).value_counts().replace(
            {False: 'Нет', True: 'Да'})
        print(f"{group_name} - Наличие диабета:\n{diabetes_count}")
        # Построение графика
        diabetes_count.plot(kind='bar', title='Наличие диабета', xlabel='Диабет', ylabel='Количество пациентов')
        plt.savefig(f'{group_name}_диабет.png')
        plt.show()
        print(f"График наличия диабета сохранен: {group_name}_диабет.png")
    else:
        print(f"{group_name} - Столбец 'Категория сопутствующей патологии' не найден.")

    # Анализ крови
    def analyze_blood(df, group_name):
        print(f"Начало анализа крови для {group_name}...")
        if 'Темпера тела' in df.columns:
            avg_temp = df['Темпера тела'].mean()
            print(f"{group_name} - Средняя температура тела: {avg_temp:.2f}°C")

            # Построение графика
            plt.figure()
            df['Темпера тела'].hist(bins=10, edgecolor='black')
            plt.title(f'Температура тела пациентов ({group_name})')
            plt.xlabel('Температура (°C)')
            plt.ylabel('Количество пациентов')
            plt.grid(False)
            plt.savefig(f'{group_name}_температура.png')
            plt.show()  # Отобразить график
            plt.close()
            print(f"График температуры сохранен: {group_name}_температура.png")
        else:
            print(f"{group_name} - Столбец 'Темпера тела' не найден.")

    # Анализ данных для каждой группы и построение графиков
    print("Анализ группы больных гриппом:")
    analyze_age(df_gripp, "Грипп")
    analyze_gender(df_gripp, "Грипп")
    analyze_hospitalization(df_gripp, "Грипп")
    analyze_saturation(df_gripp, "Грипп")
    analyze_comorbidities(df_gripp, "Грипп")
    analyze_blood(df_gripp, "Грипп")

    print("\nАнализ группы больных ковидом:")
    analyze_age(df_cov, "Ковид")
    analyze_gender(df_cov, "Ковид")
    analyze_hospitalization(df_cov, "Ковид")
    analyze_saturation(df_cov, "Ковид")
    analyze_comorbidities(df_cov, "Ковид")
    analyze_blood(df_cov, "Ковид")

    print("Графики успешно сохранены.")