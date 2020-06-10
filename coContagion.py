# title : contagion.py - 古今亭ジョン・python, tkinter版
# begin : 2020-03-29 19:54:26 
# note  : cell stage表示 frameworking
#       : タイマーコールバックの例
#       : 

from tkinter import *
import math
import random

#  ウィンドウサイズ、ブロックサイズ、callback ticks
winWidth  = 1000
winHeight =  700
block     =    6
waitTicks =   20

# infection rate
# 基本再生産数は「何人に感染させられるか」というもので、
# このシミュレーションでは適用されない
# この数値は「周囲から感染させられるリスク」だった
infectRate = 0.15

#  集計用変数
suscept = 0
infect  = 0
recovre = 0

# cell 状態
# 0 ; non-infection
# 1..MAX-1 ; infectted , spreadding
# -1 ; quarantained / recovery

# 発症レート
MAX  =  5

# cell space calc
# ウィンドウサイズ、セルブロックサイズから、セル空間の大きさを設定
width  = int(winWidth / block)
height = int((winHeight - 50) / block)

# report cell space size
print("# infection Rate : ",  infectRate)
print("# cell space size : ", width, height)

#  cell space
#  リストの要素を操作するだけなので、globalで再束縛の必要はない、らしい
#  スライスで横、縦の順に添え字を扱うには、この順番で確保する
curr = [ [0 for i in range(height) ] for j in range(width) ]
next = [ [0 for i in range(height) ] for j in range(width) ]
#  画素のIDを保持している
pixi = [ [0 for i in range(height) ] for j in range(width) ]


#  neumann neighbour infectie ?
def infecti(m, n) :
  if m > 0 :  # 左端ではないバヤイ
    if curr[m-1][n] > 0 and random.random() < infectRate :
      return 1
  if m < width-1 :   # 右端ではないバヤイ
    if curr[m+1][n] > 0 and random.random() < infectRate:
      return 1
  if n > 0 :  # 上端ではないバヤイ
    if curr[m][n-1] > 0 and random.random() < infectRate:
      return 1
  if n < height-1 :   # 下端ではないバヤイ
    if curr[m][n+1] > 0 and random.random() < infectRate:
      return 1

  return 0


def progress():
    global stage # 大域変数を使用する宣言

    #  セル空間の表示
    suscept = 0
    infect  = 0
    recovre = 0

    for n in range(height) : 
      for m in range(width) :
        # case 'recovre' ; 黒で表示
        if curr[m][n] == -1 :
          recovre = recovre + 1
          canvas.itemconfigure(pixi[m][n], outline='#111', fill='#111')
        # caes 'infect' ; オレンジ色で表示
        if curr[m][n] >= 1 :
          infect = infect + 1
          canvas.itemconfigure(pixi[m][n], outline='#E60', fill='#E60')
        # caes 'suscept' ; 白で表示
        if curr[m][n] == 0 :
          suscept = suscept + 1
          canvas.itemconfigure(pixi[m][n], outline='#EEE', fill='#EEE')

    #  集計表示
    rep = "s:"+str(suscept)+", "
    rep = rep+"i:"+str(infect)+", "
    rep = rep+"r:"+str(recovre)
    #  Canvas widget上に設けたtext widgetの表示を更新
    canvas.itemconfigure(number, text=rep)

    #  世代数と要素総数の出力
    print(stage, suscept, infect, recovre)

    #  セル空間の更新

    # random walk by cell swapping
    for i in range(100) : 
      x1 = int(random.random()*width)
      y1 = int(random.random()*height)
      x2 = int(random.random()*width)
      y2 = int(random.random()*height)
      curr[x2][y2], curr[x1][y1] = curr[x1][y1], curr[x2][y2]

    #  infection part 
    for n in range(height) : 
      for m in range(width) :
        next[m][n] = curr[m][n]
        #  感染状態が上限に達したら、Quarantine / Recovre
        if curr[m][n] >= MAX  : 
          next[m][n] = -1
        #  感染していたら、感染状態の更新 (増殖)
        if curr[m][n] > 0 and curr[m][n] < MAX:
          next[m][n] = next[m][n]+1
        #  感染していない場合、周囲に「spreadre」がいれば、感染
        if curr[m][n] == 0 :
          if infecti(m, n) == 1 : 
            next[m][n] = 1

    for n in range(height) : 
      for m in range(width) :
        curr[m][n] = next[m][n] 

    stage = stage + 1

    #  100msecの時間待ちのあと、再び自分を呼び出す
    if infect > 0 : 
      root.after(waitTicks, progress)


# Main part

#  randomize
random.seed()

#  random cell placing
for i in range(1) : 
  x = int(random.random()*width)
  y = int(random.random()*height)
  curr[x][y] = 1


stage = 0
root = Tk()
canvas = Canvas(root, width=winWidth, height=winHeight)
number = canvas.create_text(200, 30, text='          ',
    font='Times 20', fill='#090')
root.title('古今亭ジョン  infect Rate='+str(infectRate))

for n in range(height) : 
  for m in range(width) :
    pixi[m][n] = canvas.create_rectangle(m*block, n*block+50, m*block+(block-1), n*block+(block-1)+50,
        width=1, outline='#EEE', fill='#EEE', tags='cells')

canvas.pack()

progress()  #  呼び出し
root.mainloop()

