import mysql.connector as myc

QUESTIONS = [
    ['What is a correct syntax to output "Hello World" in Python?',"Print('Hello World')|print('Hello World')|display('Hello World')",1],
    ['How do you insert COMMENTS in Python code?','$This is a comment|//This is a comment|#This is a comment',2],
    ['Which one is NOT an allowed variable name?','my-var|my_var|myvar',0],
    ['How do you create a variable with the numeric value 5?',"x=5|x=int('5')|Both a and b",2],
    ['Which method can be used to return a string in upper case letters?',"uppercase()|toupper()|upper()",2],
    ['Which SQL statement is used to delete data from a database?',"REMOVE|COLLAPSE|DELETE",2],
    ['Which SQL statement is used to return only different values?',"SELECT UNIQUE|SELECT DISTINCT|SELECT DIFFERENT", 1],
    ['Which SQL keyword is used to sort the result-set?', "ORDER BY|ORDER|SORT BY", 0],
    ['With SQL, how can you insert a new record into the "Persons" table?',"INSERT VALUES ('Ajay Paul', 'Paulose') INTO Persons|INSERT ('Ajay Paul', 'Paulose') INTO Persons|INSERT INTO Persons VALUES('Ajay Paul', 'Paulose')",2]
]

def _connect_(db=False):
    try:
        if not db:
            con = myc.connect(
            host='localhost',
            user='root',
            password='sreehari'
        )
        else:
            con = myc.connect(
                host = 'localhost',
                user='root',
                password = 'sreehari',
                database='quizproject'
            )
        cur = con.cursor()
        return con,cur
    except myc.Error as e:
        print('[Error]:',e.msg)


def _execbulk(query,cur,data=None):
    
    if not '\n' in query:
        return cur.execute(query,data) if data else cur.execute(query)
    splt = query.split('\n')
    for w in splt:
        try:
            cur.execute(w)
        except myc.Error as e:
            print('[Error]: ',e.msg)

def _insertqns(con,cur):
    print('[Info]: Inserting questions data.')
    for question in QUESTIONS:
        cur.execute("INSERT INTO questions VALUES (%s, %s, %s)", (question[0], question[1], question[2]))
    cur.execute("INSERT INTO leaderboard VALUES (%s, %s, %s, %s, %s)", ('Sreeramachandran S Menon (admin)',100,100,100,'nigga'))
    con.commit()
    print("[Info]: All the data has been inserted.")

def _initial_setup():
    con,cur = _connect_()
    try:
        cur.execute("CREATE DATABASE quizproject")
    except myc.DatabaseError as e:
        if e.msg == "Can't create database 'quizproject'; database exists":
            print("[INFO]: Initial setup was already done before.")
            return print("➖➖➖➖➖➖➖➖➖➖➖➖➖➖")
        print(e.msg)
    
    _execbulk("""USE quizproject
              CREATE TABLE questions (qn varchar(200), options varchar(200), ansindex int)
              CREATE TABLE leaderboard (name varchar(40), qnscorrect int, qnsattempted int, ratio FLOAT, passkey varchar(5) PRIMARY KEY)""",
              cur)
    print("[INFO]: Initial setup has finished.")
    _insertqns(con,cur)
    print("➖➖➖➖➖➖➖➖➖➖➖➖➖➖")
    con.close()