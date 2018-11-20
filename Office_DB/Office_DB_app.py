import pymysql.cursors

# Connect to the database
con = pymysql.connect(host='localhost',
                             user='USER_LOGIN', #insert login
                             password='USER_PASSWORD', # insert password
                             db='office_DB',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
cur = con.cursor()

from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

# Main page
@app.route('/')
def main_page():
    return render_template('main.html')

# Searching by employee name
@app.route('/by_employee')
def employee_search():
    cur.execute('select emp_id, emp_name from employees')
    emps = cur.fetchall()

    return render_template('search_by_employee.html', emps=emps)

# Result page
@app.route('/employee_data')
def employee_data():
    if request.args:
        emp_id = request.args['emp_form']
        emp_id_str = str(emp_id)
        
        cur.execute('select employees.emp_name, employees.emp_job, departments.dep_name, \
                    workspace.place_name, rooms.room_name, rooms.room_floor\
                    from employees \
                    left join assignment \
                    on employees.emp_id = assignment.emp_id \
                    left join departments \
                    on employees.emp_dep = departments.dep_id \
                    left join workspace \
                    on assignment.place_id = workspace.place_id \
                    left join rooms \
                    on workspace.room_id = rooms.room_id \
                    where employees.emp_id = ' + emp_id_str)
        
        inj = cur.fetchall()
        res = inj[0]
        
    return render_template('employee_data.html', emp_id_str = emp_id_str, res = res)

# Editing employee data
@app.route('/edit_employee')
def edit_employee():
    if request.args:
        emp_id = request.args['emp_id']
        cur.execute('select emp_name, emp_job, emp_dep from employees where emp_id=' + emp_id)
        emp_info = cur.fetchall()
        cur.execute('select dep_name, dep_id from departments')
        deps = cur.fetchall()
    return render_template('edit_employee.html', emp_info=emp_info, deps=deps, emp_id=emp_id)  

# Updating employee profile
@app.route('/update_employee')
def update_employee():
    if request.args:
        name = request.args['new_name']
        job = request.args['new_job']
        dep = request.args['new_dep']
        emp_id = request.args['emp_id']
        try:
            cur.execute('update employees set emp_name="'+name+'", emp_job="'+job+'", emp_dep='+dep+' where emp_id='+emp_id)
            ret_str = '<html><body><p>Профиль сотрудника обновлён.</p><p><a href="/">Вернуться на главную</a></p></body></html>'
            con.commit()
        except TypeError as e:
            print(e)
            ret_str = 'error '+e
        return ret_str

# Deleting employee profile
@app.route('/delete_employee')
def delete_employee():
    if request.args:
        try:
            cur.execute('delete from assignment where emp_id=' + request.args['emp_id'])
            cur.execute('delete from employees where emp_id=' + request.args['emp_id'])
            ret_str = '<html><body><p>Профиль сотрудника удалён.</p><p><a href="/">Вернуться на главную</a></p></body></html>'
            con.commit()
        except TypeError as e:
            print(e)
            ret_str = 'error '+e
        return ret_str

# Searching by room
@app.route('/by_room')
def room_search():
    cur.execute('select room_id, room_name from rooms')
    rooms = cur.fetchall()

    return render_template('search_by_room.html', rooms=rooms)

# Result page for rooms
@app.route('/room_data')
def room_data():
    if request.args:
        room_id = request.args['room_form']
        room_id_str = str(room_id)
        
        cur.execute('select employees.emp_name, employees.emp_job, departments.dep_name, assignment.ass_id, \
                    workspace.place_id, workspace.place_name, rooms.room_name, rooms.room_floor \
                    from employees \
                    inner join assignment \
                    on employees.emp_id = assignment.emp_id \
                    inner join departments \
                    on employees.emp_dep = departments.dep_id \
                    right join workspace \
                    on assignment.place_id = workspace.place_id \
                    right join rooms \
                    on workspace.room_id = rooms.room_id \
                    where rooms.room_id = ' + room_id_str)
        
        res = cur.fetchall() 
        
        cur.execute('select employees.emp_name, employees.emp_id from employees \
                    left join assignment on employees.emp_id = assignment.emp_id \
                    where assignment.ass_id is null')
        free_emps = cur.fetchall()
        
    return render_template('room_data.html', room_id_str = room_id_str, res = res, free_emps = free_emps)

# Deleting workplace
@app.route('/delete_place')
def delete_place():
    if request.args:
        try:
            cur.execute('delete from workspace where place_id=' + request.args['place_id'])
            cur.execute('delete from assignment where place_id=' + request.args['place_id'])
            ret_str = '<html><body><p>Рабочее место удалено.</p><p><a href="/">Вернуться на главную</a></p></body></html>'
            con.commit()
        except TypeError as e:
            print(e)
            ret_str = 'error '
        return ret_str

# Deleting employee from a place
@app.route('/delete_assignment')
def delete_assignment():
    if request.args:
        try:
            cur.execute('delete from assignment where ass_id=' + request.args['ass_id']) 
            ret_str = '<html><body><p>Сотрудник удалён с данного рабочего места.</p><p><a href="/">Вернуться на главную</a></p></body></html>'
            con.commit()
        except TypeError as e:
            ret_str = 'error '+e
        return ret_str

# Assign an employee to a place
@app.route('/assign_emp')
def assign_emp():
    if request.args:
        place_id = request.args['place_id']
        emp_id = request.args['emp_id']
        try:
            cur.execute('insert into assignment (place_id, emp_id) values ("' + place_id + '", "' + emp_id + '")')
            ret_str = '<html><body><p>Сотрудник назначен на данное место.</p><p><a href="/">Вернуться на главную</a></p></body></html>'
            con.commit()
        except TypeError as e:
            ret_str = 'error '+e
        return ret_str   
            
# Adding a new workplace
@app.route('/create_place')
def create_place():
    if request.args:
        new_place = request.args['new_place']
        room_id = request.args['room_id']
        try:
            cur.execute('insert into workspace (room_id, place_name) values ("' + room_id + '", "' + new_place + '")')
            ret_str = '<html><body><p>Новое рабочее место создано.</p><p><a href="/">Вернуться на главную</a></p></body></html>'
            con.commit()
        except pymysql.err.IntegrityError as e:
            if e.args[0]==1062:
                ret_str = 'Ошибка: такое название уже используется'
            else:
                ret_str = 'Error: '+str(e.args[0])
    return(ret_str)

# Adding a new employee
@app.route('/new_employee')
def new_employee(): 
    cur.execute('select dep_name, dep_id from departments')
    deps = cur.fetchall()
    return render_template('new_employee.html', deps = deps)

# Adding a new employee
@app.route('/save_emp')
def save_emp():
    if request.args:
        name = request.args['name']
        job = request.args['job']
        dep = request.args['dep']
        try:
            cur.execute('insert into employees (emp_name, emp_job, emp_dep) values ("' + name + '", "' + job + '", "' + dep + '")')
            ret_str = '<html><body><p>Новый сотрудник добавлен.</p><p><a href="/">Вернуться на главную</a></p></body></html>'
            con.commit()
        except TypeError as e:
            ret_str = 'error '+e
        return ret_str 
    return(ret_str)

if __name__ == '__main__':
    app.run(debug=True)

con.close()
