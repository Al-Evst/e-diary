# Скрипт для управления оценками и похвалами школьного дневника #

## Скрипты позволяют: ##

1. Исправлять плохие оценки (2 и 3) на пятёрки

2. Удалять замечания ученику

3. Добавлять похвалу ученику по конкретному предмету

## Структура/Функции ##
* ```get_schoolkid_by_name``` — общая функция поиска ученика по части имени, с обработкой ошибок.

* ```fix_marks``` — исправляет все двойки и тройки на пятёрки для указанного ученика.

* ```remove_chastisements``` — удаляет все замечания ученика.

* ```create_commendation``` — создаёт похвалу на основе последнего урока по заданному предмету.

## Как использовать ##
Открой Django shell:
```
python manage.py shell
```
Импортируй функции:
```
from your_module import fix_marks, remove_chastisements, create_commendation
```
Запусти нужную функцию:
```
fix_marks()  # Исправит оценки Ване Фролову
remove_chastisements()  # Удалит замечания Феофану
create_commendation('Фролов Иван', 'Музыка')  # Добавит похвалу Ване Фролову по предмету
```
