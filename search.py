
### 検索ツールサンプル
### これをベースに課題の内容を追記してください

# 検索ソース
# ファイルパス
path = 'C:\My Achievement\source.csv'

# リスト内容
w = 'ねずこ\nたんじろう\nきょうじゅろう\nぎゆう\nげんや\nかなお\nぜんいつ'

# リスト書込
with open(path,mode='w') as f:
    f.write(w)

# リスト読込
with open(path) as f:
    source = [s.strip() for s in f.readlines()]

### 検索ツール
def search():
    word =input("鬼滅の登場人物の名前を入力してください >>> ")
    
    ### ここに検索ロジックを書く
    if word in source:
        print("{}が見つかりました".format(word))
    else:
        print('{}が見つかりませんでした'.format(word))
        source.append(word)

if __name__ == "__main__":
    search()
