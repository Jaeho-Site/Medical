from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

class PillIdentifier:
    def __init__(self, driver):
        self.driver = driver
        self.driver.get("https://www.health.kr/searchIdentity/search.asp")
        self.wait = WebDriverWait(driver, 10)
        
        self.result = []
        self.result_html = ''
        
        # 알약 모양 선택자 정의(약학정보원에서 검색가능한 모양과 색상)
        self.ShapeSelectorDict = {
            "circular": "#shape_01",
            "oval": "#shape_02",
            "semicircular": "#shape_03",
            "triangular": "#shape_04",
            "square": "#shape_05",
            "rhombus": "#shape_06",
            "oblong": "#shape_07",
            "octagon": "#shape_08",
            "hexagon": "#shape_09",
            "pentagon": "#shape_10",
            "all": "#shape_all"
        }
        
        # 알약 색상 리스트 정의
        self.ColorList = ["white","yellow","orange","pink","red","brown",
                         "ygreen","green","bgreen","blue","navy","wine",
                         "purple","grey","black","transp","all"] 