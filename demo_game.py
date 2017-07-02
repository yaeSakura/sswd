#!/usr/bin/env python
# -*- coding:utf-8 -*-
from Tkinter import *
import tkMessageBox
import random

root = Tk()
spyword = [["钢笔", "铅笔"], ["月亮", "太阳"], ["鸭脖", "鸡爪"], ["苹果", "安卓"], ["孟非", "乐嘉"]]
a = 0  # get_message使用数
b = 0  # get_ticket使用数
c = 1  # get_result的轮数
word = []  # 定义词语列表
cnt = []  # 计算玩家票数列表
live = []  # 统计玩家生还列表
sameVote = 0  # 出现相同的标志
spyWin = 0    # 卧底胜利的判定条件
spy = 0   # 存卧底
num = 0   # 获取总人数

def get_player():
    global spy, word, cnt, live, num
    # 初始化数据
    word = []
    cnt = []
    live = []
    spy = 0
    num = 0
    try:
        num = int(gamePlayers.get())
    except Exception,e:
        tkMessageBox.showinfo("人数类型错误", "请输入整数")
    if num < 3 or num > 10:
        tkMessageBox.showinfo("人数错误", "游戏人数只能为3到10人")
    else:
        # print num
        msg.insert('1.0', '游戏开始\n')
        for i in range(0, num):
            word.append('a')
            cnt.append(0)
            live.append(i + 1)
        # 卧底玩家
        spy = random.randint(0, num - 1)
        # 随机词语
        list_rand = random.choice(spyword)
        for m in range(0, num):
            if m == spy:
                word[m] = str(list_rand[1])
            else:
                word[m] = str(list_rand[0])
        print word[spy], spy+1


def get_message():
    global a, word
    if gamePlayers.get():
        try:
            msg.insert('1.0', word[a]+'--'+str(a+1)+'\n')
            a += 1
        except Exception, e:
            tkMessageBox.showinfo("提示", "请开始发言")
    else:
        tkMessageBox.showinfo("人数错误", "请先输入人数")


def hide_message():
    msg.delete('1.0', '2.0')


def get_ticket():
    global sameVote, b, cnt, live, num
    if b > len(live)-1:
        tkMessageBox.showinfo("投票结束", "请点击结果按钮")
    else:
        if int(vote.get()) in live:
            if live[b] == int(vote.get()):
                tkMessageBox.showinfo("投票错误", "不能投自己")
            else:
                vote2p = int(vote.get()) - 1
                cnt[vote2p] += 1
                sameVote = 0
                tkMessageBox.showinfo("%s号投票结束" % (str(live[b])), "请下一位投票")
                b += 1
        elif int(vote.get()) > num or int(vote.get()) < 0:
            tkMessageBox.showinfo("投票错误", "没有该玩家")
        else:
            tkMessageBox.showinfo("投票错误", "该玩家已经阵亡")


def get_result():
    global cnt, sameVote, live, spy, spyWin, c, b, a
    sameVote = 0
    b = 0  # 重置玩家投票
    for y in range(0, len(cnt)):
        if max(cnt) != 0 and cnt.count(max(cnt)) > 1:
            equalPlary = ''
            for i in range(len(cnt)):
                if cnt[i] == max(cnt):
                    equalPlary += str(i+1) + ' '
                else:
                    cnt[i] = 0
            msg.insert('3.0', '拥有相同票数的玩家为：%s\n' % (equalPlary,))
            tkMessageBox.showinfo("得票结果", "不止一位玩家得票数最高，请这些玩家重新发言")
            sameVote = 1
            break
        elif sameVote == 0 and cnt[y] == max(cnt) != 0:
            if y == spy:
                tkMessageBox.showinfo("游戏结束", "卧底得票数最多，卧底为%d号" % (y+1))
                msg.insert(END, '游戏结束，平民胜利\n')
                spyWin = 1
                # 重置数据
                cnt = []
                a = 0
                vote.delete(0, END)
            else:
                live.remove(y+1)
                cnt[y] = -1
                for x in range(len(cnt)):
                    if cnt[x] != -1:
                        cnt[x] = 0
                tkMessageBox.showinfo("游戏继续", "%d号玩家被冤死！" % (y+1))
                msg.insert(END, '第%d轮结束,剩余玩家号：%s.\n' % (c, str(live)[1: -1]))
                c += 1
            break
    if spyWin == 0 and len(live) == 2:
        msg.insert(END, '游戏结束，卧底为：%d\n' % (spy+1))
        tkMessageBox.showinfo("游戏结束", "卧底胜利！\n")
        # 重置数据
        cnt = []
        a = 0
        vote.delete(0, END)
    print cnt
    print live


root.title("谁是卧底")
root.geometry("400x400")
root.resizable(width=True, height=True)
Label(root, text="游戏人数：", bg="red", font=("Arial", 15)).pack()
frm = Frame(root)
# frm.pack()
# 输入人数文本框
var = StringVar()
gamePlayers = Entry(root, textvariable=var)
gamePlayers.pack()
# 判定人数
Button(root, text="开始游戏", command=get_player).pack()
Label(root, text="提示信息：", bg="red", font=("Arial", 15)).pack()
# 提示信息文本框
msg = Text(root, height=10)
msg.pack()
Button(root, text="查看提示", command=get_message).pack(side=LEFT)
Button(root, text="隐藏提示", command=hide_message).pack(side=RIGHT)
# 投票
Label(root, text="投票：", bg="blue", font=("Arial", 15)).pack()
var1 = StringVar()
vote = Entry(root, textvariable=var1)
vote.pack()
Button(root, text="投票", command=get_ticket).pack()
Button(root, text="结果", command=get_result).pack()
root.mainloop()


# if __name__ == "__main__":
    # style()
