import random
import hashlib
from datetime import date, datetime

appraiseOverall = [
    "(은)는 전체적으로 경이롭고 예술적이야.\n",
    "(은)는 전체적으로 시선을 끄는 뭔가가 있어.\n",
    "(은)는 전체적으로 보통이상이야.\n",
    "(은)는 전체적으로 좀처럼 활약이 어려워 보인다.\n"
]

appraiseBestAttribute = [
    "두드러진 점은 공격의 키. ",
    "두드러진 점은 방어의 키. ",
    "두드러진 점은 HP의 키. ",
]

# 안 나오기도 한다.
appraiseBestAttr2nd = [
    "그리고 공격도 뒤처지지 않아. ",
    "그리고 방어도 뒤처지지 않아. ",
    "그리고 HP도 뒤처지지 않아. ",
    ""
]

appraiseAttrStat = [
    "이 점을 보면 측정할 수 없을 정도로 높아! 최고야!\n",
    "이 점을 보면 훌륭해. 놀라워.\n",
    "이 점을 보면 꽤 강하다고 말할 수 있군.\n",
    "이 점을 보면 그럭저럭이라고 할 수 있군.\n"
]

# 안 나오기도 한다.
appraiseSize = [
    "(은)는 평균보다 작아.\n",
    "(은)는 평균보다 크다.\n"
]

def getAppraiseIndex(num):
    bestAttr = num % 3
    bestAttr2nd = (num + bestAttr + 1) % 4

    if num % 13 < 7:
        isAppraiseSize = 2
    else:
        isAppraiseSize = num % 2

    grade = num % 10
    if grade == 9:
        overall = 0
    else: 
        overall = int(grade/3) + 1

    spread = num % 7
    if spread < 2 and overall != 0:
        attrStat = overall - 1
    elif spread >= 5 and overall != 3:
        attrStat = overall + 1
    else:
        attrStat = overall

    return (overall, bestAttr, bestAttr2nd, attrStat, isAppraiseSize)


def randAppraise(msg):
    target = msg.msg[len("!분석 "):]
    hash = hashlib.md5()
    hash.update(target.encode())
    hash.update(msg.nick.encode())
    hash.update(datetime.now().strftime("%Y%m%d").encode())
    num = int(hash.hexdigest(), 16)

    (overall, bestAttr, bestAttr2nd, attrStat, size) \
        = getAppraiseIndex(num)

    result = msg.nick + ", 너의 " + target +"(을)를 분석해주자.\n"
    result = result + "너의 " + target + appraiseOverall[overall] \
        + appraiseBestAttribute[bestAttr] \
        + appraiseBestAttr2nd[bestAttr2nd] \
        + appraiseAttrStat[attrStat]
    
    if size != 2:
        result = result + "너의 " + target + appraiseSize[size]

    result = result + '\n' + "이걸로 내 분석은 끝이야."
    return result

def randOPMsg(msg):
    list = ["고맙군."]
    return random.choice(list)

def randDEOPMsg(msg):
    list = ["어쩔 수 없지.", "운명을 받아들이게."]
    return random.choice(list)

def randCuriousMsg(msg):
    list = ["..."]
    return random.choice(list)
    
