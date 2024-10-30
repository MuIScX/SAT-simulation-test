# user.py
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, user_id, student_id, password_hashed,first_name, last_name,gmail,phone_number):
        self.id = user_id
        self.student_id = student_id
        self.password_hashed = password_hashed
        self.first_name = first_name
        self.last_name = last_name
        self.gmail = gmail
        self.phone_number = phone_number

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class Questions:
    def __init__(self, id, tests_id, question_topic, question_skill, question_text, option_1, option_2, option_3, option_4, correct_option, difficulty, subquestion_text ,type,module,):

        self.id = id
        self.tests_id = tests_id
        self.question_topic = question_topic
        self.question_skill = question_skill
        self.question_text = question_text
        self.option_1 = option_1
        self.option_2 = option_2
        self.option_3 = option_3
        self.option_4 = option_4
        self.correct_option = correct_option
        self.difficulty = difficulty
        self.subquestion_text = subquestion_text
        self.type = type
        self.module = module
    
class User_answer:
    def __init__(self, id, user_test_id, questions_id, user_input, iscorrect):
        
        self.id = id
        self.user_test_id = user_test_id
        self.questions_id = questions_id
        self.user_input = user_input
        self.iscorrect = iscorrect

class User_test:
    def __init__(self, id, student_id, time_used, start_date, end_date, score, status, math_score, verbal_score):
        
        self.id = id
        self.tests_id = student_id
        self.question_topic = time_used
        self.question_skill = start_date
        self.question_text = end_date
        self.option_1 = score
        self.option_2 = status
        self.option_3 = math_score
        self.option_4 = verbal_score

class Tests:
    def __init__(self, id, test_name,  test_description, test_type):
        
        self.id = id
        self.test_name = test_name
        self.test_description = test_description
        self.test_type = test_type
    
