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


def get_schoolkid_by_name(name_part):
   
    try:
        return Schoolkid.objects.get(full_name__icontains=name_part)
    except Schoolkid.DoesNotExist:
        logger.error(f'Ученик с именем, содержащим "{name_part}", не найден.')
    except Schoolkid.MultipleObjectsReturned:
        logger.error(f'Найдено несколько учеников с именем, содержащим "{name_part}". Уточните запрос.')
    return None


def fix_marks():
    schoolkid = get_schoolkid_by_name('Фролов Иван')
    if not schoolkid:
        return

    bad_marks = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3])
    bad_marks_count = bad_marks.count()
    bad_marks.update(points=5)
    logger.info(f'Ване Фролову исправлено {bad_marks_count} оценок. Все плохие оценки заменены на пятёрки.')


def remove_chastisements():
    schoolkid = get_schoolkid_by_name('Феофан')
    if not schoolkid:
        return

    chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    chastisements.delete()
    logger.info(f'Все замечания удалены для ученика {schoolkid.full_name}.')


def create_commendation(full_name_part, subject_title):
    schoolkid = get_schoolkid_by_name(full_name_part)
    if not schoolkid:
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
