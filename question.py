from database import Database
import random
import pymysql


class Exam:
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
    def create_random_exam(self, test_id, module):
        # Initialize an empty list to store the questions
        questions = []
        # Generate a random number of questions for the Verbal module
            # Generate 12-14 questions for Information and Idea topic
        num_ii = 7
        questions += self.get_random_questions('Information and Idea',1,num_ii,test_id)
        questions += self.get_random_questions('Information and Idea',2,num_ii,test_id)


            # Generate 13-15 questions for Craft and Structure topic

            # Fill the remaining quota with random questions
        return questions

    # Get questions by topic

    # Get random questions
    def get_random_questions(self, test_id,topic, module,num_questions):
        # Use query function to find random questions
        self.query('UPDATE questions SET tests_id = %s WHERE question_topic = %s AND module = %s AND tests_id = NULL ORDER BY RAND() LIMIT %s', (test_id,topic, module, num_questions))
        result =  self.query("SELECT * FROM questions WHERE test_id=%s", (test_id))
        return result