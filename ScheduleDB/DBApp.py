import sqlite3
con = sqlite3.connect('uniDB.db', check_same_thread = False)
cur = con.cursor()

from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/check')
def checking():
    cur.execute('select group_id, group_name from students')
    groups = cur.fetchall()
    
    cur.execute('select day_id, day_name from weekdays')
    days = cur.fetchall()
    
    return render_template('parametrs.html', groups=groups, days=days)

@app.route('/results')
def output():
    if request.args:
        group = request.args['group_form']
        day = request.args['day_form']
                    
        cur.execute('select group_name from students where group_id =' + str(group))
        group_name = str(cur.fetchall())
        group_name = group_name.strip("[],()'")

        cur.execute('select day_name from weekdays where day_id =' + str(day))
        day_name = str(cur.fetchall())
        day_name = day_name.strip("[],()'")
        
        cur.execute('select * from schedule where day_id = ' + str(day) + ' and group_id = ' + str(group))
        rawdata = cur.fetchall()

        all_classes = [] # Здесь будут данные для таблицы
        
        for i in rawdata:
            class_info = []

            class_id = str(i[0]) # id пары
            class_num = str(i[2]) # Вытаскиваем номер пары
            room_id = str(i[4]) # Вытаскиваем id аудитории
            subject_id = str(i[6]) # id дисциплины
            type_id = str(i[7]) # id вида занятия
            prof_id = str(i[5]) # id преподавателя

            class_info.append(class_num)

            cur.execute('select time from timetable where time_id = ' + class_num)
            times = str(cur.fetchall())
            times = times.strip("[],()'")
            class_info.append(times)

            cur.execute('select room_name from rooms where room_id = ' + room_id)
            rooms = str(cur.fetchall())
            rooms = rooms.strip("[],()'")
            class_info.append(rooms)

            cur.execute('select class_name from classes_list where class_name_id = ' + subject_id)
            subjects = str(cur.fetchall())
            subjects = subjects.strip("[],()'")
            class_info.append(subjects)

            cur.execute('select type_name from class_types where type_id = ' + type_id)
            types = str(cur.fetchall())
            types = types.strip("[],()'")
            class_info.append(types)

            cur.execute('select prof_name from professors where prof_id = ' + prof_id)
            profs = str(cur.fetchall())
            profs = profs.strip("[],()'")
            class_info.append(profs)

            class_info.append(class_id)

            all_classes.append(class_info)
        
        return render_template('result.html', group_name=group_name, day_name=day_name, \
                               all_classes=all_classes)
    return render_template('result.html')


@app.route('/edit')
def editing():
    if request.args:
        mode = request.args['mode_form']
        current_class = 0 #по дефолту текущий id записи - ноль
        current_class_data = [] #по дефолту данные текущей записи - пустые
        cur.execute('select day_id, day_name from weekdays')
        days = cur.fetchall()
        cur.execute('select time_id, time from timetable')
        times = cur.fetchall()
        cur.execute('select room_id, room_name from rooms')
        rooms = cur.fetchall()
        cur.execute('select group_id, group_name from students')
        groups = cur.fetchall()
        cur.execute('select prof_id, prof_name from professors')
        profs = cur.fetchall()
        cur.execute('select class_name_id, class_name from classes_list')
        disciplines = cur.fetchall()
        cur.execute('select type_id, type_name from class_types')
        types = cur.fetchall()
        
        if mode == 'edit':
            current_class = request.args['class_id'] #обрабатываем id для edit
            cur.execute('select * from schedule where class_id = ' + str(current_class))
            current_class_data = cur.fetchall()
            current_class_data = current_class_data[0]
        

    return render_template('edit_schedule.html', mode=mode, current_class=current_class, days=days, times=times, rooms=rooms, \
                           groups=groups, profs=profs, disciplines=disciplines, types=types, current_class_data=current_class_data)

@app.route('/done')
def modifying():
    if request.args:
        if request.args['mode']=='add':
            prof_name = request.args.get('prof_name')
            group_name = request.args.get('group_name')
            weekday = request.args.get('weekday')
            class_time = request.args.get('class_time')
            room_name = request.args.get('room_name')
            class_name = request.args.get('class_name')
            class_type = request.args.get('class_type')
        
            try:
                cur.execute('insert into schedule (day_id, time_id, group_id, room_id, prof_id, class_name_id, type_id) values ("' + \
                                weekday + '", "' + class_time +'", "' + group_name + '", "' + room_name + '", "' + \
                                prof_name + '", "' + class_name + '", "' + class_type + '")')
                ret_str = '<html><body><p>Готово!</p><p><a href="/">Вернуться на главную</a></p></body></html>'
                con.commit()
            except sqlite3.IntegrityError as e:
                if 'UNIQUE' in e.args[0]:
                    ret_str = 'Ошибка: неуникальные данные'
                else:
                    ret_str = 'Error: '+e.args[0]
            return ret_str
        elif request.args['mode']=='delete':
            try:
                cur.execute('delete from schedule where class_id='+request.args['class_id'])
                ret_str = '<html><body><p>Готово!</p><p><a href="/">Вернуться на главную</a></p></body></html>'
                con.commit()
            except sqlite3.IntegrityError as e:
                ret_str = 'Error: '+e.args[0]
            return ret_str
        elif request.args['mode']=='edit':
            prof_name = request.args.get('prof_name')
            group_name = request.args.get('group_name')
            weekday = request.args.get('weekday')
            class_time = request.args.get('class_time')
            room_name = request.args.get('room_name')
            class_name = request.args.get('class_name')
            class_type = request.args.get('class_type')
            
            try:
                cur.execute('update schedule set day_id='+weekday+', time_id='+class_time+', group_id='+group_name+ \
                            ', room_id='+room_name+', prof_id='+prof_name+', class_name_id='+class_name+', type_id='+class_type+ \
                            ' where class_id='+request.args['class_id'])
                ret_str = '<html><body><p>Готово!</p><p><a href="/">Вернуться на главную</a></p></body></html>'
                con.commit()
            except sqlite3.IntegrityError as e:
                if 'UNIQUE' in e.args[0]:
                    ret_str = 'Ошибка: неуникальные данные'
                else:
                    ret_str = 'Error: '+e.args[0]
            return ret_str


if __name__ == '__main__':
    app.run(debug=True)
