import os
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver import Firefox
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
import time
import datetime
import pandas as pd

csv_pass = "./total_list_{search_keyword}_{dt_now}.csv"
log_pass = "./log/log_{dt_now}.csv"

# Chromeを起動する関数
def set_driver(driver_path, headless_flg):
    if "chrome" in driver_path:
          options = ChromeOptions()
    else:
      options = Options()

    # ヘッドレスモード（画面非表示モード）をの設定
    if headless_flg == True:
        options.add_argument('--headless')

    # 起動オプションの設定
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
    # options.add_argument('log-level=3')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--incognito')          # シークレットモードの設定を付与

    # ChromeのWebDriverオブジェクトを作成する。
    if "chrome" in driver_path:
        return Chrome(executable_path=os.getcwd() + "/" + driver_path,options=options)
    else:
        return Firefox(executable_path=os.getcwd()  + "/" + driver_path,options=options)
    
#log処理
def log(txt):
    with open(log_pass,"a") as f:
        f.write(txt + "\n")

# main処理

def main():
    search_keyword = input("検索するワードを入力してください")
    # driverを起動
    if os.name == 'nt': #Windows
        driver = set_driver("chromedriver.exe", False)
    elif os.name == 'posix': #Mac
        driver = set_driver("chromedriver", False)
    # Webサイトを開く
    driver.get("https://tenshoku.mynavi.jp/")
    time.sleep(5)
    try:
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
        time.sleep(5)
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
    except:
        pass
    # 検索窓に入力
    driver.find_element_by_class_name(
        "topSearch__text").send_keys(search_keyword)
    # 検索ボタンクリック
    driver.find_element_by_class_name("topSearch__button").click()
    time.sleep(3)
    driver.execute_script('document.querySelector(".karte-close").click()')

    # ページ終了まで繰り返し取得
    log("処理開始")
    total_name_list = []
    total_detail_list = []
    total_target_list = []
    total_local_list = []
    total_fee_list = []
    total_starting_salary_list = []
    success = 0
    fail = 0
    count = 0
    while True:
        detail_list = []
        target_list = []
        local_list = []
        fee_list = []
        starting_salary_list = []
        count += 1
        # 検索結果の一番上の会社名を取得
        try:
            name_list = driver.find_elements_by_class_name("cassetteRecruit__name")
            items = driver.find_elements_by_class_name("tableCondition")

            for table in items:
                try:
                    ele = table.find_elements_by_class_name("tableCondition__body")
                    detail_list.append(ele[0])
                    target_list.append(ele[1])
                    local_list.append(ele[2])
                    fee_list.append(ele[3])
                    starting_salary_list.append(ele[4])
                except:
                    pass
            success += 1
        except Exception as e:
            log(e)
            fail += 1
        
        # 1ページ分繰り返し
        for name,detail,target,local,fee,starting_salary in zip(name_list,detail_list,target_list,local_list,fee_list,starting_salary_list):
            print(name.text,detail.text,target.text,local.text,fee.text,starting_salary.text)
            total_name_list.append(name.text)
            total_detail_list.append(detail.text)
            total_target_list.append(target.text)
            total_local_list.append(local.text)
            total_fee_list.append(fee.text)
            total_starting_salary_list.append(starting_salary.text)

        print(f"{count}ページ終了しました")
        
        next_botton = driver.find_elements_by_class_name("iconFont--arrowLeft")
        if len(next_botton) >=1:
            next_link = next_botton[0].get_attribute("href")
            driver.get(next_link)
        else:
            break

    log("処理終了")

    #現在日付時刻取得
    dt_now = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    
    #csv出力
    df = pd.DataFrame(
            {"会社名": total_name_list, 
            "仕事内容": total_detail_list,
            "対象": total_target_list,
            "勤務地":total_local_list,
            "給与":total_fee_list,
            "初年度年収":total_starting_salary_list})
    df.to_csv(csv_pass.format(search_keyword=search_keyword,dt_now=dt_now),encoding="utf-8-sig")
        

# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()
