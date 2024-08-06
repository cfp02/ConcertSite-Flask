import sqlite3

def alter_database():
    conn = sqlite3.connect('instance/concert_mailer.sqlite')
    cursor = conn.cursor()

    # Put some commands here
    '''
    '''
    # cursor.execute("ALTER TABLE venue ADD COLUMN venue_email_text TEXT")

    

    conn.commit()
    conn.close()

if __name__ == "__main__":
    alter_database()
