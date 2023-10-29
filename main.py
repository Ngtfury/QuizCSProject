import setup
import mysql.connector as myc
setup._initial_setup()

def startgame(acc):
    print(acc)
    _accname = acc[0]
    _qnattended = acc[1]
    qnscorrect = acc[2]
    ratio = acc[3]
    passky = acc[4]
    

def welcomemessage():
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
        con,cur = setup._connect_(True)
        if ch == '1':
            passkey_ = input("Enter your passkey to continue: ")
            cur.execute("SELECT * FROM leaderboard WHERE passkey = %s", (passkey_,))
            acc = cur.fetchall()
            if acc == []:
                print("There is no account associated with that passkey ❌")
                continue
            startgame(acc[0])
            break
        elif ch == '2':
            name_ = input("Enter your name: ")
            while True:
                passkey_ = input("Please create a passkey: ")
                try:
                    cur.execute("INSERT INTO leaderboard VALUES (%s,%s,%s,%s,%s)", (name_,0,0,0,passkey_))
                    con.commit()
                    print("Your account has been created successfully! ✅")
                    ch = input("Do you want to start the quiz? (Y/N)").lower()
                    if ch == 'y':
                        startgame((name_,0,0,passkey_))
                        break
                except myc.IntegrityError as e:
                    print("That passkey already exist for another account. Please try again with a different passkey.")
                    continue
        elif ch == '3':
            break

def _main_():
    ...

welcomemessage()