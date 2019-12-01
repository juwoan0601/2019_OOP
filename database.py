##json 데이터 활용 방법##
#foodlist는 데이터베이스에 있는 데이터를 json형식으로 바꾸고 리스트로 만들어 반환하는 함수이다.
#json 데이터는 name : ooo 등 key-value형식으로 이루어져 있다. 

#어떤 데이터의 name을 알고 싶다면 (리스트변수)['name']을 치면 알 수 있다. 예를 들어 foodlist의 모든 name을 출력하고 싶다면
#ㅣ=foodlist(collection)
#for i in l:
#   print(i['name'])
#   print('\m') 이런 코드를 작성하면 된다.

#하나의 데이터는 다음과 같이 구성된다.
#_id : 데이터베이스가 부여하는 고유한 id
# name: 음식 이름(string)
# unchange: 맛,  주재료 등 음식 고유의 property를 barcode로 나타낸 것(string형식, int로는 표현 안됨)
# change: 시간, 날씨 등의 데이터가 들어가는 곳 기본값은 0/0/0/0/0/0/0/0/0/0/0/0/0/0/(string)
# restaurant: 대표음식점, 기본값은 111, 추가조사 완료 되면 바꾸기, 서버에서 바로 바꾸는게 빨라서 따로 함수를 만들지 않음 

#mongodb를 활용함
from pymongo import MongoClient
from bson import json_util
import json

#DB에 접근, client는 read, write의 권한을 가지고 있음
client = MongoClient("mongodb://program:1234@oop3rd-shard-00-00-wiwvp.mongodb.net:27017,oop3rd-shard-00-01-wiwvp.mongodb.net:27017,oop3rd-shard-00-02-wiwvp.mongodb.net:27017/test?ssl=true&replicaSet=OOP3rd-shard-0&authSource=admin&retryWrites=true&w=majority")
db=client.OOP #클러스터에 접근
collection=db.OOP #collection(데이터의 묶음)에 접근

#음식의 list를 만들어 반환하는 함수, json형식으로 데이터에 접근 할 수 있음
def FoodList(collection):
    s=collection.find()
    l = list(s)
    return l

#새로운 음식 data를 삽입하는 함수
def InsertFood(collection, name, unchange, change='0/0/0/0/0/0/0/0/0/0/0/0/0/0/', restaurant = '111'):
    #만약 같은 이름의 음식이 있다면 음식을 추가하지 않는다.
    l=FoodList(collection)
    for i in l:
        if(name == i['name']):
            print('This is existing food...')
            return 0
    post = {'name': name , 'unchange' : unchange, 'change' : change, 'restaurant' : restaurant }
    collection.insert_one(post)
    return 0

#음식 data를 삭제하는 함수
def DeleteFood(collection, name):
    l=FoodList(collection)
    k=0
    for i in l:
        if(name == i['name']):
            collection.delete_one({'name': name})
            print(name, 'was', 'Deleted')
            k=k+1
            return 0
    if(k == 0):
        print('There is no such food...')
        return 0 


#change 데이터를 update하는 함수, newv는 새로운 binary vector이다.
def UpdateChange(collection, name, newv):
    if((CheckFood(collection, name))==False): #데이터베이스에 없는 이름이면
        print("There is no such food...")
        return -1
    a=collection.find_one({'name':name})
    #newv를 string으로 바꾸자
    length=len(newv)
    newstring = ""
    for p in range(0, length):
        newstring = newstring + str(newv[p]) +'/'
    collection.update_one({'name':name}, {'$set':{'change':newstring}})
    return 0


#string을 binary vector로 바꾸는 함수, data는 바꾸자 하는 것(change/unchange)
def ReturnBin(collection, name, data):
    if((CheckFood(collection, name))==False): #데이터베이스에 없는 이름이면
        print("There is no such food...")
        return -1
    a=collection.find_one({'name':name})

    if(data == 'change'):
        intstring = a['change']
        BitNum = len(intstring)
        bin =[]
        temp =''
        for p in range(0, BitNum):
            if(intstring[p] != '/'):
                temp = temp + intstring[p]
            else:
                bin.append(int(temp))
                temp = ''
        return bin

    elif(data == 'unchange'):
        intstring = a['unchange']
        BitNum = len(intstring)
        bin =[]
        for p in range(0, BitNum):
            if(intstring[p] == '1'):
                bin.append(1)
            else:
                bin.append(0)
        return bin
 

#음식이 있는지 확인하는 함수
def CheckFood(collection, name):
    l=FoodList(collection)
    k=0
    for i in l:
        if(name == i['name']):
            k=k+1
            return True
    if(k==0):
        return False