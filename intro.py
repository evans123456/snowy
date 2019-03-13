import sqlite3
import json
import re
import os
from datetime import datetime
import time

# path = './conversations/psychology.yml'
sql_transaction = []
connection = sqlite3.connect('conversations.db')
c = connection.cursor()
global my_name,my_gender


def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper


@run_once
def introduction():
	

	print(my_name + ': Before we begin i will give you a quick introduction')
	time.sleep(2)
	print(my_name + ': Everything you tell me is private and stored securely')
	time.sleep(2)
	print(my_name + ': I will check-up on you daily to ask about your thoughts,feelings and your environment')
	time.sleep(2)
	print(my_name + ': This is not a crisis service or a replacement of a human')
	time.sleep(2)
	print(my_name + ': Conversations will be started by the user inform of greetings and then terminated by the frase "bye"')
	time.sleep(2)
	print(my_name + ': I am a self-help tool and im not intended to be a medical replacement')
	print(my_name + ': Are we clear?(reply with yes/no)')
	are_we_clear = input('You: ')
	if are_we_clear.lower() == 'yes':
		print(my_name + ': Great, lets get started')
		conversation()
	else:
		introduction()
	
def chatbot():
	global my_name 
	global my_gender 
	my_name = input('What name would you like to give me? ')# name will be displayed on chat
	my_gender = input('What gender would you like to give me? ')

# def check_message(): 
# 	while True:
# 		message = input('You: ')
# 		if message.strip() != 'Bye':
# 			reply = bot.get_response(message)
# 			print('ChatBot: ',reply)
# 		else:
# 			print('ChatBot: Bye')
# 			break

def get_response(message): #need to do the pairing of parent child
	
	print(message)
	message = '  - '+message
	print(message)

	v = c.execute('''  SELECT * FROM converse WHERE comment LIKE '{}%';  '''.format(message))
	rows = v.fetchall()
	print(rows)


def transaction_bldr(sql):
    global sql_transaction 
    sql_transaction.append(sql) #to create a bulk sql statement
    if len(sql_transaction) > 10:
        c.execute('BEGIN TRANSACTION')
        for s in sql_transaction:
            try:
                c.execute(s)
            except:
                pass
        connection.commit()
        sql_transaction = []

def create_table():
	c.execute("""CREATE TABLE IF NOT EXISTS converse (parent_id INT PRIMARY KEY, comment_id INT, parent TEXT,comment TEXT) """)
	print('-----DATABASE CREATED SUCCESSFULL-------')


def read_folder():
	for filename in os.listdir('./conversations/'):
		path = './conversations/'+ filename
		insert_data(path)
	
def insert_data(path):
	i = 0
	file = open(path, "r")
	for line in file:
		i += 1
		
		x = re.findall(r"(\A- - [A-Za-z])", line)

		if (x):
			print("Yes, there is a match!")
			print(line)
			sql = """ INSERT INTO converse ( parent ) VALUES ("{}"); """.format(line) 
			transaction_bldr(sql)
			print('inserted')
		else:
			print("No match")
			print(line)
			sql = """ INSERT INTO converse ( comment ) VALUES ("{}"); """.format(line) 
			transaction_bldr(sql)
			print('inserted')


def conversation():
	while True:
		message = input('You: ')
		if message.strip() != 'Bye':
			reply = get_response(message)
			print(my_name+ ": " + reply)
		else:
			print(my_name+": Bye, Have a good day")
			break

if __name__ == "__main__":
	# create_table()
	# read_folder()
	chatbot()
	introduction()
	
	# insert_data()
	pass