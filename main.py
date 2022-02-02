from selenium import webdriver
from selenium.webdriver.chrome import service as fs
from time import sleep
import code
import time

# 設定
chrome_driver_path = 'chromedriver.exe'
user_data_dir = r'.\tmp\User Data\\'
profile_dir = 'Profile 1'


# Chrome起動
options = webdriver.ChromeOptions()
options.add_argument('--user-data-dir={}'.format(user_data_dir))
options.add_argument('--profile-directory={}'.format(profile_dir))
chrome_service = fs.Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(
    service=chrome_service,
    options=options
)

# YouTube Audio Libraryを表示
driver.get('https://www.youtube.com/audiolibrary')

# 対話モード -> exit()で続行
code.interact(local=locals())

# 初回のダイアログを消す
if driver.find_elements_by_id('dismiss-button'):
    dismiss = driver.find_element_by_id('dismiss-button').click()

# 表示件数を100にする
driver.find_element_by_xpath('//ytcp-select[@id="page-size"]//span[contains(@class,"ytcp-text-dropdown-trigger")]').click()
driver.find_element_by_xpath('//*[@id="select-menu-for-page-size"]//ytcp-ve//yt-formatted-string[contains(@class,"ytcp-text-menu") and text()="100"]').click()

# ちょい待ち
time.sleep(1)

# 全ページ
for i in range(20):
    # すべてのダウンロードボタンを押す
    driver.set_script_timeout(200)
    result = driver.execute_async_script('''
        const callback = arguments[0]
        const downloads = document.querySelectorAll('#download')
        const _sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
        //let i = 3
        for (const download of downloads) {
            download.click()
            await _sleep(1000)
            //if (--i <= 0) break
        }
        callback(true)
    ''')

    # ちょい待ち
    time.sleep(1)

    # 現在のページを取得
    page_text_before = driver.find_element_by_xpath('//span[contains(@class,"page-description")]').text

    # 次ページボタンをクリック
    driver.find_element_by_xpath('//ytcp-icon-button[@id="navigate-after"]').click()

    # ちょい待ち
    time.sleep(1)

    # 現在のページを取得
    page_text_after = driver.find_element_by_xpath('//span[contains(@class,"page-description")]').text

    # ページが遷移していなかったら終わり
    if page_text_before == page_text_after:
        break

# 対話モード
code.interact(local=locals())

# ブラウザ終了
driver.quit()
