# HANDORA

Навчальний маркетплейс крафтових товарів та хендмейду на **Python / Django**, PostgreSQL, HTML5, CSS3 і JavaScript.

## Можливості
- каталог товарів і фільтрування за категоріями;
- сторінки майстрів і товарів;
- реєстрація, авторизація та профіль;
- сесійний кошик;
- оформлення замовлення з перевіркою кількості й доступного залишку;
- адміністративна панель Django, світла й темна теми.

## Локальний запуск (PowerShell)
1. Потрібні Python 3.12+ та PostgreSQL.
2. Створи віртуальне середовище: `py -3.12 -m venv .venv`
3. Активуй: `.\.venv\Scripts\Activate.ps1`
4. Встанови пакети: `pip install -r requirements.txt`
5. Скопіюй `.env.example` у `.env`. **Згенеруй власний SECRET_KEY**, задай локальні DB_NAME, DB_USER, DB_PASSWORD, DB_HOST та DB_PORT. Не публікуй `.env`.
6. Створи відповідну базу та роль у PostgreSQL.
7. Виконай `python manage.py migrate`, `python manage.py createsuperuser` (за потреби) і `python manage.py runserver`.
8. Відкрий http://127.0.0.1:8000/ .

## Тестування
Для ізольованого тестового запуску без PostgreSQL:

```powershell
$env:DJANGO_SETTINGS_MODULE="config.test_settings"
python manage.py test accounts cart orders -v 2
```

GitHub Actions виконує ті самі перевірки для push і pull request. **Не вважай тести пройденими до появи успішного статусу CI.**

## Безпека
Не коміть `.env`, `.venv/`, `db.sqlite3` та файли з персональними даними. Якщо секрет раніше був опублікований, його треба замінити: просто видалити файл із поточної гілки недостатньо. Для очищення старої історії Git потрібна окрема процедура з узгодженням змін для всіх копій репозиторію.
