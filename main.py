from setup import _initial_setup,_connect_
import mysql.connector as myc
import random
from texttable import Texttable
_initial_setup()

def getleaderboardpos(passkey):
    con,cur = _connect_(True)
    cur.execute("SELECT * FROM leaderboard ORDER BY ratio DESC")
    _lb = cur.fetchall()
    total = 0
    pos = 0
    for w in _lb:
        total+=1
        if w[4] == passkey:
            pos += total
    con.close()
    return total,pos

def runquiz(num, passkey):
    con,cur = _connect_(True)
    cur.execute("SELECT * FROM questions")
    _obj = cur.fetchall()
    print("➖➖➖➖➖➖➖➖➖➖➖➖➖➖")
    print('Quiz trivia started. To cancel game just type cancel as the answer.\n')
    cur.execute("SELECT qnsattempted,qnscorrect FROM leaderboard WHERE passkey = %s", (passkey,))
    eh = cur.fetchall()[0]
    qnsattempted_ = eh[0]
    qnscorrect = eh[1]
    for e in range(num):
        question = random.choice(_obj)
        _obj.remove(question)
        questn = question[0]
        options = question[1].split('|')
        ansindex = question[2]
        ans = options[ansindex]
        print(f'Qn {e+1}. {questn}')
        for x in range(len(options)):
            print(f'Option {x+1}: {options[x]}')
        answe = int(input("Select the correct option: "))-1
        if answe == ansindex:
            print("Correct answer! ✅")
            print("➖➖➖➖➖➖➖➖➖➖➖➖➖➖")
            qnsattempted_+=1
            qnscorrect+=1
            cur.execute("UPDATE leaderboard SET qnsattempted=qnsattempted+1,qnscorrect=qnscorrect+1 WHERE passkey = %s", (passkey,))
            continue
        else:
            qnsattempted_+=1
            print(f"Wrong answer ❌. The correct answer is {ans}")
            print("➖➖➖➖➖➖➖➖➖➖➖➖➖➖")
            cur.execute("UPDATE leaderboard SET qnsattempted=qnsattempted+1 WHERE passkey = %s", (passkey,))
            continue
    cur.execute("UPDATE leaderboard SET ratio = %s WHERE passkey = %s", ((qnscorrect/qnsattempted_)*100, passkey))
    con.commit()
    con.close()
    hehehe = input("You have finished your quiz. Do you want to run the program again? (Y/N): ").lower()
    if hehehe == 'y':
        _main_()
    
    
    



def startgame(passky):
    print("➖➖➖➖➖➖➖➖➖➖➖➖➖➖")
    con,cur = _connect_(True)
    cur.execute("SELECT * FROM leaderboard WHERE passkey = %s", (passky,))
    acc = cur.fetchall()[0]
    _accname = acc[0]
    _qnattended = acc[2]
    qnscorrect = acc[1]
    ratio = acc[3]
    if ratio>=90:
        _ratioprompt = 'Very Good'
    elif ratio>=80:
        _ratioprompt = 'Good'
    elif ratio>=60:
        _ratioprompt = 'Fine'
    elif ratio>=40:
        _ratioprompt = 'Not so good'
    else:
        _ratioprompt = 'Very bad'
    print(f"Hello, you are now logged in as {_accname}! 🎉")
    print("""Please select an option below.
1. Start a new quiz.
2. See your stats.
3. Delete your account.
4. Exit Program.""")
    while True:
        cheh = input("Enter your choice: ")
        if not cheh in ['1', '2', '3', '4']:
            print("Invalid input, please input either 1, 2, 3 or 4.")
            continue
        if cheh == '1':
            numqn = int(input("How many questions do you want to attend?: "))
            print(f'Okay so {numqn} questions. I\'m ready when you\'re ready!')
            while True:
                strt = input(f"Can we start the game, {_accname}? (Y/N): ").lower()
                if not strt in ['y','n']:
                    print("Invalid input, please input either Y or N.")
                    continue
                if strt == 'n':
                    e = input("Do you want to cancel the game? (Y/N): ").lower()
                    if not e in ['y','n']:
                        print("Invalid input, please input either Y or N.")
                        continue
                    if e == "y":
                        print("Game cancelled.")
                        print("""
Please select an option below.
1. Start a new quiz.
2. See your stats.
3. Delete your account.
4. Exit Program.""")
                        break
                    continue
                con.close()
                runquiz(numqn, passky)
                return
        elif cheh == '2':
            total,pos_ = getleaderboardpos(passky)
            print("➖➖➖➖➖➖➖➖➖➖➖➖➖➖")
            print(
                f"""- You have attended a total of {_qnattended} questions! 👍
- Of which for {qnscorrect} questions you gave the correct answer. ✅
- Your overall performance ratio is {ratio}. Which is {_ratioprompt}! ✋
- Your position in the leaderboard is {pos_} out of {total} players! 🙌
Please note that your performance ratio determines your position in the leaderboard."""
            )
            con.close()
            return
        elif cheh == '3':
            if passky == 'nigga':
                print("Nice try. Get a life bro.")
                return
            chwh = input("Are you sure you want to delete your account? (Y/N): ").lower()
            if chwh == 'n':
                print("Action cancelled.")
                return
            cur.execute("DELETE FROM leaderboard WHERE passkey = %s", (passky,))
            con.commit()
            print("Your account has been deleted from the database.")
            return
        elif cheh == '4':
            con.close()
            print("Good byee!")
            return


def _main_():
    print(
"""Welcome to python quiz! 🙂
If you are new, please create an account for leaderboard.
If you already have an account please login with your passkey.\n"""
    )
    print("1. Login to an existing account.\n2. Create an account.\n3. Exit program.")
    while True:
        ch = input("Enter your choice: ")
        if not ch in ['1','2','3']:
            print("Incorrect Choice, Please input either 1 or 2.")
            continue
        con,cur = _connect_(True)
        if ch == '1':
            passkey_ = input("Enter your passkey to continue: ")
            cur.execute("SELECT * FROM leaderboard WHERE passkey = %s", (passkey_,))
            acc = cur.fetchall()
            if acc == []:
                print("There is no account associated with that passkey ❌")
                continue
            con.close()
            startgame(passkey_)
            return
        elif ch == '2':
            name_ = input("Enter your name: ")
            while True:
                passkey_ = input("Please create a passkey: ")
                try:
                    cur.execute("INSERT INTO leaderboard VALUES (%s,%s,%s,%s,%s)", (name_,0,0,0,passkey_))
                    con.commit()
                    print("Your account has been created successfully! ✅")
                    #ch = input("Do you want to start the quiz? (Y/N): ").lower()
                    #if ch == 'y':
                    con.close()
                    startgame(passkey_)
                    return
                except myc.IntegrityError as e:
                    print("That passkey already exist for another account. Please try again with a different passkey.")
                    continue
        elif ch == '3':
            con.close()
            return


_main_()