# coding:utf-8
# version:python 3.7
# author:Ivy

from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import time
import random
import os

root = Tk()
root.title("抽奖助手")

#####################################
##           功能设计
#####################################

def getName():
    #读取姓名文件，获得姓名列表
    if os.path.exists('name.txt'):
        with open('name.txt','r', encoding='UTF-8') as f:
            name_list=f.readlines()
        for i in range(len(name_list)):
            name_list[i]=name_list[i].replace('\n','')
        return name_list
    else:
        messagebox.showerror('错误','name.txt不存在！')
        root.destroy()

def setName():
    # 随机产生姓名
    namestr.set(random.choice(name_list))

def start():
    global running
    # 开始
    if not running:
        update()
        running=True

def stop():
    global timer,running,name_list,rewardNow,reward,rewardNames
    # 暂停
    if running:
        if rewardNow is None:
            # 初始化状态
            rewardNow=[0,0]
        elif (rewardNow[0]==len(reward)-1 and rewardNow[1]==reward[rewardNow[0]][1]-1):
            # 所有奖项都抽完了
            messagebox.showerror('感谢使用','所有奖项都抽完了！感谢您的使用！')
            root.destroy()
        elif rewardNow[1]==reward[rewardNow[0]][1]-1:
            # 当前奖项已经抽完
            rewardNow=[rewardNow[0]+1,0]
            rewardNames=''
        else:
            # 继续抽取当前奖项
            rewardNow[1]=rewardNow[1]+1

        status=(reward[rewardNow[0]][0],rewardNow[1])
        root.after_cancel(timer)
        setName()
        rewardNames+=(' '+namestr.get())
        msgstr.set('恭喜他们获得 {}\n 【{} 】 '.format(status[0],rewardNames))
        running=False
        name_list.remove(namestr.get()) # 从奖池中删除已经获奖的人

def update():
    global timer
    # 刷新显示内容
    setName()
    timer=root.after(50,update)

def initTree():
    global tree,reward
    for v in reward:
        tree.insert('','end',value=v)

def insertReward():
    # 新增奖项
    global tree,rewardName,rewardNum,reward
    v=(rewardName.get(),int(rewardNum.get()))
    tree.insert('','end',value=v)
    reward.append((rewardName.get(),int(rewardNum.get())))
    rewardName.set('')
    rewardNum.set('')

def cleanAll():
    # 清空所有奖项
    global tree,reward
    x=tree.get_children()
    for item in x:
        tree.delete(item)
    reward=[]


####################################
##         初始化
####################################

# 变量定义
msgstr=StringVar()
namestr=StringVar()
rewardName=StringVar()
rewardNum=StringVar()
running=False
reward=[('一等奖',1),('二等奖',3),('三等奖',5)]
rewardNow=None
rewardNames=''

name_list=getName()

####################################
##         界面设计
####################################

root.geometry('600x300')

nb = ttk.Notebook(root) # 创建tab的notebook

##### 主程序页
tab1 = ttk.Frame(nb)
nb.add(tab1, text='主程序')

# 定义标签栏
l1 = Label(tab1, textvariable=msgstr, font=("Arial, 20")).pack(side=TOP,pady=20)
l2 = Label(tab1, textvariable=namestr, font=("Arial, 35")).pack(side=TOP,pady=10)
setName()
msgstr.set("准备开始抽奖！")

# 定义按钮
frame_a=ttk.Frame(tab1)
b1=Button(frame_a, text='start', command=start, width=7, height=2,font=("Arial","14")).pack(side=LEFT)
b2=Button(frame_a, text='stop', command=stop, width=7, height=2,font=("Arial","14")).pack(side=RIGHT)
frame_a.pack(anchor=CENTER)

##### 初始化页
tab2 = ttk.Frame(nb)
nb.add(tab2, text='初始化')

# 定义输入框
frame1=ttk.Frame(tab2)
frame2=ttk.Frame(frame1)
frame_b=ttk.Frame(frame2)
l3 = Label(frame_b, text='奖项名',font=("Arial","14")).pack(side=LEFT)
en1 = Entry(frame_b, textvariable=rewardName).pack(side=LEFT)
frame_b.pack(side=TOP,anchor=CENTER)
frame_c=ttk.Frame(frame2)
l4 = Label(frame_c, text='获奖人数',font=("Arial","14")).pack(side=LEFT)
en2 = Entry(frame_c, textvariable=rewardNum).pack(side=LEFT)
frame_c.pack(side=TOP,anchor=CENTER)
frame2.pack(side=LEFT)

# 定义按钮
frame3=ttk.Frame(frame1)
b3=Button(frame3, text='新增奖项', command=insertReward, width=10,height=1).pack(side=TOP,anchor=CENTER)
b4=Button(frame3, text='清空所有奖项', command=cleanAll, width=10,height=1).pack(side=TOP,anchor=CENTER)
frame3.pack(side=RIGHT)
frame1.pack(side=TOP)

# 表格
tree = ttk.Treeview(tab2, columns=('奖项','获奖人数'),show='headings')
tree.column('奖项',width=300,anchor='center')
tree.column('获奖人数',width=300,anchor='center')
tree.heading('奖项',text='奖项')
tree.heading('获奖人数',text='获奖人数')
tree.pack(side=TOP, expand=1,pady=10)
initTree()

#### 软件说明页
tab3 = ttk.Frame(nb)
nb.add(tab3, text='软件说明')
l5=Label(tab3, anchor='nw', justify = 'left',wraplength = 600,font=("Times New Roman", "14"),
text='''作者: Ivy Wong
版本：v1.0

使用方法:
1、在name.txt中设置好抽奖名单，每行一个人名，如有重名，请自带标识符号或说明；
2、在软件中的初始化页面进行奖项初始化；
3、在主程序页面中开始运行即可！
''').pack(side=TOP,expand=1)


nb.pack(anchor=NW,expand=1, fill="both")

####################################
##         运行程序
####################################

root.mainloop()
