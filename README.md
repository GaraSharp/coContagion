# coContagion

tiny contagion simulator

first appearance on 2020-05-16

「古今亭ジョン」 - classical (?) contagion simulation
===================================================

いい加減な「感染シミュレーション」を、python3+tkinterで作成しました。

# usage and dosage

このpython3コードは、実行時にtkinterを使用しているので、適宜調整して戴きたく。

端末から、
```
python3 coContagion.py
```
とすると動作します。

同時に端末に未感染数(Susceptions)、感染数(Infections)、隔離/回復数(Recovres)が出力されるので、リダイレクトでデータファイルを作っておくと、後でgnuplotなどでグラフに出来ます。
```
python3 coContagion.py > data.dat
```
感染数が0になると、停止します。しかし、ウィンドウは表示されたままなので、ウィンドウのcloseボタンを押すなどして、終了して下さい。


#  code description

セル・ゲームの一つとして構成されております。セルには、感染状態による状態数が振られております。

0	感染せず (suscept)
1...MAX-1 感染 (infection)
MAX -> -1	回復/隔離 (recovre)

リストによって構成されるセル空間は「密」であり、neumann近傍 (上下左右)のセルから感染します。

ゲーム進行は、

1.		ランダム移動
2.		感染フェーズ
3.		状態更新

を繰り返します。

1. ランダム移動

ランダム移動は、ランダムに選定した2つのセルを交換するという、vandalな方法を使用しております。

更に、近傍移動として、上限距離を指定した手法もありそうですが、そこまで芸の細かい事はしておりません。

発症/隔離セルは「移動しない」というのが自然ではありますが、感染の対象とはしないので、ランダム移動の対象として除外する事はしておりません (イカゲン)。

ランダム移動、すなわち、ランダムに選択した2つのセル交換を、100回実施しております。


2. 感染フェーズ

セルの状態数は、0...MAXで、0が非感染、1..MAX-1が感染、MAXが発症/隔離としております。

感染フェーズは、未感染セルのneumann近傍に感染セルがあるかを調べ、あれば「感染」とします。
この時、周囲に感染セルがあっても、確率的に感染が起こるとして、感染係数 (infectRate ; コード中では 0.15 にしております)を設定しております。

感染セルについては、状態数を+1、増加します。
状態数がMAXになった所で、そのセルは発症/隔離という扱いになります。

コード中で、MAXは5に設定しております。


3.  状態更新

セル空間、更に表示を更新すると共に、感染数、発症数の集計を行います。


#  and other things ...

+ python3+tkinterで画面表示を行っておりますが、MacOSだとメモリ食いになっている模様。何かいい方法はないものか ?
+ root.after(waitTicks, progress)　でtimer callback を使っておりますが、セル処理が大変なので、waitTicksを1 にしても、それほど早くはなりません。一方、すぐに処理が進んでしまうと、アニメーション的には面白くありません。
+　Vでもやってみたいのですが、目下、セル表示の画素数が多く出来ないので、それを突破できたら ... 。
+　初期条件と乱数の具合で、すぐに収束してしまう場合もあります。

