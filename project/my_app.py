from flask import Flask
from flask import render_template
from flask import request
from collections import Counter
import json

app = Flask(__name__)


@app.route('/')
def index():
    if request.args:
        f = open ('verbs.txt', 'a', encoding = 'utf-8')
        f.write ('%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s\n' % (request.args.get('language'), request.args.get('apple'), \
                 request.args.get('hands'), request.args.get('floor'), request.args.get('teeth'), request.args.get('hair'), \
                 request.args.get('room'), request.args.get('body'), request.args.get('window'), request.args.get('face'), \
                 request.args.get('clothes'), request.args.get('dishes')))
        f.close()
    return render_template('index.html')

@app.route('/stats')
def stats():
    langs = []
    apple = []
    hands = []
    floor = []
    teeth = []
    hair = []
    room = []
    body = []
    window = []
    face = []
    clothes = []
    dishes = []
    
    f = open ('verbs.txt', 'r', encoding = 'utf-8')
    text = f.readlines()
    num = 0
    for line in text:
        num += 1
        x = line.split(', ')
        
        langs.append(x[0])
        apple.append(x[1])
        hands.append(x[2])
        floor.append(x[3])
        teeth.append(x[4])
        hair.append(x[5])
        room.append(x[6])
        body.append(x[7])
        window.append(x[8])
        face.append(x[9])
        clothes.append(x[10])
        dishes.append(x[11])
        
    f.close
    
    mostlangs = []    
    replang = {}
    repl = 0
    statslang = ''
    for l in langs:
        if l in replang:
            replang[l] += 1
        else:
            replang[l] = 1
    for lan in replang:
        if replang[lan] > repl:
            repl = replang[lan]
    for look in replang:
            if repl == replang[look]:
                mostlangs.append(look)
    for stat in mostlangs:
        statslang += '• ' + str(stat) + '  '

    langs2 = []
    for i in langs:
        if i not in langs2:
            langs2.append(i)
    linelang = ''
    for lang in langs2:
        linelang += lang + ', '
        
    apple2 = []
    for a in apple:
        if a not in apple2:
           apple2.append(a)
    lineapple = ''
    for appl in apple2:
        lineapple += appl + ', '
        
    hands2 = []
    for h in hands:
        if h not in hands2:
            hands2.append(h)
    linehands = ''
    for hnd in hands2:
        linehands += hnd + ', '
        
    floor2 = []
    for fl in floor:
        if fl not in floor2:
            floor2.append(fl)
    linefloor = ''
    for flr in floor2:
        linefloor += flr + ', '
        
    teeth2 = []
    for t in teeth:
        if t not in teeth2:
            teeth2.append(t)
    lineteeth = ''
    for tth in teeth2:
        lineteeth += tth + ', '
        
    hair2 = []
    for hr in hair:
        if hr not in hair2:
            hair2.append(hr)
    linehair = ''
    for hai in hair2:
        linehair += hai + ', '
        
    room2 = []
    for r in room:
        if r not in room2:
            room2.append(r)
    lineroom = ''
    for rm in room2:
        lineroom += rm + ', '
        
    body2 = []
    for b in body:
        if b not in body2:
            body2.append(b)
    linebody = ''
    for bd in body2:
        linebody += bd + ', '
        
    window2 = []
    for w in window:
        if w not in window2:
            window2.append(w)
    linewindow = ''
    for ww in window2:
        linewindow += ww + ', '
        
    face2 = []
    for fc in face:
        if fc not in face2:
            face2.append(fc)
    lineface = ''
    for fac in face2:
        lineface += fac + ', '
        
    clothes2 = []
    for cl in clothes:
        if cl not in clothes2:
            clothes2.append(cl)
    lineclothes = ''
    for clo in clothes2:
        lineclothes += clo + ', '
        
    dishes2 = []
    for d in dishes:
        if d not in dishes2:
            dishes2.append(d)
    linedishes = ''
    for dis in dishes2:
        linedishes += dis + ', '
        
    return render_template('stats.html', repl=repl, statslang=statslang, num=num, linelang=linelang, lineapple=lineapple, linehands=linehands, \
                           linefloor=linefloor, lineteeth=lineteeth, linehair=linehair, lineroom=lineroom, \
                           linebody=linebody, linewindow=linewindow, lineface=lineface, lineclothes=lineclothes, \
                           linedishes=linedishes)

@app.route('/json')
def jsonfun():
    f = open ('verbs.txt', 'r', encoding = 'utf-8')
    text = f.readlines()
    arr1 = []
    alldata = []
    for line in text:
        d = {}
        arr = []
        arr1 = line.split(', ')
        for i in arr1:
            i = i.strip('\n')
            arr.append(i)
        d['language'] = arr[0]
        d['apple'] = arr[1]
        d['hands'] = arr[2]
        d['floor'] = arr[3]
        d['teeth'] = arr[4]
        d['head'] = arr[5]
        d['room'] = arr[6]
        d['body'] = arr[7]
        d['window'] = arr[8]
        d['face'] = arr[9]
        d['clothes'] = arr[10]
        d['dishes'] = arr[11]
        alldata.append(d)
        
    data = json.dumps(alldata, ensure_ascii=False)
    return render_template ('jsons.html', data=data)

@app.route('/search')
def search():
    lang= ''
    global language_x
    if request.args:
        lang += request.args['language']
        language_x += lang
    return render_template ('search.html')

@app.route('/results')
def results():
    global language_x
    resultats = ''
    
    f = open ('verbs.txt', 'r', encoding = 'utf-8')
    text = f.readlines()
    arr1 = []
    allres = []
    for line in text:
        arr = []
        arr1 = line.split(', ')
        for i in arr1:
            i = i.strip('\n')
            arr.append(i)
        if language_x == arr[0]:
            resultats += 'Язык: %s\nЯблоко: %s\nРуки: %s\nПол: %s\nЗубы: %s\nВолосы: %s\nКомната: %s\nТело: %s\nОкно: %s\nЛицо: %s\nОдежда: %s\nПосуда: %s\n' % arr[0], arr[1], arr[2], arr[3], arr[4], \
                                                             arr[5], arr[6], arr[7], arr[8], arr[9], arr[10], arr[11]
            
    if resultats == '':
        resultats = 'Ничего не найдено'
    return render_template ('results.html', resultats=resultats)

language_x = ''

if __name__ == '__main__':
    app.run(debug=True)
