import pandas as pd
import tkinter as tk
from tkinter import ttk

# Загрузка данных
data = pd.read_excel('Грипп+ковид(подправленное от дат).xlsx')
data = data.dropna(subset=['Шифр'])  # Убираем строки с NaN в 'Шифр'

# Фильтрация по заболеванию
flu_data = data[data['Шифр'].str.startswith('Г')]
covid_data = data[data['Шифр'].str.contains('кф')]


# Функция для форматирования распределения по полу
def format_gender_distribution(data):
    gender_counts = data['Пол'].value_counts()
    male_count = gender_counts.get(1, 0)  # Если нет мужчин, значение будет 0
    female_count = gender_counts.get(0, 0)  # Если нет женщин, значение будет 0
    return f"Мужчины: {male_count}, Женщины: {female_count}"


# Вычисления показателей
results = {
    "Средний возраст - Грипп": flu_data['Возраст'].mean(),
    "Средний возраст - COVID": covid_data['Возраст'].mean(),
    "Распределение по полу для Гриппа": format_gender_distribution(flu_data),
    "Распределение по полу для COVID": format_gender_distribution(covid_data),
    "Средняя продолжительность госпитализации - Грипп": flu_data['Продолжительность госпитализации'].mean(),
    "Средняя продолжительность госпитализации - COVID": covid_data['Продолжительность госпитализации'].mean(),
    "Средняя сатурация - Грипп": flu_data['Sat O2 %'].mean(),
    "Средняя сатурация - COVID": covid_data['Sat O2 %'].mean(),
    "Средний уровень СРБ - Грипп": flu_data['СРБ мг/л'].mean(),
    "Средний уровень СРБ - COVID": covid_data['СРБ мг/л'].mean(),
    "Средний уровень эритроцитов - Грипп": flu_data['Эритроциты'].mean(),
    "Средний уровень эритроцитов - COVID": covid_data['Эритроциты'].mean(),
    "Средний уровень лейкоцитов - Грипп": flu_data['Лейкоциты'].mean(),
    "Средний уровень лейкоцитов - COVID": covid_data['Лейкоциты'].mean(),
    "Средний уровень тромбоцитов - Грипп": flu_data['Тромбоциты'].mean(),
    "Средний уровень тромбоцитов - COVID": covid_data['Тромбоциты'].mean(),
    "Средний уровень СОЭ - Грипп": flu_data['СОЭ мм/ч'].mean(),
    "Средний уровень СОЭ - COVID": covid_data['СОЭ мм/ч'].mean()
}

# Преобразуем данные в DataFrame для отображения
df_results = pd.DataFrame(list(results.items()), columns=["Показатель", "Значение"])


# Функция для формирования текстовых выводов
def generate_comparative_analysis():
    analysis = ""

    if results["Средний возраст - Грипп"] < results["Средний возраст - COVID"]:
        analysis += "1. Грипп чаще встречается у более молодых пациентов, чем COVID.\n"
    else:
        analysis += "1. COVID чаще встречается у более молодых пациентов, чем грипп.\n"

    if results["Средняя продолжительность госпитализации - Грипп"] < results[
        "Средняя продолжительность госпитализации - COVID"]:
        analysis += "2. Пациенты с COVID проводят больше времени в больнице, чем с гриппом.\n"
    else:
        analysis += "2. Пациенты с гриппом проводят больше времени в больнице, чем с COVID.\n"

    if results["Средняя сатурация - Грипп"] > results["Средняя сатурация - COVID"]:
        analysis += "3. У пациентов с гриппом наблюдается немного более высокая сатурация, чем у пациентов с COVID.\n"
    else:
        analysis += "3. У пациентов с COVID наблюдается немного более высокая сатурация, чем у пациентов с гриппом.\n"

    if results["Средний уровень СРБ - Грипп"] < results["Средний уровень СРБ - COVID"]:
        analysis += "4. Уровень СРБ выше у пациентов с COVID, что может свидетельствовать о более выраженной воспалительной реакции.\n"
    else:
        analysis += "4. Уровень СРБ выше у пациентов с гриппом.\n"

    if results["Средний уровень эритроцитов - Грипп"] < results["Средний уровень эритроцитов - COVID"]:
        analysis += "5. У пациентов с COVID наблюдается более высокий уровень эритроцитов.\n"
    else:
        analysis += "5. У пациентов с гриппом наблюдается более высокий уровень эритроцитов.\n"

    if results["Средний уровень лейкоцитов - Грипп"] < results["Средний уровень лейкоцитов - COVID"]:
        analysis += "6. У пациентов с COVID выше уровень лейкоцитов, что может говорить о различиях в иммунной реакции.\n"
    else:
        analysis += "6. У пациентов с гриппом выше уровень лейкоцитов.\n"

    return analysis


# Создаем окно
root = tk.Tk()
root.title("Результаты анализа")

# Настроим таблицу для выводов
tree = ttk.Treeview(root, columns=("Показатель", "Значение"), show="headings", height=10)
tree.heading("Показатель", text="Показатель")
tree.heading("Значение", text="Значение")

# Вставляем данные в таблицу
for index, row in df_results.iterrows():
    tree.insert("", "end", values=(row["Показатель"], row["Значение"]))

# Размещаем таблицу в окне
tree.pack(padx=10, pady=10)

# Текстовое поле для выводов
label = tk.Label(root, text="Сравнительный анализ: \n" + generate_comparative_analysis(), justify="left", anchor="w")
label.pack(padx=10, pady=10)

# Запуск приложения
root.mainloop()
