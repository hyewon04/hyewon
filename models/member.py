class Member:
    """회원 데이터를 저장하는 클래스"""
    def __init__(self, user_id, password, name, phone, security_question, security_answer, joined_at):
        self.user_id = user_id
        self.password = password
        self.name = name
        self.phone = phone
        self.security_question = security_question
        self.security_answer = security_answer
        self.joined_at = joined_at

    def to_dict(self):
        """객체를 딕셔너리 형태로 변환 (JSON 저장용)"""
        return {
            "user_id": self.user_id,
            "password": self.password,
            "name": self.name,
            "phone": self.phone,
            "security_question": self.security_question,
            "security_answer": self.security_answer,
            "joined_at": self.joined_at

        }

    @classmethod
    def from_dict(cls, data):
        """딕셔너리 데이터로부터 Member 객체 생성 (JSON 로드용)"""
        return cls(
            data["user_id"],
            data["password"],
            data["name"],
            data["phone"],
            data["security_question"],
            data["security_answer"],
            data["joined_at"]

        )