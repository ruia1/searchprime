# -*- coding: utf-8 -*-
from random import randint
from math import sqrt

def m(n):
    if type(n) != int or n < 2: return False
    if n == 2: return True
    if n & 1 == 0: return False
    if n < 5000:#5000以下は誤作動防止のため総割り
        for i in range(3,int(sqrt(n))+1,2):
            if n%i == 0: return False
        return True
    d = (n - 1) >> 1
    while d & 1 == 0:
        d >>= 1
    for i in range(100):
        a = randint(1,n-1)
        t = d
        y = pow(a, t, n)
        while t !=n - 1 and y != 1 and y != n -1:
            y = (y * y) % n
            t <<= 1
        if y != n - 1 and t & 1 == 0: return False
    return True

def add(n):#1足す
    try:
        nl = n[-1]
    except IndexError:
        return "1"#'K'を'11'に繰り上げる
    if nl == "K":
        return add(n[0:-1])+"1"
    elif nl in ["1","2","3","4","5","6","7","8"]:
        return n[0:-1]+str(int(nl)+1)
    elif nl == "9":
        return n[0:-1]+"T"
    elif nl == "T":
        return n[0:-1]+"J"
    elif nl == "J":
        return n[0:-1]+"Q"
    else:
        return n[0:-1]+"K"
    
def odd(n):#偶数なら1足す
    nl = n[-1]
    if nl in ["2","4","6","8"]:
        return n[0:-1]+str(int(nl)+1)
    elif nl == "T":
        return n[0:-1]+"J"
    elif nl == "Q":
        return n[0:-1]+"K"
    elif nl == "5":
        return n[0:-1]+"7"
    return n

def dic(n):
    try:
        nl = n[-1]
    except IndexError:
        return ""
    if nl == "1":
        return dic(n[0:-1])+"K"
    elif nl in ["2","3","4","5","6","7","8","9"]:
        return n[0:-1]+str(int(nl)-1)
    elif nl == "T":
        return n[0:-1]+"9"
    elif nl == "J":
        return n[0:-1]+"T"
    elif nl == "Q":
        return n[0:-1]+"J"
    else:
        return n[0:-1]+"Q"
    
def substitutes(st):#数字→絵札
    st = st.replace("10","T")
    st = st.replace("12","Q")
    st = st.replace("13","K")
    st = st.replace("11","J")
    return st

def unsubstitutes(st):#絵札→数字
    st = st.replace("T","10")
    st = st.replace("Q","12")
    st = st.replace("K","13")
    st = st.replace("J","11")
    return st

def checkp(n,judlenme,qkp,lenmin,lenmax,pereven,secard,al):#条件に合っているか探索　合っているならFalse
    if judlenme:#枚数でカウント
        nn = unsubstitutes(n)
        ni = int(nn)
        if "0" in n:
            print(n,0)
            return "E"
        nlen = len(n)
        if lenmax != 0 and nlen > lenmax:return "s"
        if lenmin != 0 and nlen < lenmin:return "l"
        if not m(ni):return True
        if secard != "0":
            if secard not in n:return True
    else:#桁数でカウント
        ni = n
        nn = str(n)
        n = nn
        nlen = len(nn)
        if lenmax != 0 and lenmax < nlen:return "s"
        if lenmin != 0 and nlen < lenmin:return "l"
        if not m(ni):return True
        if secard != "0":
            if unsubstitutes(secard) not in nn:return True
        if qkp:
            if "0" in substitutes(n):return True
    if pereven != 0:#偶数消費割合について判定
        npereven = 0
        if nlen > 1:
            for i in n[0:-1]:
                if i in ["2","4","5","6","8","T","Q"]:
                    npereven += 1
            if 100*npereven <= (nlen-1)*pereven:return True
        else:
            if nn not in ["2","5"] and not npereven:return True
    if al:#詳細設定が設定されてるなら
        if 3 in al:#レピュニット素数
            for i in nn:
                if i != "1":return True
        if 4 in al:#安全素数
            if not m(ni>>1):return True
        if 5 in al:#ソフィー・ジェルマン素数
            if not m(2*ni+1):return True
        nl = int(nn[-1])
        al6 = 6 in al
        if al6:#四つ子素数
            if ni in [5,7]:
                pass
            elif nl == 1:
                if not(m(ni+2) and m(ni+6) and m(ni+8)):return True
            elif nl == 3:
                if not(m(ni-2) and m(ni+4) and m(ni+6)):return True
            elif nl == 7:
                if not(m(ni-6) and m(ni-4) and m(ni+2)):return True
            else:
                if not(m(ni-8) and m(ni-6) and m(ni-2)):return True
        or8,or9,or10,n3 = False,False,False,bool(ni%3-1)#n3:niの3の剰余(1:False,2:True)
        if 7 in al:#三つ子素数
            if ni in [3,5] or al6:
                pass
            elif ni == 2:
                return True
            elif n3:#３の剰余が２で
                if nl == 3:#末尾が３の時、n-6,n-4型しかあり得ない
                    if not (m(ni-6) and m(ni-4)):return True
                elif nl == 9:#上に同じ
                    if not (m(ni+2) and m(ni+6)):return True
                else:#末尾が1か7なら
                    mm4,m2 = m(ni-4),m(ni+2)
                    if not mm4 and not m2:return True#n-4,n+2どちらも素数でなければ三つ子でない
                    if mm4 and m2:#どちらも素数なら三つ子
                        pass
                    elif mm4:#n-4が素数なら、n-6を判定
                        if not m(ni-6):return True
                    else:#n+2が素数なら、n+2を判定
                        if not m(ni+6):return True
            else:#３の剰余が１で～（上に同じ）
                if nl == 1:
                    if not (m(ni-6) and m(ni-2)):return True
                elif nl == 7:
                    if not (m(ni+4) and m(ni+6)):return True
                else:
                    mm2,m4 = m(ni-2),m(ni+4)
                    if not mm2 and not m4:return True
                    if mm2 and m4:
                        pass
                    elif mm2:
                        if not m(ni-6):return True
                    else:
                        if not m(ni+6):return True
        if 11 in al:#JK四つ子　~1,~7,~11,~13
            if ni < 10:return True
            elif nl == 1:
                if not(m(ni+6) and m(10*ni+1) and m(10*ni+3)) or not(nn[-2]=="1" and m(ni+2) and m(ni//10) and m(ni//10+6)):return True
            elif nl == 3:
                if not(nn[-2]=="1" and m(ni-2) and m(ni//10) and m(ni//10+2)):return True
            elif nl == 7:
                if not(m(ni-6) and m(10*ni-59) and m(10*ni-57)):return True
            else:
                return True
        if 8 in al:#双子素数
            if al6 or or8 or ni in [2,3] or 11 in al:#四つ子or三つ子or2or3orJK四つ子なら双子
                pass
            elif n3:
                if not m(ni+2):return True
            elif not m(ni-2):return True
        if 9 in al:#いとこ素数
            if al6 or or9:
                pass
            elif n3:
                if not m(ni-4):return True
            elif not m(ni+4):return True
        if 10 in al:#セクシー素数
            if al6 or or10 or 11 in al:
                pass
            elif not(m(ni-6) and m(ni+6)):return True
    return False

def sehome():
    while True:
        con = False
        print("素数探索モードです。探索する素数の条件を設定してください。\n"+
              "探索する数、大きさ、表示順、素数大富豪素数、偶数消費、\n"
              "特定のカードを含むか、詳細設定を設定します。\n"+
              "endを入力することでいつでも終了できます。\n"
              "redoを入力することでいつでも入力をし直す事ができます。\n")
        while True:
            print("探索する素数の数を入力してください。")
            many = input()
            if many == "end":
                print("終了します")
                if '__main__'==__name__:input("終了するにはエンターを押してください...")
                return
            elif many == "redo":
                con = True
                break
            try:many=int(many)
            except ValueError:
                print("正しい値を入力してください。")
                continue
            if many < 1:
                print("正しい値を入力してください。")
                continue
            break
        if con:continue
        print("\n大きさの条件を設定します。判定する方法を選択してください。桁数:0 枚数:1")
        judlenme = input()
        if judlenme == "end":
            print("終了します。")
            if '__main__'==__name__:input("終了するにはエンターを押してください...")
            return
        elif judlenme == "redo":
            con = True
            continue
        try:judlenme=int(judlenme)
        except ValueError:judlenme=1
        while True:
            print("探索する桁数(枚数)の最小値を入力してください。指定しない場合、0を入力してください。")
            lenmin = input()
            if lenmin == "end":
                print("終了します。")
                if '__main__'==__name__:input("終了するにはエンターを押してください...")
                return
            elif lenmin == "redo":
                con = True
                break
            try:lenmin=int(lenmin)
            except ValueError:
                print("正しい値を入力してください。")
                continue
            break
        if con:continue
        while True:
            print("探索する桁数(枚数)の最大値を入力してください。指定しない場合、0を入力してください。")
            lenmax = input()
            if lenmax == "end":
                print("終了します。")
                if '__main__'==__name__:input("終了するにはエンターを押してください...")
                return
            elif lenmax == "redo":
                con = True
                break
            try:lenmax=int(lenmax)
            except ValueError:
                print("正しい値を入力してください。")
                continue
            if (lenmin > lenmax and lenmax != 0) and lenmax >= 0:
                print("正しい値を入力してください。")
                continue
            break
        if con:continue
        if lenmax == 0:
            sortme = 1
        else:
            while True:
                print("昇順か降順、どちらで探索しますか。1:昇順 0:降順")
                sortme = input()
                if sortme == "end":
                    if '__main__'==__name__:input("終了するにはエンターを押してください...")
                    return
                elif sortme == "redo":
                    con = True
                    break
                try:sortme=int(bool(int(sortme)))
                except ValueError:
                    print("正しい値を入力してください。")
                    continue
                break
            if con:continue
        if judlenme:
            qkp = 1
        else:
            print("素数大富豪素数を探索しますか。はい：1 いいえ：0 を入力してください。")
            qkp=input()
            if qkp == "end":
                print("終了します。")
                if '__main__'==__name__:
                    input("終了するにはエンターを押してください...")
                    return
            elif qkp == "redo":
                con = True
                continue
            try:qkp=int(qkp)
            except ValueError:qkp=1
        while True:
            print("偶数の最低消費割合をパーセンテージで入力してください。%は入力不要です。\n"+
                  "偶数消費割合は、下一桁を除いて計算されます。\n"+
                  "指定しない場合は0を入力してください。")
            pereven = input()
            if pereven == "end":
                print("終了します。")
                if '__main__'==__name__:input("終了するにはエンターを押してください...")
                return
            elif pereven == "redo":
                con = True
                break
            try:pereven=int(pereven)
            except ValueError:
                print("正しい値を入力してください。")
                continue
            if pereven > 100 or pereven < 0:
                print("0以上100以下で入力してください。")
                continue
            break
        if con:continue
        while True:
            print("特定のカードを含むことを条件に設定します。指定するカードを選択してください。\n"+
                  "絵札はTJQKで、指定しない場合は0を入力してください。")
            secard = input()
            if secard == "end":
                print("終了します。")
                if '__main__'==__name__:input("終了するにはエンターを押してください...")
                return
            elif secard == "redo":
                con = True
                break
            if secard not in ["A","1","2","3","4","5","6","7","8","9","T","J","Q","K","0"]:
                print("正しい値を入力してください。")
                continue
            break
        while True:
            print("詳細設定をしますか。はい：1 いいえ:0")
            advanceset = input()
            if advanceset == "end":
                print("終了します。")
                if '__main__'==__name__:input("終了するにはエンターを押してください...")
                return
            elif advanceset == "redo":
                con = True
                break
            elif advanceset in ["1","１"]:advanceset = 1
            elif advanceset in ["0","０"]:advanceset = 0
            else:
                print("正しい値を入力してください。")
                continue
            break
        if con:continue
        al = []
        fname = False
        if advanceset:
            while True:
                print("詳細設定をします。変更する設定の番号を入力してください。\n"+
                      "デフォルトは無効になっています。\n"+
                      "双子素数の要素など、他の選択肢に包含される選択肢は、\n"+
                      "それを包含するものを選択している場合には選択する必要はありません。\n"+
                      "設定を終了する場合、0を入力してください。\n"+
                      "1 :メルセンヌ素数 2 :フェルマー素数 3 :レピュニット素数 4 :安全素数\n"+
                      "5 :ソフィージェルマン素数 6 :四つ子素数の要素 7 :三つ子素数の要素\n"+
                      "8 :双子素数の要素 9 :いとこ素数の要素 10:セクシー素数の要素\n"+
                      "11:JK四つ子素数の要素")
                ads = input()
                print()
                if ads == "end":
                    print("終了します。")
                    if '__main__'==__name__:input("終了するにはエンターを押してください...")
                    return
                elif ads == "redo":
                    con = True
                    break
                try:ads = int(ads)
                except ValueError:
                    print("正しい値を入力してください。")
                    continue
                if ads > 13 or ads < 1:print("正しい値を入力してください。")
                else:
                    if ads in al:
                        print(str(ads)+"は設定されています。解除しますか。はい：1 いいえ：0")
                        if input() in ["1","１"]:al.remove(ads)
                    else:
                        if ads == 0:break
                        if ads in [1,2,3,6,11]:
                            if judlenme:
                                print("1,2,3,6,11は、大きさの判別に枚数を指定する事はできません。\n"+
                                      "設定を桁数に変更の上、",end="")
                        print(str(ads)+"を設定します。よろしいですか。はい：1 いいえ：0")
                        if input() in ["1","１"]:
                            al.append(ads)
                            al.sort()
                    print("\n現在有効になっている設定は",end = "")
                    if al:
                        print("、")
                        for i in al:
                            print(i,end=" ")
                        print("です。")
                    else:
                        print("ありません。")
                    print("続けて設定しますか。はい：1 いいえ：0")
                    if input() in ["0","０"]:break
            if con:continue
            while True:
                print("保存用のファイルに書き込みますか。はい：1 いいえ：0")
                fname = input()
                print()
                if fname == "end":
                    print("終了します。")
                    if '__main__'==__name__:input("終了するにはエンターを押してください...")
                    return
                elif fname == "redo":
                    con = True
                    break
                try:fname=int(fname)
                except ValueError:
                    print("正しい値を入力してください。")
                    continue
                if fname == 1:
                    while True:
                        print("ファイル名を、.txtをつけずに入力してください。")
                        fname = input()+".txt"
                        print("\n"+fname+"に書き込みます。よろしいですか。はい：1 いいえ：0 書き込まない:-1")
                        inp = input()
                        try:inp = int(inp)
                        except:
                            print("正しい値を入力してください。")
                            continue
                        if inp == 1:break
                        if inp == -1:
                            fname = False
                            break
                else:fname = False
                if fname:
                    print(fname+"に書き込みます。")
                    f = open(fname,"w")
                break
            if con:continue
        print("探索を開始します。")
        count = 0
        al1,al2,al3,al6,al11= 1 in al,2 in al,3 in al,6 in al,11 in al
        if (al1 and al2) or (al3 and (al1 or al2)) or (al6 and al11):
            print(str(many)+"個は見つかりませんでした。続けますか。はい：1 いいえ：0")
        elif al3 and al6:
            if not checkp(11,False,qkp,lenmin,lenmax,pereven,secard,al):
                if fname:f.write("11\n")
                print(11)
                if count == 1:
                    print("続けますか。はい：1 いいえ：0")
                else:
                    print(str(many)+"個は見つかりませんでした。続けますか。はい：1 いいえ：0")
        elif al1:#メルセンヌ素数探索
            al = al.remove(1)
            if sortme and not checkp(3,0,qkp,lenmin,lenmax,pereven,secard,al):
                print(3)
                if fname:f.write("3\n")
                count += 1
            if sortme:n = 3
            else:
                n = int(3.322*lenmax)+1
                if not n&1:n += 1#奇数にする
            while True:
                if m(n):
                    nn = 2**n-1
                    cp = checkp(nn,0,qkp,lenmin,lenmax,pereven,secard,al)
                    if not cp:
                        if fname:f.write(str(nn)+"\n")
                        print(nn)
                        count += 1
                        if count >= many:
                            print("続けますか。はい：1 いいえ：0")
                            break
                    elif (sortme and cp == "s") or (not sortme and cp == "l"):
                        print(str(many)+"個は見つかりませんでした。続けますか。はい：1 いいえ：0")
                        break
                if sortme:n += 2
                else:n -= 2
            if not sortme and not checkp(3,0,qkp,lenmin,lenmax,pereven,secard,al):
                print(3)
                if fname:f.write("3\n")
                count += 1
        elif al2:
            for n in range(int(not sortme)*6,sortme*6,sortme*2-1):
                nn = 2**(2**n)+1
                cp = checkp(nn,0,qkp,lenmin,lenmax,pereven,secard,al)
                if not cp:
                    if fname:f.write(str(nn)+"\n")
                    print(nn)
                    count += 1
                    if count >= many:
                        print("続けますか。はい：1 いいえ：0")
                        break
                elif (sortme and (cp == "s" or n == 5)) or (not sortme and (cp == "l" or n == 0)):
                    print(str(many)+"個は見つかりませんでした。続けますか。はい：1 いいえ：0")
                    break
        elif al3:
            al = al.remove(3)
            for n in [3,2,19,23,317,3][int(not sortme)*5:sortme*5+1:sortme*2-1]:
                if n == 3:
                    print(str(many)+"個は見つかりませんでした。続けますか。はい：1 いいえ：0")
                    break
                nn = (10**n-1)//9
                cp = checkp(nn,0,0,lenmin,lenmax,pereven,secard,al)
                if not cp:
                    if fname:f.write(str(nn)+"\n")
                    print(nn)
                    count += 1
                    if count >= many:
                        print("続けますか。はい：1 いいえ：0")
                        break
                elif (sortme and cp == "s") or (not sortme and cp == "l"):
                    print(str(many)+"個は見つかりませんでした。続けますか。はい：1 いいえ：0")
                    break
                n += 1
        elif al6:
            t = False
            if sortme:
                for i in [5,7]:
                    cp = checkp(i,0,qkp,lenmin,lenmax,pereven,secard,al)
                    if not cp:
                        if fname:f.write(str(i)+"\n")
                        print(i)
                        count += 1
                        if count >= many:
                            print("続けますか。はい：1 いいえ：0")
                            t = True
                            break
                    elif cp == "s":
                        print(str(many)+"個は見つかりませんでした。続けますか。はい：1 いいえ：0")
                        t = True
                        break
                    if t:break
                if lenmin > 1:
                    n = 1+10**(lenmin-1)
                else:
                    n = 11
            else:
                10**(lenmax-1)-29
            while True:
                for nn in [n,n+2,n+6,n+8][::sortme*2-1]:
                    cp = checkp(nn,0,qkp,lenmin,lenmax,pereven,secard,al)
                    if not cp:
                        if fname:f.write(str(nn)+"\n")
                        print(nn)
                        count += 1
                        if count >= many:
                            print("続けますか。はい：1 いいえ：0")
                            t = True
                            break
                    elif (sortme and cp == "s") or (not sortme and cp == "l"):
                        print(str(many)+"個は見つかりませんでした。続けますか。はい：1 いいえ：0")
                        t = True
                        break
                if t:break
                if sortme:n += 30
                else:n -= 30
            if not sortme and not cp == "l":
                for i in [7,5]:
                    cp = checkp(i,0,qkp,lenmin,lenmax,pereven,secard,al)
                    if not cp:
                        if fname:f.write(str(i)+"\n")
                        print(i)
                        count += 1
                        if count >= many:
                            print("続けますか。はい：1 いいえ：0")
                            t = True
                            break
                    elif cp == "l":
                        print(str(many)+"個は見つかりませんでした。続けますか。はい：1 いいえ：0")
                        t = True
                        break
                    if t:break
        elif al11:
            if sortme:
                if lenmin > 1:n = 10**(lenmin-1)+21
                else:n = 31
            else:
                if lenmax == 1:1
                10**(lenmax-1)-9
            t = False
            while True:
                for nn in [n,n+6,10*n+1,10*n+3][::sortme*2-1]:
                    cp = checkp(nn,0,qkp,lenmin,lenmax,pereven,secard,al)
                    if not cp:
                        if fname:f.write(str(nn)+"\n")
                        print(nn)
                        count += 1
                        if count >= many:
                            print("続けますか。はい：1 いいえ：0")
                            t = True
                            break
                    elif (sortme and cp == "s") or (not sortme and cp == "l"):
                        print(str(many)+"個は見つかりませんでした。続けますか。はい：1 いいえ：0")
                        t = True
                        break
                if t or n == 1:break
                if sortme:n += 30
                else:n -= 30
        else:
            if judlenme:
                if sortme:
                    if lenmin > 0:
                        n = ""
                        for i in range(lenmin):
                            n += "1"
                    else:
                        n = "2"
                else:
                    n = ""
                    for i in range(lenmax):
                        n += "K"
                ns = []
                while True:
                    if unsubstitutes(n) not in ns:
                        cp = checkp(n,1,0,lenmin,lenmax,pereven,secard,al)
                        if not cp:
                            if fname:f.write(n+"\n")
                            print(n)
                            ns.append(unsubstitutes(n))
                            count += 1
                            if count >= many:
                                print("続けますか。はい：1 いいえ：0")
                                break
                        elif (sortme and cp == "s") or (not sortme and cp == "l"):
                            print(str(many)+"個は見つかりませんでした。続けますか。はい：1 いいえ：0")
                            break
                    if sortme:n = odd(add(n))
                    else:
                        if n == "2":
                            print(str(many)+"個は見つかりませんでした。続けますか。はい：1 いいえ：0")
                            break
                        elif n == "3":n = "2"
                        else:n = dic(dic(n))
            else:
                if sortme:
                    if not checkp(2,0,qkp,lenmin,lenmax,pereven,secard,al):
                        if fname:f.write("2\n")
                        print(2)
                        count += 1
                        if many == 1:
                            print("続けますか。はい:1 いいえ:0")
                            break
                    if lenmin != 0:
                        n = 10**(lenmin-1)+1
                    else:
                        n = 3
                else:
                    n = 10**(lenmax)-3
                while True:
                    cp = checkp(n,0,qkp,lenmin,lenmax,pereven,secard,al)
                    if not cp:
                        if fname:f.write(str(cp)+"\n")
                        print(n)
                        count += 1
                        if count >= many:
                            print("続けますか。はい:1 いいえ:0")
                            break
                    elif (sortme and cp == "s") or (not sortme and cp == "l"):
                        print(str(many)+"個は見つかりませんでした。続けますか。はい:1 いいえ:0")
                        break
                    if sortme:n += 2
                    else:n -= 2
                    if n == 1:break
                if not sortme and cp != "l" and count < many:
                    if not checkp(2,0,qkp,lenmin,lenmax,pereven,secard,al):
                        if fname:f.write("2\n")
                        print(2)
                        count += 1
                        if count >= many:
                            print("続けますか。はい:1 いいえ:0")
                    print(str(many)+"個は見つかりませんでした。続けますか。はい:1 いいえ:0")
        if fname:f.close()
        if input() in ["0","０"]:
            print("終了します。")
            if '__main__'==__name__:input("終了するにはエンターを押してください...")
            return
if __name__ == '__main__':
    sehome()