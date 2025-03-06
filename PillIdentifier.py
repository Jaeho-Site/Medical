from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

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
    
    def DriverInput(self,selector,value):
        input_field = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
        input_field.send_keys(value)

    def DriverClick(self,selector):      
        target_element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,selector)))
        self.driver.execute_script("arguments[0].click();", target_element.find_element(By.TAG_NAME, "a"))       
        print(f"{selector} 클릭 완료")

    def DirverButton(self,selector):
        search_button = self.driver.find_element(By.CSS_SELECTOR, selector)
        search_button.click()

    def IdentifyPill(self, shape, color, imprint1, imprint2):
        if imprint1:
            self.DriverInput("#drug_print_front", imprint1)

        if imprint2:
            self.DriverInput("#drug_print_back", imprint2)

        if shape and shape in self.ShapeSelectorDict:
            self.DriverClick(self.ShapeSelectorDict[shape])

        if color in self.ColorList:
            self.DriverClick("#color_" + color)

        self.DirverButton("#btn_idfysearch")

        result_table = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#idfytotal0")))
        pill_names = self.driver.find_elements(By.CSS_SELECTOR, "#idfytotal0 > tbody > tr > td.txtL.name")
        self.result_html = "\n".join([pill.text for pill in pill_names])

        print("검색된 약 목록:")
        print(self.result_html)

           
if __name__ == "__main__":
    driver = webdriver.Chrome()
    ident = PillIdentifier(driver)
    ident.IdentifyPill("circular", "pink", "LH", "")
    print("검색 결과 HTML:", ident.result_html)

    driver.quit()