from services.member_service import MemberService


def main():
    member_service = MemberService()

    while True:
        print("\n=== 📚 독서 기록 관리 시스템 ===")
        if member_service.current_user:
            print(f"현재 접속 중: {member_service.current_user.name} ({member_service.current_user.user_id})")
            print("1. 로그아웃")
            print("2. 프로그램 종료")
        else:
            print("1. 회원가입")
            print("2. 로그인")
            print("3. 프로그램 종료")
            
        choice = input("메뉴 선택: ").strip()

        if member_service.current_user:
            # 로그인 상태일 때의 메뉴
            if choice == '1':
                member_service.logout()
            elif choice == '2':
                print("프로그램을 종료합니다.")
                break
            else:
                print(" 잘못된 입력입니다. 다시 선택해주세요.")
        else:
            # 비로그인 상태일 때의 메뉴
            if choice == '1':
                member_service.register()
            elif choice == '2':
                if member_service.login():
                    # 로그인 성공 후 추가 도서 관리 메뉴 등으로 분기 가능
                    pass
            elif choice == '3':
                print("프로그램을 종료합니다.")
                break
            else:
                print(" 잘못된 입력입니다. 다시 선택해주세요.")

if __name__ == "__main__":
    main()