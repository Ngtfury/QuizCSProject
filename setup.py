import mysql.connector as myc

def _connect_():
    try:
        con = myc.connect(
        host='localhost',
        user='root',
        password='sreehari'
    )
        cur = con.cursor()
        return con,cur
    except myc.Error as e:
        print('[Error]:',e.msg)
    
con,cur = _connect_()

def _execbulk(query,data=None):
    if not '\n' in query:
        return cur.execute(query,data) if data else cur.execute(query)
    splt = query.split('\n')
    for w in splt:
        try:
            cur.execute(w)
        except myc.Error as e:
            print('[Error]: ',e.msg)

def _initial_setup():
    try:
        cur.execute("CREATE DATABASE quizproject")
    except myc.DatabaseError as e:
        if e.msg == "Can't create database 'quizproject'; database exists":
            return print("[INFO]: Initial setup was already done before.")
        print(e.msg)
    
    _execbulk("""USE quizproject
              CREATE TABLE questions (qn varchar(60), options int, ans varchar(1))
              CREATE TABLE leaderboard (name varchar(40), qnscorrect int, qnsattempted int, ratio FLOAT, passkey varchar(5))""")
    print("[INFO]: Initial setup has finished.")
_initial_setup()
    
