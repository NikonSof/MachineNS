import pandas as pd

# Загружаем файл Excel
file_path = 'Болезни.xlsm'
df = pd.read_excel(file_path, sheet_name='Лист1')

# Очистка данных от пустых строк
df_clean = df.dropna(how='all')

# Фильтрация умерших пациентов
df_filtered = df_clean[~df_clean['Исход течения болезни'].str.contains('смерть', na=False, case=False)]

# Разделение на две группы: грипп (Г) и ковид (U07)
df_gripp = df_filtered[df_filtered['Диагноз'].str.contains('Г', na=False)]
df_cov = df_filtered[df_filtered['Диагноз'].str.contains('U07', na=False)]

# Проверка количества данных в каждой группе
print("Грипп:", df_gripp.shape)
print("Ковид:", df_cov.shape)

if df_gripp.empty:
    print("Предупреждение: В группе гриппа нет данных.")
if df_cov.empty:
    print("Предупреждение: В группе ковида нет данных.")

# Сохраняем отфильтрованные данные в новые Excel файлы
df_gripp.to_excel('грипп.xlsx', index=False)
df_cov.to_excel('ковид.xlsx', index=False)

# Загружаем уже отфильтрованные данные
df_gripp = pd.read_excel('грипп.xlsx')
df_cov = pd.read_excel('ковид.xlsx')

# Функция для очистки и преобразования столбца сатурации
def clean_saturation_column(df):
    df['Sаt O2 , % при госпитализации'] = pd.to_numeric(df['Sаt O2 , % при госпитализации'], errors='coerce')

# Очистка столбца сатурации
clean_saturation_column(df_gripp)
clean_saturation_column(df_cov)

# Анализ по возрасту
def analyze_age(df, group_name):
    avg_age = df['Возраст'].mean()
    std_age = df['Возраст'].std()
    print(f"{group_name} - Средний возраст: {avg_age:.2f}, Стандартное отклонение: {std_age:.2f}")

# Анализ по полу
def analyze_gender(df, group_name):
    gender_counts = df['Пол'].value_counts()
    print(f"{group_name} - Пол:\n{gender_counts}")

# Анализ по продолжительности госпитализации
def analyze_hospitalization(df, group_name):
    avg_duration = df['Продолжительность госпитализации'].mean()
    median_duration = df['Продолжительность госпитализации'].median()
    print(f"{group_name} - Средняя продолжительность госпитализации: {avg_duration:.2f}, Медиана: {median_duration:.2f}")

# Анализ по сатурации
def analyze_saturation(df, group_name):
    avg_saturation = df['Sаt O2 , % при госпитализации'].mean()
    print(f"{group_name} - Средняя сатурация при госпитализации: {avg_saturation:.2f}")

# Анализ биохимических показателей крови
def analyze_blood(df, group_name):
    blood_cols = ['Эритроциты', 'Лейкоциты', 'Тромбоциты', 'СРБ', 'СОЭ']
    for col in blood_cols:
        if col in df.columns:
            avg_value = df[col].mean()
            print(f"{group_name} - Средний {col}: {avg_value:.2f}")

# Анализ данных для каждой группы
print("Анализ группы больных гриппом:")
analyze_age(df_gripp, "Грипп")
analyze_gender(df_gripp, "Грипп")
analyze_hospitalization(df_gripp, "Грипп")
analyze_saturation(df_gripp, "Грипп")
analyze_blood(df_gripp, "Грипп")

print("\nАнализ группы больных ковидом:")
analyze_age(df_cov, "Ковид")
analyze_gender(df_cov, "Ковид")
analyze_hospitalization(df_cov, "Ковид")
analyze_saturation(df_cov, "Ковид")
analyze_blood(df_cov, "Ковид")
