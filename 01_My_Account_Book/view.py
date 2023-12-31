class View:
    # (1) 메인 페이지 디자인
    def main():
        str = """
-----------------------------
       * 나만의 가계부 *
-----------------------------
  1. 가계부 불러오기
  2. 가계부 조회하기
  3. 데이터 입력
  4. 데이터 수정
  5. 데이터 삭제
  6. 프로그램 종료
-----------------------------"""
        return str

    # (2) 가계부 불러오기 페이지 디자인
    def load_account():
        str = """
-----------------------------
      * 가계부 불러오기 *
-----------------------------
  불러오고자 하는 가계부의
  파일명을 입력하세요.
  파일 위치: MY_Account_Book 아래

  입력 방법: file.excel
-----------------------------"""
        return str
    
    def load_account_done(result):
        str = f"""
-----------------------------
      * 가계부 불러오기 *
-----------------------------
  {result}
-----------------------------"""
        return str
    
    # (3) 데이터 입력 페이지 디자인
    def create_data():
        str = """
-----------------------------
        * 데이터 입력 *
-----------------------------
  데이터를 입력하세요.
  입력 방법:
  날짜,품목,수입,지출,메모
-----------------------------"""
        return str
    
    # (4) 데이터 수정 페이지 디자인
    def edit_data():
        str = """
-----------------------------
        * 데이터 수정 *
-----------------------------
  수정하고 싶은 데이터의
  일련번호를 입력하세요.

  입력 방법: 1
-----------------------------"""
        return str
    
    # (5) 데이터 삭제 페이지 디자인
    def delete_data():
        str = """
-----------------------------
        * 데이터 삭제 *
-----------------------------
  삭제하고 싶은 데이터의
  일련번호를 입력하세요.

  입력 방법: 1
-----------------------------"""
        return str
    
    # (6) 가계부 조회 페이지 디자인
    def view_data():
        str = """
-----------------------------
        * 가계부 조회 *
-----------------------------
  조건을 설정하고 싶은 열과
  조건 하나를 입력하세요.

  조건 열:
  날짜, 품목, 수입, 지출, 메모

  입력 방법: 날짜, 2023-12-12

  * 모두 조회하고 싶다면 : 모두

-----------------------------"""
        return str
    
    # (7) 가계부 종료 페이지 디자인
    def unload_me():
        str = """
-----------------------------
        * 가계부 종료 *
-----------------------------
  가계부 프로그램을 종료합니다.
-----------------------------"""
        return str