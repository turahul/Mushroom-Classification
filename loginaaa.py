import streamlit as st
import pandas as pd


# Import Libraries 
from plantcv import plantcv as pcv
import matplotlib
import streamlit as st

from PIL import Image

class options:
    def __init__(self):
        self.image = "download.jpg"
        self.debug = "plot"
        self.writeimg= False
        self.result = "."
        self.outdir = "." # Store the output to the current directory
        
# Get options
args = options()

# Set debug to the global parameter 
pcv.params.debug = args.debug


# DB Management
import sqlite3 
conn = sqlite3.connect('data.db')
c = conn.cursor()


# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False






def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data


def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data



def main():
	"""Simple Login App"""

	st.title("Plant Phenotyping")

	menu = ["Home","Login","SignUp"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Home":
		st.subheader("Home")

	elif choice == "Login":
		st.subheader("Login Section")

		username = st.sidebar.text_input("User Name")
		password = st.sidebar.text_input("Password",type='password')
		if st.sidebar.checkbox("Login"):
			# if password == '12345':
			create_usertable()
			hashed_pswd = make_hashes(password)

			result = login_user(username,check_hashes(password,hashed_pswd))
			if result:

				st.success("Logged In as {}".format(username))

				
				uploaded_file = st.file_uploader("Choose an image...", type="jpg")
				if uploaded_file is not None:
					inp = Image.open(uploaded_file)
					inp.save('input.jpg')
					img, path, filename = pcv.readimage(filename='input.jpg')
					image = Image.open('input.jpg')
					st.image(image, caption='Original Image',use_column_width=True)
                    # Convert RGB to HSV and extract the saturation channel
    # Inputs:
    #   rgb_image - RGB image data 
    #   channel - Split by 'h' (hue), 's' (saturation), or 'v' (value) channel
					
					s = pcv.rgb2gray_hsv(rgb_img=img, channel='s')
					pcv.print_image(s, "plant/rgbtohsv.png")
					image = Image.open('plant/rgbtohsv.png')
					st.image(image, caption='RGB to HSV', use_column_width=True)
                    
                   
    


                    
                    
                    
					
			else:
				st.warning("Incorrect Username/Password")





	elif choice == "SignUp":
		st.subheader("Create New Account")
		new_user = st.text_input("Username")
		new_password = st.text_input("Password",type='password')

		if st.button("Signup"):
			create_usertable()
			add_userdata(new_user,make_hashes(new_password))
			st.success("You have successfully created a valid Account")
			st.info("Go to Login Menu to login")








if __name__ == '__main__':
	main()