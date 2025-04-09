from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route("/")
def index():
    # Ссылка на CSV из Google Таблицы
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRjUviiQ0tNUb4ZoE6-limatZVsu8KVhnRseksLoNeNeqFHDG8-x6tryZmsk5QZuJwTjOK20v6plMLd/pub?output=csv"

    try:
        # Загружаем данные из таблицы
        df = pd.read_csv(sheet_url)

        # Переименуем "Описание" → "Метрика" (если есть)
        if "Описание" in df.columns:
            df = df.rename(columns={"Описание": "Метрика"})

        # Удалим "Название метрики", если есть
        #if "Название метрики" in df.columns:
            #df = df.drop(columns=["Название метрики"])

        # Заменяем NaN на "—"
        df = df.fillna("—")

        # Преобразуем данные для шаблона
        columns = df.columns.tolist()
        rows = df.values.tolist()

        return render_template("index.html", columns=columns, rows=rows)

    except Exception as e:
        return f"<pre>Ошибка при загрузке данных:\n{e}</pre>"

if __name__ == "__main__":
    app.run(debug=True)

