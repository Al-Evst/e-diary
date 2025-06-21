import random
import logging
from datacenter.models import Schoolkid, Lesson, Commendation, Mark, Chastisement
from datacenter.praises import PRAISES


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)


def fix_marks():
    try:
        schoolkid = Schoolkid.objects.get(full_name__icontains='Фролов Иван')
    except Schoolkid.DoesNotExist:
        logger.error('Ученик "Фролов Иван" не найден.')
        return
    except Schoolkid.MultipleObjectsReturned:
        logger.error('Найдено несколько учеников с именем "Фролов Иван". Уточните запрос.')
        return

    bad_marks = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3])
    bad_marks_count = bad_marks.count()
    bad_marks.update(points=5)
    logger.info(f'Ване Фролову исправлено {bad_marks_count} оценок. Все плохие оценки заменены на пятёрки.')


def remove_chastisements():
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains='Феофан')
    except Schoolkid.DoesNotExist:
        logger.error("Ученик Феофан не найден")
        return
    except Schoolkid.MultipleObjectsReturned:
        logger.error("Найдено несколько учеников с именем Феофан")
        return

    chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    chastisements.delete()
    logger.info("Все замечания удалены для ученика Феофан")


def create_commendation(full_name_part, subject_title):
    try:
        schoolkid = Schoolkid.objects.get(full_name__icontains=full_name_part)
    except Schoolkid.DoesNotExist:
        logger.error(f'Ученик с именем, содержащим "{full_name_part}", не найден.')
        return
    except Schoolkid.MultipleObjectsReturned:
        logger.error(f'Найдено несколько учеников с именем, содержащим "{full_name_part}". Уточните запрос.')
        return

    last_lesson = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject__title=subject_title
    ).order_by('-date').first()

    if not last_lesson:
        logger.warning(f'Уроки по предмету "{subject_title}" не найдены для этого ученика.')
        return

    praise_text = random.choice(PRAISES)

    commendation = Commendation.objects.create(
        text=praise_text,
        created=last_lesson.date,
        schoolkid=schoolkid,
        subject=last_lesson.subject,
        teacher=last_lesson.teacher
    )
    commendation.save()
    logger.info(f'Похвала "{praise_text}" добавлена для {schoolkid.full_name} по предмету "{subject_title}" на дату {last_lesson.date}.')