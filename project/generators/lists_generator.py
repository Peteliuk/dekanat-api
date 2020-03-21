import grequests


def get_generated_lists():
    """
    Generates `teachers`, `groups`, `auditoriums`, `subjects`
    lists what will be inserted into database
    and `time bounds` list what will help to generate subject number by time

    variables:
        teachers_cur:       (list<string>) list of teachers names
        groups:             (list<string>) list of groups names
        auds_cur:           (list<touple<string, int>>) list of auditoriums parameters
        subjects:           (list<touple<string, string, string, int, string>>)
                            list of subjects parameters
        time_bounds_cur:    (list<touple<string, string, int>>)
                            list of touples with subject's start time, end time and number

    :return:                (dict<key:list>) dictionary of those lists
    """
    # request_groups = (grequests.get('http://api.pnu-bot.pp.ua/api/groups'),)
    # groups = grequests.map(request_groups)[0].json()
    groups = ['ІПЗ-11', 'ІПЗ-21', 'ІПЗ-31', 'ІПЗ-41', 'ІПЗ-1м',
              'М(ас)-11', 'М(ас)-21', 'М(ас)-31', 'М(ас)-41', 'М(докт)-2',
              'М-11', 'М-21', 'М-31', 'М-41', 'М -31', 'М- 41',
              'ПМ -3', "ПМ -4", "ПМк-11", "ПМк-12", "ПМк-21", "ПМк-22",
              "ПМк-31", "ПМк-32", "ПМк-41", "ПМк-42", "ПММ -21", "ПММ-11", "ПММ-2",
              'С-3', 'С-4',
              "ІСТ((з)-11", "ІСТ(з)-21", "ІСТ-11", "ІСТ-21", "ІСТ-31",
              "КН(з)-11", "КН(з)-21", "КН(з)-31", "КН(з)-41", "КНМ-11",
              "КНМ-21", "КН-11", "КН-21", "КН-31", "КН-41", "КН-42",
              "СО(М)(з)-3", "СО(М)(з)-4", "СО(М)з-11", "СО(М)з-21", "СО(М)м-11",
              "СО(М)-11", "СО(М)-2", "СО(М)-3", "СО(М)-4",
              "СО(І) - 2", "СО(І)-11", "СО(І)-3", "СО(І)-4", "СО(І)з-31", "СО(І)з-41", "СО(І)м-11", "СО(І)м-21"
              ]
    teachers_prev = []
    auds_prev = []
    subjects = []
    time_bounds_prev = []
    requests = (grequests.get(f'http://api.pnu-bot.pp.ua/api/schedule?group={group}') for group in groups)
    responses = grequests.map(requests)
    for response in responses:
        schedule = response.json() if response else {'schedule': []}
        if schedule['schedule']:
            group = schedule['group']
            items = schedule['schedule'][0]['items']
            for item in items:
                subject_num = int(item['number'])
                time_bound = item['time_bounds'].split(' - ')
                time_bounds_prev.append((time_bound[0], time_bound[1], subject_num))
                info = item['info'].split(' /  ')
                if info[0][0] != ' ':
                    aud = info[0]
                    n = 2 if '.' in info[1].split()[1] else 3
                    teacher = ' '.join(info[1].split()[:n])
                    name = info[2] if len(info) >= 4 else ' '.join(info[1].split()[n:])
                auds_prev.append(aud)
                teachers_prev.append(teacher)
                subjects.append((teacher, group, aud, subject_num, name))
    teachers_cur = list(dict.fromkeys(teachers_prev))
    auds_cur = [(a, i) for a in list(dict.fromkeys(auds_prev)) for i in range(1, 9)]
    time_bounds_cur = list(dict.fromkeys(time_bounds_prev))
    # print(f'{groups}\n--------\n{teachers_cur}\n--------\n{auds_cur}')
    # print(f'--------\n{subjects}\n--------\n{time_bounds_cur}')
    return {'teachers': teachers_cur,
            'groups': groups,
            'auds': auds_cur,
            'subjects': subjects,
            'time_bounds': time_bounds_cur
            }


if __name__ == '__main__':
    get_generated_lists()
