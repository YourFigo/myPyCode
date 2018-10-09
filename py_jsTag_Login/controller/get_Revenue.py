from revenue import revenue_AOL
from revenue import revenue_Adview
from revenue import revenue_Mobfox
from revenue import revenue_Mopub
from revenue import revenue_NewCM
from revenue import revenue_OpenX
from revenue import revenue_Pubnative
from revenue import revenue_Solo
from revenue import revenue_Tappx
from revenue import revenue_cm
from revenue import revenue_Smaato


def get_Revenue():
    print("正在爬取数据..........")
    revenue_Mobfox.test_Mobfox()
    print("\n")
    revenue_Mopub.test_Mopub()
    print("\n")
    revenue_Tappx.test_Tappx()
    print("\n")
    revenue_Smaato.test_Smaato()
    print("\n")
    revenue_cm.test_cm()
    print("\n")
    revenue_AOL.test_AOL()
    print("\n")
    revenue_Pubnative.test_Pubnative()
    print("\n")
    revenue_Adview.test_Adview()
    print("\n")
    revenue_NewCM.test_NewCM()
    print("\n")
    revenue_OpenX.test_OpenX()
    print("\n")
    revenue_Solo.test_Solo()
    print("所有抓取结束")

if __name__ == '__main__':
    get_Revenue()