# import re : 문자열이 특정한 규칙과 일치 하는지 확인하는 코드
import os
import re
from datetime import datetime

from models.member import Member
from utils.file_handler import FileHandler


class MemberService:
    def __init__(self, filename="data/members.json"):
        self.filename = filename
        self.members = {}  # {user_id: Member 객체}
        self.current_user = None  # 현재 로그인한 회원 객체
        self.load_members()

    def load_members(self):
        """프로그램 실행 시 JSON 파일에서 회원 정보를 불러옴"""
        data_list = FileHandler.load_json(self.filename)
        for item in data_list:
            member = Member.from_dict(item)
            self.members[member.user_id] = member
        return self.members

    def save_members(self):
        """회원 정보 변경 시 JSON 파일에 즉시 저장"""
        # data 폴더가 없으면 생성
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        data_list = [member.to_dict() for member in self.members.values()]
        FileHandler.save_json(self.filename, data_list)

    def check_duplicate(self, user_id):
        """동일한 회원 아이디 등록 방지 (중복 검사)"""
        return user_id in self.members

    # 이메일 형식 확인 코드
    def is_valid_email(self, email):
        # fullmatch(): 문자열 전체와 일치하는지 확인 / is not None 으로 True or False  
        # [^ ]: 대괄호 안의 ^는 그 뒤에 나오는 것들을 제외 한다는 뜻
        # r을 이용해 \를 문자 그대로 판단 
        return re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email) is not None

    # 비밀번호 password 형식 확인 코드
    def is_valid_password(self, password):
        # re.search(): 문자열에서 특정 패턴 찾기 / 조건에 한 문자라도 맞으면 결과를 반환
        return (
            len(password) >= 8
            and re.search(r"[A-Za-z]", password) # 영어 대소문자 중에 하나라도 포함되는가
            and re.search(r"\d", password)       # 숫자가 하나라도 포함되는가
            and re.search(r"[^A-Za-z0-9]", password) # 영어와 숫자를 제외한 다른 특수문자가 하나라도 포함되는가 
        )

    # 전화번호 확인 형식 확인 코드
    def is_valid_phone(self, phone):
        digits = phone.replace("-", "") # 하이픈을 지운 형태로 반환
        # isdigit(): 숫자만 존재하는지 확인 
        # startswith("010"): 010로 시작하는지 확인 
        return digits.isdigit() and len(digits) == 11 and digits.startswith("010") 
    
    def register(self):

        """회원가입 기능"""

        print("\n--- [회원가입] ---")

        # 이메일 아이디 입력이 올바를 때까지 반복
        while True:
            user_id = input("이메일 아이디 입력: ").strip().lower()

            if not self.is_valid_email(user_id):
                print("올바른 이메일 형식으로 입력해 주세요.")
                continue

            if self.check_duplicate(user_id):
                print("이미 가입된 이메일입니다. 다른 이메일을 입력해 주세요.")
                continue
            
            break

        # 패스워드 입력이 올바를 때까지 반복
        while True:
            password = input("비밀번호 입력(8자 이상, 영문·숫자·특수문자 포함): ").strip()

            if not self.is_valid_password(password):
                print("패스워드 조건을 만족하지 않습니다.")
                print("영문, 숫자, 특수문자를 포함한 8자 이상으로 다시 입력해 주세요.")
                continue

            break

        # 이름 입력이 올바를 때까지 반복
        while True:
            name = input("이름 입력: ").strip()

            if not name:
                print("이름은 비워 둘 수 없습니다. 다시 입력해 주세요.")
                continue

            break

        # 핸드폰 번호 입력이 올바를 때까지 반복
        while True:
            phone = input("연락처 입력(예: 010-1234-5678): ").strip()

            if not self.is_valid_phone(phone):
                print("연락처 010으로 시작하는 11자리 번호로 다시 입력해 주세요.")
                continue

            break

        # 비밀 번호 찾기용 질문 선택
        print("\n비밀번호 찾기에 사용할 보안 질문을 선택해 주세요.")
        print("1. 가장 좋아하는 책은 무엇인가요?",
              "\n2. 가장 좋아하는 작가는 누구인가요?",
              "\n3. 가장 좋아하는 동물은 무엇인가요?",
              "\n4. 가장 기억에 남는 여행지는 어디인가요?",
              "\n5. 가장 좋아하는 계절은 무엇인가요?")
        while True:
            security_question = input("번호를 입력해 주세요: ").strip()

            if not 1 <= int(security_question) <= 5:
                print("올바른 번호를 입력해주세요")
                continue

            break 

        security_answer = input("질문에 대한 답을 입력해 주세요: ")

        # 가입일 자동 저장 
        joined_at = datetime.now().strftime("%Y-%m-%d")

        member = {
            "user_id": user_id,
            "name": name,
            "password": password,
            "phone": phone,
            "joined_at": joined_at,
            "security_question": security_question,
            "security_answer": security_answer
        }

        new_member = Member(user_id, password, name, phone,security_question,security_answer, joined_at)
        self.members[user_id] = new_member
        self.save_members()

        print("\n회원가입이 완료되었습니다!")
        print(f"아이디: {member['user_id']}")
        print(f"이름: {member['name']}")
        print(f"가입 날짜: {member['joined_at']}")

        return True
        

    def login(self):
        """로그인 기능"""
        print("\n--- [로그인] ---")
        user_id = input("아이디 입력: ").strip().lower()
        password = input("비밀번호 입력: ").strip()

        member = self.members.get(user_id)
        if member and member.password == password:
            self.current_user = member
            print(f"로그인 성공! [{member.name}]님 환영합니다.")
            return True
        else:
            print("아이디 또는 비밀번호가 일치하지 않습니다.")
            return False

    def logout(self):
        """로그아웃 기능"""
        if self.current_user:
            print(f"[{self.current_user.name}]님이 로그아웃하셨습니다.")
            self.current_user = None
        else:
            print("로그인된 사용자가 없습니다.")