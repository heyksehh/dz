import json
import matplotlib.pyplot as plt
import urllib.request


def get_data (): # Моя программа умеет читать только 100 постов, так как с 26 апреля я в отъезде без компа и не успеваю её доделать :(
    info = [] # Массив с данными для передачи другим функциям
    postLen = [] # Данные про длину постов
    commentLen = [] # Данные про среднюю длину комментариев
    data_age = {} # Данные про возраст и среднюю длину комментариев
    data_city = {} # Данные про город и среднюю длину комментариев
    
    req = urllib.request.Request('https://api.vk.com/method/wall.get?domain=formula_1_fan&count=100')
    response = urllib.request.urlopen(req)
    result = response.read().decode('utf-8')
    data = json.loads(result)

    groupId = data["response"][1]["from_id"] 
    for i in range (1,100): # Проходимся по всем постам
        texts = data["response"][i]["text"] + '\n'
        f = open('.\\file_posts.txt', 'a', encoding='utf-8')
        f.write(texts)
        f.close()

        textPost = data["response"][i]["text"] # Собираем текст поста
        postWords = textPost.split(' ')
        words = 0
        for word in postWords:
            words += 1 # Считаем слова
        getPostId = data["response"][i]["id"]
        getComments = data["response"][i]["comments"]
        postLen.append(words-1) # Массив с кол-вом слов в постах
    
        req2 = urllib.request.Request('https://api.vk.com/method/wall.getComments?owner_id=' + str(groupId) + '&post_id=' + str(getPostId) + '&count=' + str(getComments["count"]))
        response2 = urllib.request.urlopen(req2) 
        result2 = response2.read().decode('utf-8')
        data2 = json.loads(result2) # Собираем информацию про комментарии поста
    
        c = 1
        allComments = 0 # Счётчик для обего числа слов
        while c < getComments["count"]+1: # Для каждого комментария под постом
            textComment = data2["response"][c]["text"]
            texts2 = textComment + '\n'
            
            f = open('.\\file_comments.txt', 'a', encoding='utf-8')
            f.write(texts2)
            f.close() #Скачиваем комментарий в файл
        
            userId = data2["response"][c]["from_id"] # Узнаём автора комментария
        
            req3 = urllib.request.Request('https://api.vk.com/method/users.get?user_id=' + str(userId) + '&fields=bdate') # Собираем дату рождения
            response3 = urllib.request.urlopen(req3) 
            result3 = response3.read().decode('utf-8')
            data3 = json.loads(result3)
    
            req4 = urllib.request.Request('https://api.vk.com/method/users.get?user_id=' + str(userId) + '&fields=city') # Собираем город
            response4 = urllib.request.urlopen(req4) 
            result4 = response4.read().decode('utf-8')
            data4 = json.loads(result4)
    
            commentWords = textComment.split(' ')
            words2 = 0
            for word in commentWords:
                words2 += 1 # Считаем количество слов в комментарии
            allComments += words2 # Общее число слов во всех комментариях

            getBdate0 = str([user['bdate'] for user in data3['response'] if 'bdate' in user])
            getBdate = getBdate0.strip("[]''") # Вытаскиваем дату рождения

            getCity0 = str([user['city'] for user in data4['response'] if 'city' in user])
            getCity = getCity0.strip("[]") # Вытаскиваем город

            c+=1
        
            if len(getBdate) > 6:
                DMY = getBdate.split('.')
                getAge = 2016-int(DMY[-1])
                if int(DMY[-2]) < 5:
                    getAge += 1 # Узнаём возраст пользователя
    
                if str(getAge) in data_age:
                    data_age[str(getAge)] = (int(data_age[str(getAge)]) + words2)/2 # Cловарь с данными для графика
                else:
                    data_age[str(getAge)] = words2 # Cловарь с данными для графика
            else:
                continue
            
            if getCity != '0':
                if str(getCity) in data_city:
                    data_city[str(getCity)] = (int(data_city[str(getCity)]) + words2)/2 # Cловарь с данными для графика
                else:
                    data_city[str(getCity)] = words2 # Cловарь с данными для графика
            else:
                continue
        
        if c != 1:
            averageComment = allComments/(c-1) # Средняя длина комментария
            commentLen.append(averageComment)
        else:
            commentLen.append(0)

    info.append (data_age) # Массив для передачи другим функциям
    info.append (data_city)
    info.append (commentLen)
    info.append (postLen)

    return info


def dataAge (info): # Делаем два массива для графика
    data_age = info[0]
    user_age_info = []
    userAge = []
    userCommentAge = []
    for data in data_age:
        userAge.append(int(data))
        userCommentAge.append(int(data_age[data]))
    user_age_info.append (userAge)
    user_age_info.append (userCommentAge)
    return user_age_info

    
def dataCity (info): # Делаем два массива для графика
    data_city = info[1]
    user_city_info = []
    userCity = []
    userCommentCity = []
    for data in data_city:
        userCity.append(data)
        userCommentCity.append(int(data_city[data]))
    user_city_info.append (userCity)
    user_city_info.append (userCommentCity)
    return user_city_info
        
    
def draw_1 (info): # График 1
    commentLen = info[2]
    postLen = info[3]
    plt.bar(commentLen, postLen)
    plt.title('Comment/Post Lengths relation')
    plt.xlabel('Average Comment Length')
    plt.ylabel('Post Length')
    plt.show()
   

def draw_2 (user_age_info): # График 2
    userAge = user_age_info[0]
    userCommentAge = user_age_info[1]
    plt.bar(userAge, userCommentAge)
    plt.title('Age/Comment Lengths relation')
    plt.xlabel('Age')
    plt.ylabel('Average Comment Length')
    plt.show()
    

def draw_3 (user_city_info): # График 3
    userCity = user_city_info[0]
    userCommentCity = user_city_info[1]
    plt.bar(range(len(userCity)), userCommentCity)
    plt.xticks(range(len(userCity)), userCity, rotation = 'vertical')
    plt.title('City/Comment Lengths relation')
    plt.xlabel('City')
    plt.ylabel('Average Comment Length')
    plt.show()
    

def main():
    f1 = get_data ()
    f5 = dataAge (f1)
    f6 = dataCity (f1)
    f7 = draw_1 (f1)
    f8 = draw_2 (f5)
    f9 = draw_3 (f6)
    
if __name__ == '__main__':
    main()    
