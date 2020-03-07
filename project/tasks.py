import requests
import schedule

from .models import Functions


def get_generated_lists():
    """
    Generates `teachers`, `groups`, `auditoriums`, `subjects`
    lists what will be inserted into database

    :return:            (dict) dictionary of those lists
    """
    groups = requests.get('http://api.pnu-bot.pp.ua/api/groups').json()
    # groups = ['ІПЗ-11', 'ІПЗ-21', 'ІПЗ-31', 'ІПЗ-41', 'ІПЗ-1м', 'М-11', 'М-21']
    teachers_prev = []
    auds_prev = []
    subjects = []
    schedules = [requests.get(f'http://api.pnu-bot.pp.ua/api/schedule?group={group}&date_to=09.03.2020').json()
                 for group in groups]
    for schedule_element in schedules:
        if schedule_element['schedule']:
            group = schedule_element['group']
            items = schedule_element['schedule'][0]['items']
            for item in items:
                subject_num = int(item['number'])
                info = item['info'].split(' /  ')
                aud = info[0]
                teacher = ' '.join(info[1].split(' ')[:2])
                name = info[2]
                auds_prev.append(aud)
                teachers_prev.append(teacher)
                subjects.append((teacher, group, aud, subject_num, name))
    teachers_cur = list(dict.fromkeys(teachers_prev))
    auds_cur = [(a, i) for a in list(dict.fromkeys(auds_prev)) for i in range(1, 9)]
    # print(f'{groups}\n--------\n{teachers_cur}\n--------\n{auds_cur}\n--------\n{subjects}')
    return {'teachers': teachers_cur, 'groups': groups, 'auds': auds_cur, 'subjects': subjects}


def update_database():
    # Models Functions instance
    mf = Functions()

    # Dictionary of generated lists
    lists = get_generated_lists()

    # mf.delete_all()
    # mf.change_all_auds_status()
    mf.insert_teachers(lists['teachers'])
    mf.insert_groups(lists['groups'])
    mf.insert_auds(lists['auds'])
    mf.insert_subjects(lists['subjects'])
