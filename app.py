# app.py
from flask import Flask, render_template, request, redirect, url_for, session , jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from database import Database
from time import strptime 
from time import sleep as sl
import datetime
import json
app = Flask(__name__)
app.secret_key = '1178'

#Connect to database
db_config = {
    'host': '54.254.202.98',	
    'port': 3308,
    'user': 'satadmin',
    'password': 'Dsat@dbadmin2024',
    'database': 'satdb',
}

#Cursor
    
    




db = Database(db_config)
num = 0
def check_password(password_hashed, password):
    return check_password_hash(password_hashed, password)


@app.route('/myTest', methods=['GET', 'POST'])
def myTest():
    if 'user_id' in session:
        user = db.get_user_by_id(session["user_id"])
        return render_template('myTest.html',user=user)
    return redirect(url_for('login'))
    
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        print("POST request received at home")
        if 'start' in request.form:
            session['exam_value'] = request.form['start']

            if not db.get_user_test_id_by_student_id_and_tests_id(session['user_id'],session['exam_value']):
                print("create_user_test ")
                db.create_user_test(session['exam_value'],session['user_id'],"ONGOING")
                session['time'] = 10
                session['exam_page'] = 1
                session['vlevel'] = "easy"
                session['mlevel'] = "easy"
                session["current_module"] = 0
                session["all_time_used"] =  0
            elif db.get_user_test_id_by_student_id_and_tests_id(session['user_id'],session['exam_value']):
                if str(db.get_status(db.get_user_test_id_by_student_id_and_tests_id(session['user_id'],session['exam_value'])[0])[0]) == "DONE":
                    return redirect(url_for('score'))
            user_test_id = db.get_user_test_id_by_student_id_and_tests_id(session['user_id'],session['exam_value'])
            session["user_test_id"] = user_test_id
                 
            
            print(request.form['start'])
            return redirect(url_for('exam'))
    if 'user_id' in session:
        try:
            Done = str(db.get_status(db.get_user_test_id_by_student_id_and_tests_id(session['user_id'],session['exam_value'])[0])[0])
            print(Done)
        except: 
            Done = ""
        
        return render_template('home.html',Done=Done)
    
     #'Logged in as {}'.format(session['student_id'])
    return redirect(url_for('login'))

    
     #'Logged in as {}'.format(session['student_id']
@app.route('/preview')
def preview():
    return render_template('preview.html')

@app.route('/test')
def test():
    questions = db.get_questions_by_tests_id(1)
    question =questions[2]  
    return render_template('test.html',)

@app.route('/login', methods=['GET', 'POST'])
def login():
    #Gain infomation grom user
    if request.method == 'POST':
        print("POST")
        gmail = request.form['gmail']
        password = request.form['password']
        
        #Get user in database using function    note: All of database function is in database.py 
        user = db.get_user_by_gmail(gmail)
        #If found user in database and password is correct bring user to home page
        if user and check_password(user.password_hashed,password):
            session['user_id'] = user.id    
            session['gmail'] = user.gmail
            session['first_name'] = user.first_name
            session['last_name'] = user.last_name
            print("pass")
            return redirect(url_for('home'))
        else:
            message = "Invalid student id or password"
            return render_template('login.html',error = message)
    #If don't have post request still display login form untill user submit form
    return render_template('login.html')


@app.route('/exam', methods=['GET', 'POST'])
def exam():
    if request.method == 'POST' or "answer" in request.form:
        try:
            remain_time = request.form.get('time-value')
            module = session["current_module"]
            
            print("time = " + str(remain_time))
            try:
                x,y = remain_time.split(':')
                time = int(x)*60+int(y)   #Convert HH:
                session['time'] = time
            except:
                print("time error")
            print("POST")
            exam_page = session['exam_page']
            user_test_id = session["user_test_id"]
        
            active_value = session['exam_value']
            if session["current_module"] == 0:
                print("get data module" + str(module))
                questions = db.get_questions_by_tests_id_and_module_section_and_level(active_value,1,"Verbal",session["vlevel"])
            elif session["current_module"] == 1:
                print("get data module" + str(module))

                questions = db.get_questions_by_tests_id_and_module_section_and_level(active_value,2,"Verbal",session["vlevel"])
            elif session["current_module"] == 2:
                print("get data module" + str(module))
                questions = db.get_questions_by_tests_id_and_module_section_and_level(active_value,1,"Math",session["mlevel"])
            elif session["current_module"] == 3:
                print("get data module" + str(module))
                questions = db.get_questions_by_tests_id_and_module_section_and_level(active_value,2,"Math",session["mlevel"])
            elif session["current_module"] > 3:
                return redirect("/score")
            print (int(exam_page) -1)
            question = questions[exam_page -1]
            if questions:
                print("Question Text:", question.id)    

                # Print other relevant information about the question
            else:
                print("No questions found for topic:")
            if "answer" in request.form:
                print("Answer: " + str(request.form["answer"]))
                try:
                    answer = int(request.form['answer'])
                except:
                    answer = request.form['answer']
                text_answer = ""
                iscorrect = False
                print("Ans" + str(answer))
                if question.option_1:
                    if answer == 1:
                        print("inAnswer: " + str(answer))
                        iscorrect = db.check_answer(question.id,question.option_1)
                        print("iscorrect: " + str(iscorrect))
                        text_answer = question.option_1
                    elif answer == 2:
                        print("inAnswer: " + str(answer))
                        iscorrect = db.check_answer(question.id,question.option_2)
                        print("iscorrect: " + str(iscorrect))
                        text_answer = question.option_2
                    elif answer == 3:
                        print("inAnswer: " + str(answer))
                        iscorrect = db.check_answer(question.id,question.option_3)
                        print("iscorrect: " + str(iscorrect))
                        text_answer = question.option_3
                    elif answer == 4:
                        print("inAnswer: " + str(answer))
                        iscorrect = db.check_answer(question.id,question.option_4)
                        print("iscorrect: " + str(iscorrect))
                        text_answer = question.option_4
                else:
                    print("text_answer")
                    print("Answer: " + str(answer))
                    iscorrect = db.check_answer(question.id,str(answer))
                    print("iscorrect: " + str(iscorrect))
                    text_answer = answer


                print(text_answer)
                if db.get_user_answer_id_by_questions_id_and_user_test_id(question.id,user_test_id):
                    print("Update")
                    print(db.get_user_answer_id_by_questions_id_and_user_test_id(question.id,user_test_id))
                    db.update_user_answer(user_test_id,question.id,text_answer,iscorrect)
                else:
                    print("Create")
                    db.create_user_answer(user_test_id,question.id,text_answer,iscorrect)
                
        except:
            pass
        if "mark" in request.form:
            session[str(exam_page-1)] = True
            print(str(exam_page) + " is marked as true")
        else:
            session[str(exam_page-1)] = False
            print(str(exam_page) + " is not marked as true")
        if "Next" in request.form:
            session['exam_page'] =int(session['exam_page']) + 1
            print("next" + str(session['exam_page']))
        if "Back" in request.form and int(session['exam_page']) - 1 >0:
            session['exam_page'] =int(session['exam_page']) -1
            print("next" + str(session['exam_page']))  
        user_test_id = session["user_test_id"]
        active_value = session['exam_value']
        max_page = len(questions)

    

        if max_page == exam_page and "Next" in request.form:
            return redirect(url_for("next_module"))
        
            

    else:
        print("first")
        try:
            
            remain_time = request.form.get('time-value')
        
            print("time = " + str(remain_time))
            x,y = remain_time.split(':')
            if remain_time % 10 != 0 :

                time = int(x)*60+int(y)   #Convert HH:
                session["time"] = time
            print("1dasdasd")
        except:
            pass
        time = session["time"]
        print(time)
        module = session["current_module"]
        user_test_id = session["user_test_id"]
        active_value = session['exam_value']
        print(active_value)
        

    if session["current_module"] == 0:
        print("get data module" + str(module))
        questions = db.get_questions_by_tests_id_and_module_section_and_level(active_value,1,"Verbal",session["vlevel"])
    elif session["current_module"] == 1:
        print("get data module" + str(module))

        questions = db.get_questions_by_tests_id_and_module_section_and_level(active_value,2,"Verbal",session["vlevel"])
    elif session["current_module"] == 2:
        print("get data module" + str(module))
        questions = db.get_questions_by_tests_id_and_module_section_and_level(active_value,1,"Math",session["mlevel"])
    elif session["current_module"] == 3:
        print("get data module" + str(module))
        questions = db.get_questions_by_tests_id_and_module_section_and_level(active_value,2,"Math",session["mlevel"])
    elif session["current_module"] > 3:
        return redirect("/score")
    print()
    max_page = len(questions)
    exam_page = session['exam_page']

    print (int(exam_page) -1)
    print("maxpage"+ str(max_page))
    try:
        question = questions[exam_page-1]
    except:
        return redirect("/next_module")
    if question.type == "Verbal":
        type = "Reading & Writing"
    elif question.type == "Math":
        type = "Math"
    print(max_page)
    exam_percent = round(exam_page/max_page*100)
    try:
        userinput = db.get_user_input_by_questions_id_and_user_test_id( question.id, user_test_id)[0]
        print(userinput)
    except Exception as e :
        userinput =  ""
    try:
        mark = session[str(exam_page-1)]
        print("baesd" + str(mark))
    except Exception as e :
        mark =  ""
        print("Sesd")
    sl(1)

    return render_template('exam.html',question=question,first_name = session['first_name'],last_name = session['last_name'],type = type,exam_no = exam_page, max_page = max_page,exam_percent=exam_percent,time=session['time'],userinput=userinput,mark=mark,mlevel=session["mlevel"])

@app.route('/timeout', methods=['GET', 'POST'])
def timeout():
    if request.method == 'POST':
        active_value = session['exam_value']
        userid = session['user_id']
        print("TIME OUT")
        print(userid)
        print(active_value)
        user_test_id = session["user_test_id"]
        module = session["current_module"]
        if session["current_module"] == 2:
            math1_score = db.calculate_score(user_test_id,"Math","1")
            if int(math1_score)< 17:
                session["mlevel"] = "easy"
            else:
                session["mlevel"] = "hard"
            print(math1_score)
            print(session["mlevel"])
            
        elif session["current_module"] == 0:
            english1_score = db.calculate_score(user_test_id,"Verbal","1")
            if int(english1_score)< 17:
                session["vlevel"] = "easy"
            else:
                session["vlevel"] = "hard"
            print(english1_score)
            print(session["vlevel"])
        print("next module")
        print("current_module" +str(session["current_module"]))
        session["current_module"] = module +1
        session['exam_page'] = 1
        session["all_time_used"] +=0
        if session["current_module"]>1:
            session['time'] = 2100
        else:
            session['time'] = 1920
        active_value = session['exam_value']       
        print("current_module " +str(session["current_module"]))
            
        if session["current_module"] == 0:
            print("get data module" + str(module))
            questions = db.get_questions_by_tests_id_and_module_section_and_level(active_value,1,"Verbal",session["vlevel"])
        elif session["current_module"] == 1:
            print("get data module" + str(module))

            questions = db.get_questions_by_tests_id_and_module_section_and_level(active_value,2,"Verbal",session["vlevel"])
        elif session["current_module"] == 2:
            print("get data module" + str(module))
            questions = db.get_questions_by_tests_id_and_module_section_and_level(active_value,1,"Math",session["mlevel"])
        elif session["current_module"] == 3:
            print("get data module" + str(module))
            questions = db.get_questions_by_tests_id_and_module_section_and_level(active_value,2,"Math",session["mlevel"])
        elif session["current_module"] > 3:
            return redirect("/score")
        max_page = len(questions)
        exam_page = session['exam_page']
        print (int(exam_page) -1)
        print("maxpage"+ str(max_page))
        question = questions[exam_page -1]
        if question.type == "Verbal":
            type = "Reading & Writing"
        elif question.type == "Math":
            type = "Math"
        print(max_page)
        exam_percent = round(exam_page/max_page*100)
        
        
        
        
        return render_template('exam.html',question=question,first_name = session['first_name'],last_name = session['last_name'],type = type,exam_no = exam_page, max_page = max_page,exam_percent=exam_percent,time=session["time"],mlevel=session["mlevel"])


@app.route('/register', methods=['GET', 'POST'])
def register():
    #Gain infomation grom user
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        gmail = request.form['gmail']
        password = request.form['password']

        #Check user fill all of infomation in the form If not sent the error message
        if not first_name and last_name and gmail and password :
            message = "Please fill out the information completely."
            return render_template('register.html', error = message)
        
        #Check password and confirm password is equal ? If not sent the error message
    
        
        #Hashed password from user for security
        hashed_password = generate_password_hash(password)
        
        #Create new user
        user_id = db.create_user(first_name, last_name, gmail, hashed_password)
        
        #If user in sessin bring user to login page
        if user_id:
            
            return render_template('register.html')

    return render_template('register.html')
@app.route('/next_module', methods=['GET', 'POST'])
def next_module():
    print("budadsadtton")
    if request.method == 'POST':
        remain_time = request.form.get('time-value')
            
        print("time = " + str(remain_time))
        try:
            x,y = remain_time.split(':')
            time = int(x)*60+int(y)   #Convert HH:
            session['time'] = time
        except:
            print("time error")
        button = request.form.get('button')
        print(button)
        user_test_id = session["user_test_id"]
        if button :
            session["exam_page"] = int(button)
            return redirect(url_for('exam'))
        if "next" in request.form :
            print("next module")
            print("current_module" +str(session["current_module"]))
            if session["current_module"] == 2:
                math1_score = db.calculate_score(user_test_id,"Math","1")
                if int(math1_score)< 17:
                    session["mlevel"] = "easy"
                else:
                    session["mlevel"] = "hard"
                print("level" + session["mlevel"] )
            elif session["current_module"] == 0:
                english1_score = db.calculate_score(user_test_id,"Verbal","1")
                if int(english1_score)< 17:
                    session["vlevel"] = "easy"
                else:
                    session["vlevel"] = "hard"
                print("level" + session["vlevel"] )
            session["current_module"] = session["current_module"] +1
            session['exam_page'] = 1
            session["all_time_used"] +=session['time']

            if session["current_module"]>1:
                session['time'] = 2100
            
            else:
                session['time'] = 1920
            if session["current_module"] == 4:
                
                return redirect(url_for('score'))
            return redirect(url_for('exam'))
    active_value = session['exam_value'] 
    try:
        if session["current_module"] == 0:
        
            questions = db.get_questions_by_tests_id_and_module_section_and_level(active_value,1,"Verbal",session["vlevel"])
            section = "Reading and Writing Question"
            modules = 1
            sections= 1
        elif session["current_module"] == 1:
        
            questions = db.get_questions_by_tests_id_and_module_section_and_level(active_value,2,"Verbal",session["vlevel"])
            section = "Reading and Writing Question"
            modules = 2
            sections= 1
        elif session["current_module"] == 2:
        
            questions = db.get_questions_by_tests_id_and_module_section_and_level(active_value,1,"Math",session["mlevel"])
            section = "Mathematics Question"
            modules = 1
            sections= 2
        elif session["current_module"] == 3:
        
            questions = db.get_questions_by_tests_id_and_module_section_and_level(active_value,2,"Math",session["mlevel"])
            section = "Mathematics Question"
            modules = 2
            sections= 2
        else:
                    
            return redirect("/score")
    except:
        return redirect("/score")
    user_test_id = session["user_test_id"]
    print(user_test_id[0])
    user_answers = db.get_user_answer_by_type_and_user_test_id_and_module("Verbal",user_test_id[0],"1")
    try:
        user_answer = user_answers[0].user_input
    except:
        user_answer = ""
    print(user_answer)
    max_page = len(questions)
    qs = []
    mk = []
    for  i in range(max_page):
        try:
            if db.get_questions_id_by_questions_id_and_user_test_id(questions[i].id, user_test_id)[0] == questions[i].id:
                print(db.get_questions_id_by_questions_id_and_user_test_id(questions[i].id, user_test_id)[0])
                print(questions[i].id)
                print(True)
                qs.append(True)
            else:
                print(db.get_questions_id_by_questions_id_and_user_test_id(questions[i].id, user_test_id)[0])
                print(questions[i].id)  
                print(False)
                qs.append(False)
        except:
            print(False)
            qs.append(False)
    for j in  range(max_page):
        mk.append(session[str(j)])
        print(" HI " + str(session[str(j)]) )
    
    
    return render_template('next_module.html',qs=qs,max_page = max_page,mk=mk,section=section,modules=modules,sections=sections)

@app.route('/score')
def score():
    try:
        all_time_used = 8040 - session["all_time_used"]
    except:
        all_time_used = 0

    user_test_id = session["user_test_id"]
    db.update_time(user_test_id,all_time_used)
    math1_score = db.calculate_score(user_test_id,"Math","1")
    
    math2_score = db.calculate_score(user_test_id,"Math","2")
    
    print(math1_score)
    print(math2_score)
    correct_math_module1 = math1_score
    correct_math_module2 = math2_score
    math_score = 0
    

    if correct_math_module1 == 22 and correct_math_module2 == 22:
        math_score = 800
    elif correct_math_module1 == 0 and correct_math_module2 == 0:
        math_score = 200
        
        
    elif (15 <= correct_math_module1 <= 22) or (8 <= correct_math_module1 <= 12):
        if (correct_math_module1 == 17 and correct_math_module2 == 0) or (correct_math_module1 == 16 and correct_math_module2 == 1) or (correct_math_module1 == 15 and correct_math_module2 == 2):
            math_score = 390
        elif (correct_math_module1 == 16 and correct_math_module2 == 0) or (correct_math_module1 == 15 and correct_math_module2 == 1):
            math_score = 380
        elif correct_math_module1 == 15 and correct_math_module2 == 0:
            math_score = 360
        else:
            math_score = math_score1(correct_math_module1, correct_math_module2)
        
        
    elif 13 <= correct_math_module1 <= 14:
        if (correct_math_module1 == 14 and correct_math_module2 == 2):
            math_score = 380
        elif (correct_math_module1 == 14 and correct_math_module2 == 1) or (correct_math_module1 == 13 and correct_math_module2 == 2):
            math_score = 360
        elif (correct_math_module1 == 14 and correct_math_module2 == 0) or (correct_math_module1 == 13 and correct_math_module2 in [0, 1]):
            math_score = 350
        elif (correct_math_module1 == 7 and correct_math_module2 in [2, 3]):
            math_score = 300
        elif (correct_math_module1 == 7 and correct_math_module2 == 1) or (correct_math_module1 == 6 and correct_math_module2 == 2):
            math_score = 270
        elif (correct_math_module1 == 7 and correct_math_module2 == 0) or (correct_math_module1 == 6 and correct_math_module2 == 1) or (correct_math_module1 == 5 and correct_math_module2 == 2):
            math_score = 240
        elif (correct_math_module1 == 6 and correct_math_module2 == 0) or (correct_math_module1 == 5 and correct_math_module2 == 1) or (correct_math_module1 == 4 and correct_math_module2 == 2):
            math_score = 210
        elif (correct_math_module1 == 5 and correct_math_module2 == 0) or (correct_math_module1 == 4 and correct_math_module2 in [0, 1]) or (correct_math_module1 == 3 and correct_math_module2 <= 3) or (correct_math_module1 == 2 and correct_math_module2 <= 4) or (correct_math_module1 == 1 and correct_math_module2 <= 5):
            math_score = 200
        else:
            math_score = math_score2(correct_math_module1, correct_math_module2)
        
        
    if math_score > 800:
        math_score = 800
    elif math_score < 200:
        math_score = 200
#print(math_score)



    english1_score = db.calculate_score(user_test_id,"Verbal","1")
    english2_score = db.calculate_score(user_test_id,"Verbal","2")
    print(english1_score)
    print(english2_score)
    
    correct_verbal_module1 = english1_score
    correct_verbal_module2 = english2_score
    verbal_score = 0

    if correct_verbal_module1 == 27 and correct_verbal_module2 == 27:
        verbal_score = 800
    elif correct_verbal_module1 == 0 and correct_verbal_module2 == 0:
        verbal_score = 200

    elif (18 <= correct_verbal_module1 <= 27):
        if (correct_verbal_module1 == 27 and correct_verbal_module2 == 26) or (correct_verbal_module1 == 26 and correct_verbal_module2 == 27):
            verbal_score = 780
        elif (correct_verbal_module1 == 27 and correct_verbal_module2 == 25) or (correct_verbal_module1 == 26 and correct_verbal_module2 == 26) or (correct_verbal_module1 == 25 and correct_verbal_module2 == 27):
            verbal_score = 760
        elif (correct_verbal_module1 == 21 and correct_verbal_module2 == 0):
            verbal_score = 430
        else:
            verbal_score = verbal_score1(correct_verbal_module1, correct_verbal_module2)

    elif (1 <= correct_verbal_module1 <= 17):
        if (correct_verbal_module1 in [1, 2, 3, 4, 5, 6, 7, 8, 17] and 15 <= correct_verbal_module2 <= 27):
            verbal_score = verbal_score2(correct_verbal_module1, correct_verbal_module2)
        elif (correct_verbal_module1 == 17 and correct_verbal_module2 <= 12) or (correct_verbal_module1 == 16 and 1 <= correct_verbal_module2 <= 11) or (correct_verbal_module1 == 15 and 1 <= correct_verbal_module2 <= 12) or (correct_verbal_module1 == 9 and 4 <= correct_verbal_module2 <= 11):
            verbal_score = verbal_score3(correct_verbal_module1, correct_verbal_module2)
        elif (correct_verbal_module1 in [12, 13, 14] and correct_verbal_module2 <= 14) or (correct_verbal_module1 == 11 and 1 <= correct_verbal_module2 <= 14) or (correct_verbal_module1 == 10 and 2 <= correct_verbal_module2 <= 14):
            verbal_score = verbal_score4(correct_verbal_module1, correct_verbal_module2)
        elif (correct_verbal_module1 in [3, 4, 5, 6, 7, 8] and correct_verbal_module2 <= 14):
            verbal_score = verbal_score5(correct_verbal_module1, correct_verbal_module2)
        elif (correct_verbal_module1 in [1, 2] and correct_verbal_module2 <= 14):
            verbal_score = verbal_score6(correct_verbal_module1, correct_verbal_module2)
        elif (correct_verbal_module1 == 17 and correct_verbal_module2 == 14):
            verbal_score = 490
        elif (correct_verbal_module1 == 17 and correct_verbal_module2 == 13) or (correct_verbal_module1 == 16 and correct_verbal_module2 == 14):
            verbal_score = 480
        elif (correct_verbal_module1 == 16 and correct_verbal_module2 in [12,13]) or (correct_verbal_module1 == 15 and correct_verbal_module2 in [13,14]):
            verbal_score = 470
        elif (correct_verbal_module1 == 16 and correct_verbal_module2 == 0):
            verbal_score = 380
        elif (correct_verbal_module1 == 15 and correct_verbal_module2 == 0):
            verbal_score = 360
        elif (correct_verbal_module1 == 11 and correct_verbal_module2 == 0) or (correct_verbal_module1 == 10 and correct_verbal_module2 == 1) or (correct_verbal_module1 == 9 and correct_verbal_module2 in [2, 3]):
            verbal_score = 270
        elif (correct_verbal_module1 == 10 and correct_verbal_module2 == 0) or (correct_verbal_module1 == 9 and correct_verbal_module2 == 1):
            verbal_score = 260
        elif (correct_verbal_module1 == 9 and correct_verbal_module2 == 0):
            verbal_score = 250



    if verbal_score > 800:
        verbal_score = 800
    elif verbal_score < 200:
        verbal_score = 200
    print(verbal_score)




















    total_score = math_score + verbal_score
    












    print("Verbal" + str(verbal_score))
    db.update_score(user_test_id,verbal_score,"Verbal")
    print("Math" + str(sat_math))
    db.update_score(user_test_id,math_score,"Math")
    print("Math" + str(total_score))
    db.update_score(user_test_id,total_score,"Total")
    db.update_end_time(user_test_id)
    return render_template('score.html',Total = total_score,Math = int(math_score),Verbal = int(verbal_score))


@app.route('/logout')
def logout():
    #Delet session
    session.pop('user_id', None)
    session.pop('gmail', None)
    session.clear()
    return redirect(url_for('home'))

def sat_math(correct_Mathmodule1,correct_Mathmodule2):
    if correct_Mathmodule1  == 22 and correct_Mathmodule2  == 22:
        math_score = 800
    elif correct_Mathmodule1  == 0 and correct_Mathmodule2  == 0:
        math_score = 200

    if 15 <= correct_Mathmodule1  <= 22 or 8 > correct_Mathmodule1 <= 12:

        math_score = round(92.294772 + 16.293996 * correct_Mathmodule1  + 16.287055 * correct_Mathmodule2  / 10 * 10)

        if correct_Mathmodule2  == 0:
            if correct_Mathmodule1  == 17:
                math_score = 390
            if correct_Mathmodule1  == 16:
                math_score = 380
            elif correct_Mathmodule1  == 15:
                math_score = 360
            elif correct_Mathmodule1  in [13, 14]:
                math_score = 350

        if correct_Mathmodule2  == 1:
            if correct_Mathmodule1  == 16:
                math_score = 390
            elif correct_Mathmodule1  == 15:
                math_score = 380
            elif correct_Mathmodule1  == 14:
                math_score = 360
            elif correct_Mathmodule1  == 13:
                math_score = 350

        if correct_Mathmodule2  == 2:
            if correct_Mathmodule1  == 15:
                math_score = 390
            elif correct_Mathmodule1  == 14:
                math_score = 380
            elif correct_Mathmodule1  == 14:
                math_score = 360

        if math_score > 800:
            math_score = 800

        elif math_score < 200:
            math_score = 200

    elif 1 <= correct_Mathmodule1  <= 7 or correct_Mathmodule1  in [13, 14]:
        
        math_score = round(147.01087 + 13.913043 * correct_Mathmodule1  + 11.497036 * correct_Mathmodule2  / 10 * 10)
            
        if correct_Mathmodule2  == 0:
            if correct_Mathmodule1  in [13, 14]:
                math_score = 350
            elif correct_Mathmodule1  == 7:
                math_score = 240
            elif correct_Mathmodule1  == 6:
                math_score = 270
            elif correct_Mathmodule1  in [4, 5]:
                math_score = 200
            elif correct_Mathmodule1  in [2, 3]:
                math_score = 200

        elif correct_Mathmodule2  == 1:
            if correct_Mathmodule1  == 14:
                math_score = 360
            elif correct_Mathmodule1  == 13:
                math_score = 350
            elif correct_Mathmodule1  == 7:
                math_score = 270
            elif correct_Mathmodule1  == 6:
                math_score = 240
            elif correct_Mathmodule1  == 5:
                math_score = 210
            elif correct_Mathmodule1  == 4:
                math_score = 200
            elif correct_Mathmodule1  in [2, 3]:
                math_score = 200

        elif correct_Mathmodule2  == 2:
            if correct_Mathmodule1  == 14:
                math_score = 380
            elif correct_Mathmodule1  == 13:
                math_score = 360
            elif correct_Mathmodule1  == 7:
                math_score = 300
            elif correct_Mathmodule1  == 6:
                math_score = 270
            elif correct_Mathmodule1  == 5:
                math_score = 240
            elif correct_Mathmodule1  == 4:
                math_score = 210
            elif correct_Mathmodule1  in [2, 3]:
                math_score = 200

        elif correct_Mathmodule2  == 3:
            if correct_Mathmodule1  == 7:
                math_score = 300
            elif correct_Mathmodule1  == 3:
                math_score = 200
    return int(round(math_score))


def sat_verbal(correct_Verbalmodule1,correct_Verbalmodule2):
    if correct_Verbalmodule1 == 27 and correct_Verbalmodule2 == 27:
        verbal_score = 800
    elif correct_Verbalmodule1 == 0 and correct_Verbalmodule2 == 7:
        verbal_score = 200

    if 18 <= correct_Verbalmodule1 <= 27:
        verbal_score = round(197.943686 + 10.487013 * correct_Verbalmodule1 + 10.226875 * correct_Verbalmodule2) / 10 * 10 

        if correct_Verbalmodule1 == 27:
            if correct_Verbalmodule2 == 26:
                verbal_score = 780
            if correct_Verbalmodule2 == 25:
                verbal_score = 760

        if correct_Verbalmodule1 == 26:
            if correct_Verbalmodule2 == 27:
                verbal_score = 780
            if correct_Verbalmodule2 == 26:
                verbal_score = 760

        if correct_Verbalmodule1 == 25:
            if correct_Verbalmodule2 == 27:
                verbal_score = 760

        if correct_Verbalmodule1 == 21:
            if correct_Verbalmodule2 == 0:
                verbal_score = 430

    elif 1 <= correct_Verbalmodule1 <= 17:
        if 15 <= correct_Verbalmodule2 <= 27:
            verbal_score = round(212.958145 + 9.862368 * correct_Verbalmodule1  + 8.002586 * correct_Verbalmodule2) / 10 * 10
            
        elif 0 <= correct_Verbalmodule2 <= 14:
            
            if (correct_Verbalmodule1 == 17  and 0 <= correct_Verbalmodule2 <= 12) or (correct_Verbalmodule1 == 16  and 1 <= correct_Verbalmodule2 <= 11) or (correct_Verbalmodule1 == 15  and 1 <= correct_Verbalmodule2 <= 12) or (correct_Verbalmodule1 == 9  and 4 <= correct_Verbalmodule2 <= 14) :
                verbal_score = round(145.558206 + 13.488566 *correct_Verbalmodule1  + 10.258174 * correct_Verbalmodule2) / 10 * 10
            
            if correct_Verbalmodule1 == 17:
                if correct_Verbalmodule2 == 14:
                    verbal_score = 490
                elif correct_Verbalmodule2 == 13:
                    verbal_score = 480

            if correct_Verbalmodule1 == 16:
                if correct_Verbalmodule2 == 14:
                    verbal_score = 480
                elif correct_Verbalmodule2 in [12, 13]:
                    verbal_score = 470
                elif correct_Verbalmodule2 == 0:
                    verbal_score = 380

            if correct_Verbalmodule1 == 15:
                if correct_Verbalmodule2 in [13, 14]:
                    verbal_score = 470
                elif correct_Verbalmodule2 == 0:
                    verbal_score = 360

            if correct_Verbalmodule1 == 9:
                if correct_Verbalmodule2 in [2, 3]:
                    verbal_score = 270
                elif correct_Verbalmodule2 == 1:
                    verbal_score = 260
                elif correct_Verbalmodule2 == 0:
                    verbal_score = 250

            if (correct_Verbalmodule1 in [12, 13, 14] and 0 <= correct_Verbalmodule2 <= 14) or (correct_Verbalmodule1 == 11 and 0 <= correct_Verbalmodule2 <= 14) or (correct_Verbalmodule1 == 10 and 2 <= correct_Verbalmodule2 <= 14):
                verbal_score = round(162.6 + 12.933333 * correct_Verbalmodule1 + 9.4 *correct_Verbalmodule2 ) / 10 * 10

            if correct_Verbalmodule1 == 11:
                if correct_Verbalmodule2 == 0:
                    verbal_score = 270

            if correct_Verbalmodule1 == 10:
                if correct_Verbalmodule2 == 1:
                    verbal_score = 270
                elif correct_Verbalmodule2 == 0:
                    verbal_score = 260

            if (3 <= correct_Verbalmodule1 <= 8 and 0 <= correct_Verbalmodule2  <= 14):
                verbal_score = round(120.591667 + 14.6 * correct_Verbalmodule1  + 12.696429 * correct_Verbalmodule2) / 10 * 10
        
            if (1 <= correct_Verbalmodule1 <= 2 and 0 <= correct_Verbalmodule2 <= 14):
                verbal_score = round(181.115242 + 7.835369 * correct_Verbalmodule2) / 10 * 10


    if verbal_score > 800:
        verbal_score = 800
    elif verbal_score < 200:
        verbal_score = 200
    return int(round(verbal_score))


def verbal_score1(correct_verbal_module1, correct_verbal_module2):
	return int(round(197.943686 + 10.487013 * correct_verbal_module1 + 10.226875 * correct_verbal_module2) / 10) * 10
def verbal_score2(correct_verbal_module1, correct_verbal_module2):
	return int(round(212.958145 + 9.862368 * correct_verbal_module1  + 8.002586 * correct_verbal_module2) / 10) * 10
def verbal_score3(correct_verbal_module1, correct_verbal_module2):
	return int(round(145.558206 + 13.488566 *correct_verbal_module1  + 10.258174 * correct_verbal_module2) / 10) * 10
def verbal_score4(correct_verbal_module1, correct_verbal_module2):
	return int(round(162.6 + 12.933333 * correct_verbal_module1 + 9.4 *correct_verbal_module2 ) / 10) * 10
def verbal_score5(correct_verbal_module1, correct_verbal_module2):
	return int(round(120.591667 + 14.6 * correct_verbal_module1  + 12.696429 * correct_verbal_module2) / 10) * 10
def verbal_score6(correct_verbal_module1, correct_verbal_module2):
	return int(round(181.115242 + 7.835369 * correct_verbal_module2) / 10) * 10
def math_score1(correct_math_module1, correct_math_module2):
	return int(round(92.294772 + 16.293996 * correct_math_module1 + 16.287055 * correct_math_module2) / 10) * 10

def math_score2(correct_math_module1, correct_math_module2):

	return int(round(147.01087 + 13.913043 * correct_math_module1 + 11.497036 * correct_math_module2) / 10) * 10