from tkinter import *
import turtle    #tu
import random
suit_dict = {'0': '0.gif', '1': '1.gif', '2': '2.gif', '3': '3.gif'}
card_dict = {'2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9', '10': '10', '11': 'J',
             '12': 'Q', '13': 'K', '1': 'A'}
opr_list = ['+', '-', '*', '/']
def drawcard(card, x, y):#画牌
    tu.penup()
    tu.goto(x - 100, y)  # 坐标向左位移100
    tu.shape(card)
    tu.stamp()
def writerank(x, y, rank):#画值
    tu.penup()
    tu.goto(x - 100, y)
    tu.write(rank, font=("Arial", 30, "normal"))
def drawgame(hand_list):  # 绘制一局游戏
    for i in range(4):
        drawcard(suit_dict[hand_list[i][1]], i * 100, 0)  # 牌花色，每张牌间隔100像素
        writerank(i * 100 - 22, -25, card_dict[hand_list[i][0]])   #牌面值
def opengame():  # 游戏开场 绘制扑克牌背面
    for i in range(4):
        drawcard("back.gif", i * 100, 0)
def deal_cards():  # 随机发牌4张，每张牌是个2元组[面值，花色]
    global hand_list  # 全局变量
    answer.set("")  #分别清除输入框，和两个标签的值
    input1.set("")
    entry1.delete(0, END)
    hand_list = [[str(random.randint(1, 13)), str(random.randint(0, 3))] for i in range(4)]
    drawgame(hand_list)
    solve(hand_list)  # 先计算出24点保存起来
def combine_cards(): #计算时不关心花色，只对面值组合
    temp_list = []
    for i in range(4):
        for j in range(4):
            if i == j: continue
            for k in range(4):
                if k == j or k == i: continue
                for l in range(4):
                    if l == k or l == j or l == i: continue
                    temp_list.append([hand_list[i][0], hand_list[j][0], hand_list[k][0], hand_list[l][0]])
    return temp_list
def combine_opr():
    temp_list = []
    for opr1 in opr_list:
        for opr2 in opr_list:
            for opr3 in opr_list:
                temp_list.append([opr1, opr2, opr3])
    return temp_list
def solve(hand_list):  # 解题
    global answer_list
    answer_list = []
    cards_combination = combine_cards()
    opr_combination = combine_opr()
    for card_list in cards_combination:
        opd1, opd2, opd3, opd4 = card_list
        for opr_list in opr_combination:
            opr1, opr2, opr3 = opr_list
            expression_list = [['(', opd1, opr1, opd2, ')', opr2, '(', opd3, opr3, opd4, ')'],
                       ['(', opd1, opr1, opd2, ')', opr2, opd3, opr3, opd4],
                       ['(', opd1, opr1, opd2, opr2, opd3, ')', opr3, opd4]
                       ]  # 加括号，形成表达式
            if opr1 == '-' and int(opd1) < int(opd2):  # 去除负数运算
                expression_list.pop(0)
                expression_list.pop(1)
            for expression in expression_list:
                ex = ''.join(expression)
                try:  # 预防除数为0
                    if eval(ex) == 24 and type(eval(ex)) == int:  # 去除小数运算
                        answer_list.append(ex)
                except:
                    pass
def showanswer():
    if len(answer_list) == 0:
        answer.set("无解")
    else:
        answer.set(answer_list[0]) #只显示第一组答案
def checkanswer():
    answer2=entry1.get()+" "
    num_list = []
    num=""
#取出输入框中的数字
    for i in answer2:
        if str.isdigit(i)==False:
            num_list.append(num)
            num=""
        else:
            num+=i
    print(num_list)
    for i in num_list:
        if i=='':
            num_list.remove(i)

    sum=0#判断是否属于卡牌数字的标志
    if len(num_list)==4:
            for i in range(0, 4):
                for j in range(0,4):
                  if num_list[i]==hand_list[j][0]:
                      sum=0
                      break
                  else:
                      sum+=1
                if sum==4:
                  input1.set("请使用规定的数字")
                  break
                else:
                 if eval(entry1.get()) == 24:
                     input1.set("回答正确")
                 else:
                     input1.set("回答错误")
    else:
                  input1.set("请按规定使用数字")
    print(num_list)




hand_list = []
answer_list = []
root = Tk() #from tkinter import *
root.geometry('520x520+600+300') #位置设置
root.title('24点游戏')
root.resizable(False, False)
canvas = Canvas(root, width=620, height=400) #绘制画布
canvas.pack()
answer = StringVar()# 建立变量answer为字符串变量
theScreen = turtle.TurtleScreen(canvas)
theScreen.addshape("back.gif")
theScreen.addshape("0.gif")  # 红心
theScreen.addshape("1.gif")  # 黑桃
theScreen.addshape("2.gif")  # 梅花
theScreen.addshape("3.gif")  # 方块
tu = turtle.RawTurtle(theScreen)
theScreen.tracer(False)
opengame()
bt1 = Button(root, text=' 发牌 ', command=deal_cards)
bt1.place(x=20, y=425)
entry1 = Entry(root,bd=3)
entry1.pack(side = RIGHT)
entry1.place(x=80,y=425)
input1=StringVar()
bt2 = Button(root, text=' 检验答案 ',command=checkanswer)
bt2.place(x=240,y=425)
bt3 = Button(root, text=' 参考答案 ',command=showanswer)
bt3.place(x=340, y=425)
Label(textvariable=answer).place(x=350, y=470)
Label(textvariable=input1).place(x=240,y=470)
root.mainloop()  #tkinter的事件循环
