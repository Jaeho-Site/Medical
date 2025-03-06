from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

class PillIdentifier:
    
    def __init__(self,driver):
        self.driver = driver
        
        self.driver.get("https://www.health.kr/searchIdentity/search.asp")
        self.wait = WebDriverWait(driver, 10)
        
        self.result = []
        self.result_html = ''
        
        self.ShapeSelectorDict = {
            "circular" : "#shape_01",
            "oval" : "#shape_02",
            "semicircular" : "#shape_03",
            "triangular" : "#shape_04",
            "square" : "#shape_05",
            "rhombus" : "#shape_06",
            "oblong" : "#shape_07", # 장방형
            "octagon" : "#shape_08",
            "hexagon" : "#shape_09",
            "pentagon" : "#shape_10", 
            "all" : "#shape_all"
        }
        
        self.ColorList = ["white","yellow","orange","pink","red","brown","ygreen","green","bgreen","blue","navy","wine","purple","grey","black","transp","all"]
        
    def DriverInput(self,selector,value):
        input_field = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
        input_field.send_keys(value)

    def DriverClick(self,selector):
        try:
            target_element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,selector)))
            self.driver.execute_script("arguments[0].click();", target_element.find_element(By.TAG_NAME, "a"))
            
            print(f"{selector} 클릭 완료")

        except TimeoutException:
            print(f"오류: {selector} 요소를 찾을 수 없거나 클릭할 수 없습니다.")
            raise

    def DirverButton(self,selector):
        search_button = self.driver.find_element(By.CSS_SELECTOR, selector)
        search_button.click()

    def ParseData(self):
        # 파싱할 데이터 추출
        try:
            table_body = self.driver.find_element(By.CSS_SELECTOR, "#idfytotal0 > tbody")  # 테이블 body 선택
            rows = table_body.find_elements(By.XPATH, "./tr")  # tbody 바로 아래의 tr 요소만 선택
            
            print(len(rows))

            for i in range(3, len(rows) + 1):  # 1부터 시작하여 첫 번째 tr을 제외
                try:
                    element_selector = f"#idfytotal0 > tbody > tr:nth-child({i}) > td.txtL.name"
                    element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, element_selector)))
                    self.result.append(element.text)
                except TimeoutException:
                    print(f"오류: {i}번째 결과 요소를 찾을 수 없습니다.")
                    continue
                except Exception as e:
                    print(f"오류 발생: {e}")
                    continue

        except Exception as e:
            print(f"데이터 파싱 중 오류 발생: {e}")

    def IdentifyPill(self,shape,color,imprint1,imprint2):
        try:
            if imprint1:
                self.DriverInput("#drug_print_front",imprint1)
            
            if imprint2:
                self.DriverInput("#drug_print_back",imprint2)
            
            if shape:
                self.DriverClick(self.ShapeSelectorDict[shape])
            
            if color in self.ColorList:
                self.DriverClick("#color_" + color)
                
            self.DirverButton("#btn_idfysearch")

            try:
                result_table = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#idfytotal0")))
                self.result_html = result_table.get_attribute('outerHTML')
                
            except TimeoutException:
                print("오류: 결과 테이블을 찾을 수 없습니다.")
                raise
            
            self.ParseData()
        
        except Exception as e:
            print(f"오류 발생: {e}")

if __name__ == "__main__":
    driver = webdriver.Chrome()
    ident = PillIdentifier(driver)
    ident.IdentifyPill("circular","pink","LH","")
    print(ident.result)
    #print(ident.result_html)