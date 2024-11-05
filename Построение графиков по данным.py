import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# Загрузка данных с автоматическим преобразованием столбцов с датами
data = pd.read_excel('лист 2 общее.xlsx',
                     parse_dates=['Дата рождения', 'Дата госпитализации', 'Дата выписки', 'Дата начала заболевания'])


# Функция для построения графика с условием на значения в столбце "Шифр"
def plot_column_distribution(column_name):
    plt.figure(figsize=(12, 6))

    # Применяем условие на разделение по COVID-19 и гриппу
    sns.countplot(
        data=data,
        x=column_name,
        hue=data['Шифр'].apply(lambda x: 'Грипп' if 'Г' in str(x) else 'Ковид' if 'кф' in str(x) else ''),
        palette='viridis'
    )

    plt.title(f'Распределение по {column_name} (грипп vs ковид)')
    plt.xticks(rotation=45)
    plt.legend(title="Тип инфекции")
    plt.show()


# Построение графиков для всех столбцов данных
for column in data.columns:
    plot_column_distribution(column)