# database.py
import pymysql
from Objectclass import User, Questions , User_answer




class Database:
    def __init__(self, config):
        self.connection = pymysql.connect(**config)
        self.cursor = self.connection.cursor()
    #Close connection to database
    def close(self):
        self.connection.close()

    #Query function
    def query(self, query, params=None):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    #Execute function
    def execute(self, query, params=None):
        self.cursor.execute(query, params)
        self.connection.commit()
    def calculate_score(self,user_test_id,type,module):
        result = self.query('SELECT * FROM user_answer INNER JOIN questions ON user_answer.questions_id = questions.id WHERE type = %s  AND iscorrect= True AND user_test_id = %s AND module = %s',(type,user_test_id,module))
        return len(result)
    
    def update_score(self,user_test_id,score, type):
        if type == "Total":
            self.execute('UPDATE user_test SET score = %s  WHERE id = %s ' , (score,user_test_id))
        elif type == "Math":
            self.execute('UPDATE user_test SET math_score = %s  WHERE id = %s ' , (score,user_test_id))
        elif  type == "Verbal":
            self.execute('UPDATE user_test SET verbal_score = %s  WHERE id = %s ' , (score,user_test_id))
        self.connection.commit()
        return self.cursor.lastrowid
    def update_end_time(self,user_test_id):
        self.execute('UPDATE user_test SET end_date = NOW()  WHERE id = %s ' , (user_test_id))
        self.execute('UPDATE user_test SET status = "DONE"  WHERE id = %s ' , (user_test_id))
        return self.cursor.lastrowid
    def update_time(self,user_test_id,time):
        self.execute('UPDATE user_test SET time_used = %s  WHERE id = %s ' , (time,user_test_id))
        return self.cursor.lastrowid




    def get_questions_by_topic(self, topic):
        # Use query function to find questions in database
        result = self.query('SELECT * FROM questions WHERE question_topic = %s',(topic,))
        if result:
            questions = []
            for row in result:
                
                id, tests_id,question_topic, question_skill, question_text, option_1, option_2, option_3, option_4, correct_option, difficulty, subquestion_text,type,module = row
                question =  Questions(id, tests_id, question_topic, question_skill, question_text, option_1, option_2, option_3, option_4, correct_option, difficulty, subquestion_text,type,module)
                questions.append(question)
            return questions
        # If no questions were found, return None
        return result
    def get_questions_by_type(self, type):
        # Use query function to find questions in database
        result = self.query('SELECT * FROM questions WHERE type = %s',(type,))
        if result:
            questions = []
            for row in result:
                
                id, tests_id,question_topic, question_skill, question_text, option_1, option_2, option_3, option_4, correct_option, difficulty, subquestion_text,type,module = row
                question =  Questions(id, tests_id, question_topic, question_skill, question_text, option_1, option_2, option_3, option_4, correct_option, difficulty, subquestion_text,type,module)
                questions.append(question)
            return questions
    def get_questions_by_id(self, id):
        # Use query function to find questions in database
        result = self.query('SELECT * FROM questions WHERE id = %s',(id,))
        if result:
            questions = []
            for row in result:
                
                id, tests_id,question_topic, question_skill, question_text, option_1, option_2, option_3, option_4, correct_option, difficulty, subquestion_text,type,module = row
                question =  Questions(id, tests_id, question_topic, question_skill, question_text, option_1, option_2, option_3, option_4, correct_option, difficulty, subquestion_text,type,module)
                questions.append(question)
            return questions
        # If no questions were found, return None
        return result
    def get_questions_by_skill(self, skill):
        # Use query function to find questions in database
        result = self.query('SELECT * FROM questions WHERE question_skill = %s',(skill,))
        if result:
            questions = []
            for row in result:
                
                id, tests_id,question_topic, question_skill, question_text, option_1, option_2, option_3, option_4, correct_option, difficulty, subquestion_text,type,module = row
                question =  Questions(id, tests_id, question_topic, question_skill, question_text, option_1, option_2, option_3, option_4, correct_option, difficulty, subquestion_text,type,module)
                questions.append(question)
            return questions
        # If no questions were found, return None
        return result
    def get_questions_by_tests_id(self, tests_id):
        # Use query function to find questions in database
        result = self.query('SELECT * FROM questions WHERE tests_id = %s',(tests_id,))
        if result:
            questions = []
            for row in result:
                
                id, tests_id,question_topic, question_skill, question_text, option_1, option_2, option_3, option_4, correct_option, difficulty, subquestion_text,type,module = row
                question =  Questions(id, tests_id, question_topic, question_skill, question_text, option_1, option_2, option_3, option_4, correct_option, difficulty, subquestion_text,type,module)
                questions.append(question)
            return questions
        # If no questions were found, return None
        return result
    def get_questions_by_tests_id_and_module_section_and_level(self, tests_id,module,section,level):
        # Use query function to find questions in database
        if level == "hard":
            nl= 2
        else:
            nl= 1

        result = self.query('SELECT * FROM questions WHERE tests_id = %s AND module = %s AND type = %s AND difficulty = %s',(tests_id,module,section,nl))
        if result:
            questions = []
            for row in result:
                
                id, tests_id,question_topic, question_skill, question_text, option_1, option_2, option_3, option_4, correct_option, difficulty, subquestion_text,type,module = row
                question =  Questions(id, tests_id, question_topic, question_skill, question_text, option_1, option_2, option_3, option_4, correct_option, difficulty, subquestion_text,type,module)
                questions.append(question)
            return questions
        # If no questions were found, return None
        return result
    def check_answer(self, id,answer):

        result = self.query('SELECT correct_option FROM questions WHERE id = %s',(id,))
        if result:
            correct_option = str(result[0][0])
            
            if correct_option == answer:
                return True
            else:
                return False 
    def get_user_test_id_by_student_id_and_tests_id(self, student_id,tests_id):
        #Use query function to find user in database
        result = self.query('SELECT id FROM user_test WHERE student_id = %s AND tests_id = %s', (student_id,tests_id))
        #If user data was found return user infomation
        if result:
            id = result[0]
            return id
        #If don't found don't do anything
        return None    
    def get_user_answer_id_by_questions_id_and_user_test_id(self, questions_id,user_test_id):
        #Use query function to find user in database
        result = self.query('SELECT id FROM user_answer WHERE questions_id = %s AND user_test_id = %s', (questions_id,user_test_id))
        #If user data was found return user infomation
        if result:
            id = result[0]
            return id
        #If don't found don't do anything
        return None
    def get_user_input_by_questions_id_and_user_test_id(self, questions_id,user_test_id):
        #Use query function to find user in database
        result = self.query('SELECT user_input FROM user_answer WHERE questions_id = %s AND user_test_id = %s', (questions_id,user_test_id))
        #If user data was found return user infomation
        if result:
            id = result[0]
            return id
        #If don't found don't do anything
        return None
    def get_status(self, user_test_id):
        #Use query function to find user in database
        result = self.query('SELECT status FROM user_test WHERE id = %s', (user_test_id))
        #If user data was found return user infomation
        if result:
            id = result[0]
            return id
        #If don't found don't do anything
        return None
    def get_questions_id_by_questions_id_and_user_test_id(self, questions_id,user_test_id):
        #Use query function to find user in database
        result = self.query('SELECT questions_id FROM user_answer WHERE questions_id = %s AND user_test_id = %s', (questions_id,user_test_id))
        #If user data was found return user infomation
        if result:
            id = result[0]
            return id
        #If don't found don't do anything
        return None
    def get_user_answer_by_type_and_user_test_id_and_module(self, type, user_test_id, module):
        # Use query function to find questions in database
        result = self.query('SELECT user_answer.id, user_test_id, questions_id, user_input, iscorrect FROM user_answer INNER JOIN questions ON user_answer.questions_id = questions.id WHERE type = %s  AND user_test_id = %s AND module = %s',(type,user_test_id,module))
        if result:
            user_answers = []
            for row in result:
                
                id, user_test_id, questions_id, user_input, iscorrect = row
                user_answer =  User_answer(id, user_test_id, questions_id, user_input, iscorrect)
                user_answers.append(user_answer)
            return user_answers
    def get_time_value(self, id):
        #Use query function to find user in database
        result = self.query('SELECT time_used FROM user_test WHERE id = %s ', (id,))
        #If user data was found return user infomation
        if result:
            id = result[0]
            return id
        #If don't found don't do anything
        return None
    #Get user info grom database
    def get_user_by_student_id(self, student_id):
        #Use query function to find user in database
        result = self.query('SELECT id, student_id, password_hashed ,first_name,last_name,gmail,phone_number  FROM students WHERE student_id = %s', (student_id,))
        #If user data was found return user infomation
        if result:
            id, student_id, password_hashed ,first_name,last_name,gmail,phone_number= result[0]
            return User(id, student_id, password_hashed,first_name,last_name,gmail,phone_number)
        #If don't found don't do anything
        return None
    def get_user_by_id(self, id):
        #Use query function to find user in database
        result = self.query('SELECT id, student_id, password_hashed ,first_name,last_name,gmail,phone_number  FROM students WHERE id = %s', (id,))
        #If user data was found return user infomation
        if result:
            id, student_id, password_hashed ,first_name,last_name,gmail,phone_number= result[0]
            return User(id, student_id, password_hashed,first_name,last_name,gmail,phone_number)
        #If don't found don't do anything
        return None
    def get_user_by_gmail(self, gmail):
        #Use query function to find user in database
        result = self.query('SELECT id, student_id, password_hashed ,first_name,last_name,gmail,phone_number  FROM students WHERE gmail = %s', (gmail,))
        #If user data was found return user infomation
        if result:
            id, student_id, password_hashed ,first_name,last_name,gmail,phone_number= result[0]
            return User(id, student_id, password_hashed,first_name,last_name,gmail,phone_number)
        #If don't found don't do anything
        return None
    def get_user_answer_by_student_id_and_questions_id(self, student_id,questions_id):
        #Use query function to find user in database
        result = self.query('SELECT * FROM user_answer WHERE student_id = %s AND questions_id = %s', (student_id,questions_id))
        #If user data was found return user infomation
        if result:
            id, user_test_id, questions_id, user_input, iscorrect = result[0]
            return User_answer(id, user_test_id, questions_id, user_input, iscorrect)
        #If don't found don't do anything
        return None
    
    #Create user function
    def create_user(self,first_name,last_name, gmail, password_hash):
        try:
            #Use execute function to put user data on database
            self.execute('INSERT INTO students (first_name, last_name, gmail, password_hashed) VALUES (%s, %s, %s, %s)',
                         (first_name, last_name, gmail, password_hash))
            #Commit data
            self.connection.commit()
            return self.cursor.lastrowid
        #If it have any error with database It will pop a messange in terminal
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
    def create_user_answer(self,user_test_id,questions_id,user_input,iscorrect):
        try:
            self.execute('INSERT INTO user_answer (user_test_id, questions_id, user_input, iscorrect) VALUES (%s, %s, %s, %s)',
                     (user_test_id, questions_id, user_input, iscorrect))

            self.connection.commit()
            return self.cursor.lastrowid
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
    def update_user_answer(self,user_test_id,questions_id,user_input,iscorrect):
        try:
            self.execute('UPDATE user_answer SET user_input = %s ,iscorrect = %s WHERE user_test_id = %s AND questions_id = %s',
                     (user_input, iscorrect,user_test_id, questions_id ))

            self.connection.commit()
            return self.cursor.lastrowid
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
    def create_tests(self,test_name,test_description,test_type):
        try:
            #Use execute function to put user data on database
            self.execute('INSERT INTO students (test_name, test_description, test_type) VALUES (%s, %s, %s)',
                         (test_name, test_description, test_type))
            #Commit data
            self.connection.commit()
            return self.cursor.lastrowid
        #If it have any error with database It will pop a messange in terminal
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
    def create_user_test(self,test_id,student_id,status):
        try:
            #Use execute function to put user data on database
            self.execute('INSERT INTO user_test (tests_id, student_id, status) VALUES (%s, %s, %s)',
                         (test_id, student_id, status))
            #Commit data
            self.connection.commit()
            return self.cursor.lastrowid
        #If it have any error with database It will pop a messange in terminal
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
    
        
    def get_random_questions(self, test_id,topic, module,num_questions):
        # Use query function to find random questions
        self.execute('UPDATE questions SET tests_id = %s WHERE question_topic = %s AND module = %s  AND tests_id IS NULL ORDER BY RAND() LIMIT %s', (test_id,topic, module, num_questions))
        result =  self.query("SELECT * FROM questions WHERE tests_id=%s", (test_id))
        if result:
            questions = []
            for row in result:
                
                id, tests_id,question_topic, question_skill, question_text, option_1, option_2, option_3, option_4, correct_option, difficulty, subquestion_text,type,module = row
                question =  Questions(id, tests_id, question_topic, question_skill, question_text, option_1, option_2, option_3, option_4, correct_option, difficulty, subquestion_text,type,module)
                questions.append(question)
            return questions    
        # If no questions were found, return None
        return result
    def create_exam(self,test_id):
        Ii1 = self.get_random_questions(test_id, "Information and Ideas",1,8)
        Cs1 = self.get_random_questions(test_id, "Craft and Structure",1,6)
        Ei1 = self.get_random_questions(test_id, "Expression of Ideas",1,6)
        Sc1 = self.get_random_questions(test_id, "Standard English Conventions",1,7)

        
        Ii2 = self.get_random_questions(test_id, "Information and Ideas",2,6)
        Cs2 = self.get_random_questions(test_id, "Craft and Structure",2,7)
        Ei2 = self.get_random_questions(test_id, "Expression of Ideas",2,6)
        Sc2 = self.get_random_questions(test_id, "Standard English Conventions",2,8)

        Ag1 = self.get_random_questions(test_id, "Algebra",1,8)
        Am1 = self.get_random_questions(test_id, "Advanced Math",1,6)
        Pd1 = self.get_random_questions(test_id, "Problem Solving and Data Analysis",1,4)
        Gt1 = self.get_random_questions(test_id, "Geometry and Trigonometry",1,3)

        
        Ag2 = self.get_random_questions(test_id, "Algebra",2,7)
        Am2 = self.get_random_questions(test_id, "Advanced Math",2,9)
        Pd2 = self.get_random_questions(test_id, "Problem Solving and Data Analysis",2,3)
        Gt2 = self.get_random_questions(test_id, "Geometry and Trigonometry",2,4)

        result = Ii1 + Cs1 + Ei1 + Sc1 +Ii2 + Cs2 + Ei2 + Sc2 + Ag1 + Am1 + Pd1 + Gt1  + Ag2 + Am2 + Pd2 +  Gt2
        return result



