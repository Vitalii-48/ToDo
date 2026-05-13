# Деплой на Render

Простий учбовий варіант деплою Flask-застосунку з SQLite.

## Кроки

```bash
git add .
git commit -m "Prepare app for deploy"
git push origin master
```

На Render:

1. New -> Web Service.
2. Підключити GitHub-репозиторій.
3. Render може взяти налаштування з `render.yaml`.

Якщо вводити вручну:

```text
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
```

Environment variable:

```text
TD_SECRET_KEY=будь-який-довгий-секретний-рядок
```

SQLite нормальний для учбового деплою, але дані можуть скидатися після redeploy.
