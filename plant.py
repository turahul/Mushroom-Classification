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
		st.markdown("What is Plant Phenotype ?")        
		st.write("Plant phenotyping is an emerging science that links genomics with plant ecophysiology and agronomy. The functional plant body (PHENOTYPE) is formed during plant growth and development from the dynamic interaction between the genetic background (GENOTYPE) and the physical world in which plants develop (ENVIRONMENT). These interactions determine plant performance and productivity measured as accumulated biomass and commercial yield and resource use efficiency. The full array of plant science from molecular to field scale must be integrated to develop strategies for a sustainable plant. The progress in molecular and genetic tools for plant breeding was significant in recent years, but a quantitative analysis of the actual plant traits (e.g. grain weight or pathogen resistance), i.e. PHENOTYPING, was limited by a lack of efficient techniques. Network structured approaches were initiated to close the gap between laboratory studies and field application by developing technological solutions for this problem.")
		image = Image.open('plant/home.png')
		st.image(image, caption='Plant Phenotype',use_column_width=True)
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
                

				pla_rad = st.radio("Select the Part",('Shoot Part', 'Root Part'))
                
				if pla_rad == 'Shoot Part':
					root()
				if pla_rad == 'Root Part':
					root()
                

    
    

					
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


def shoot():
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
    					s_thresh = pcv.threshold.binary(gray_img=s, threshold=85, max_value=255, object_type='light')
    					pcv.print_image(s_thresh, "plant/binary_threshold.png")
    					image = Image.open('plant/binary_threshold.png')
    					st.image(image, caption='Binary Threshold',use_column_width=True)
                   
    # Median Blur to clean noise 

    # Inputs: 
    #   gray_img - Grayscale image data 
    #   ksize - Kernel size (integer or tuple), (ksize, ksize) box if integer input,
    #           (n, m) box if tuple input 

    					s_mblur = pcv.median_blur(gray_img=s_thresh, ksize=5)
    					pcv.print_image(s_mblur, "plant/Median_blur.png")
    					image = Image.open('plant/Median_blur.png')
    					st.image(image, caption='Median Blur',use_column_width=True)
                    
     # An alternative to using median_blur is gaussian_blur, which applies 
    # a gaussian blur filter to the image. Depending on the image, one 
    # technique may be more effective than others. 

    # Inputs:
    #   img - RGB or grayscale image data
    #   ksize - Tuple of kernel size
    #   sigma_x - Standard deviation in X direction; if 0 (default), 
    #            calculated from kernel size
    #   sigma_y - Standard deviation in Y direction; if sigmaY is 
    #            None (default), sigmaY is taken to equal sigmaX
                
    					gaussian_img = pcv.gaussian_blur(img=s_thresh, ksize=(5, 5), sigma_x=0, sigma_y=None)
    # Convert RGB to LAB and extract the blue channel ('b')

    # Input:
    #   rgb_img - RGB image data 
    #   channel- Split by 'l' (lightness), 'a' (green-magenta), or 'b' (blue-yellow) channel
    					b = pcv.rgb2gray_lab(rgb_img=img, channel='b')
    					b_thresh = pcv.threshold.binary(gray_img=b, threshold=160, max_value=255, 
                                object_type='light')
                     # Join the threshold saturation and blue-yellow images with a logical or operation 

    # Inputs: 
    #   bin_img1 - Binary image data to be compared to bin_img2
    #   bin_img2 - Binary image data to be compared to bin_img1

    
    					bs = pcv.logical_or(bin_img1=s_mblur, bin_img2=b_thresh)
    					pcv.print_image(bs, "plant/threshold comparison.png")
    					image = Image.open('plant/threshold comparison.png')
    					st.image(image, caption='Threshold Comparision',use_column_width=True)
                    
 # Appy Mask (for VIS images, mask_color='white')

    # Inputs:
    #   img - RGB or grayscale image data 
    #   mask - Binary mask image data 
    #   mask_color - 'white' or 'black' 
    
    					masked = pcv.apply_mask(img=img, mask=bs, mask_color='white')
    					pcv.print_image(masked, "plant/Apply_mask.png")
    					image = Image.open('plant/Apply_mask.png')
    					st.image(image, caption='Applied Mask',use_column_width=True)
                   # Convert RGB to LAB and extract the Green-Magenta and Blue-Yellow channels
    					masked_a = pcv.rgb2gray_lab(rgb_img=masked, channel='a')
    					masked_b = pcv.rgb2gray_lab(rgb_img=masked, channel='b')
                     # Threshold the green-magenta and blue images
    					maskeda_thresh = pcv.threshold.binary(gray_img=masked_a, threshold=115, max_value=255, object_type='dark')
    					maskeda_thresh1 = pcv.threshold.binary(gray_img=masked_a, threshold=135,max_value=255, object_type='light')
    					maskedb_thresh = pcv.threshold.binary(gray_img=masked_b, threshold=128, max_value=255, object_type='light')
    					pcv.print_image( maskeda_thresh, "plant/maskeda_thresh.png")
    					pcv.print_image(maskeda_thresh1, "plant/maskeda_thresh1.png")
    					pcv.print_image(maskedb_thresh, "plant/maskedb_thresh1.png")
  
    					image = Image.open('plant/maskeda_thresh.png')
    					st.image(image, caption='Threshold green-magneta and blue image',use_column_width=True)


   # Join the thresholded saturation and blue-yellow images (OR)
    					ab1 = pcv.logical_or(bin_img1=maskeda_thresh, bin_img2=maskedb_thresh)
    					ab = pcv.logical_or(bin_img1=maskeda_thresh1, bin_img2=ab1)
        # Opening filters out bright noise from an image.

# Inputs:
#   gray_img - Grayscale or binary image data
#   kernel - Optional neighborhood, expressed as an array of 1's and 0's. If None (default),
#   uses cross-shaped structuring element.



def root():
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
    					s_thresh = pcv.threshold.binary(gray_img=s, threshold=85, max_value=255, object_type='light')
    					pcv.print_image(s_thresh, "plant/binary_threshold.png")
    					image = Image.open('plant/binary_threshold.png')
    					st.image(image, caption='Binary Threshold',use_column_width=True)
                   
    # Median Blur to clean noise 

    # Inputs: 
    #   gray_img - Grayscale image data 
    #   ksize - Kernel size (integer or tuple), (ksize, ksize) box if integer input,
    #           (n, m) box if tuple input 

    					s_mblur = pcv.median_blur(gray_img=s_thresh, ksize=5)
    					pcv.print_image(s_mblur, "plant/Median_blur.png")
    					image = Image.open('plant/Median_blur.png')
    					st.image(image, caption='Median Blur',use_column_width=True)
                    
     # An alternative to using median_blur is gaussian_blur, which applies 
    # a gaussian blur filter to the image. Depending on the image, one 
    # technique may be more effective than others. 

    # Inputs:
    #   img - RGB or grayscale image data
    #   ksize - Tuple of kernel size
    #   sigma_x - Standard deviation in X direction; if 0 (default), 
    #            calculated from kernel size
    #   sigma_y - Standard deviation in Y direction; if sigmaY is 
    #            None (default), sigmaY is taken to equal sigmaX
                
    					gaussian_img = pcv.gaussian_blur(img=s_thresh, ksize=(5, 5), sigma_x=0, sigma_y=None)
    # Convert RGB to LAB and extract the blue channel ('b')

    # Input:
    #   rgb_img - RGB image data 
    #   channel- Split by 'l' (lightness), 'a' (green-magenta), or 'b' (blue-yellow) channel
    					b = pcv.rgb2gray_lab(rgb_img=img, channel='b')
    					b_thresh = pcv.threshold.binary(gray_img=b, threshold=160, max_value=255, 
                                object_type='light')
                     # Join the threshold saturation and blue-yellow images with a logical or operation 

    # Inputs: 
    #   bin_img1 - Binary image data to be compared to bin_img2
    #   bin_img2 - Binary image data to be compared to bin_img1

    
    					bs = pcv.logical_or(bin_img1=s_mblur, bin_img2=b_thresh)
    					pcv.print_image(bs, "plant/threshold comparison.png")
    					image = Image.open('plant/threshold comparison.png')
    					st.image(image, caption='Threshold Comparision',use_column_width=True)
                    
 # Appy Mask (for VIS images, mask_color='white')

    # Inputs:
    #   img - RGB or grayscale image data 
    #   mask - Binary mask image data 
    #   mask_color - 'white' or 'black' 
    
    					masked = pcv.apply_mask(img=img, mask=bs, mask_color='white')
    					pcv.print_image(masked, "plant/Apply_mask.png")
    					image = Image.open('plant/Apply_mask.png')
    					st.image(image, caption='Applied Mask',use_column_width=True)
                   # Convert RGB to LAB and extract the Green-Magenta and Blue-Yellow channels
    					masked_a = pcv.rgb2gray_lab(rgb_img=masked, channel='a')
    					masked_b = pcv.rgb2gray_lab(rgb_img=masked, channel='b')
                     # Threshold the green-magenta and blue images
    					maskeda_thresh = pcv.threshold.binary(gray_img=masked_a, threshold=115, max_value=255, object_type='dark')
    					maskeda_thresh1 = pcv.threshold.binary(gray_img=masked_a, threshold=135,max_value=255, object_type='light')
    					maskedb_thresh = pcv.threshold.binary(gray_img=masked_b, threshold=128, max_value=255, object_type='light')
    					pcv.print_image( maskeda_thresh, "plant/maskeda_thresh.png")
    					pcv.print_image(maskeda_thresh1, "plant/maskeda_thresh1.png")
    					pcv.print_image(maskedb_thresh, "plant/maskedb_thresh1.png")
  
    					image = Image.open('plant/maskeda_thresh.png')
    					st.image(image, caption='Threshold green-magneta and blue image',use_column_width=True)


   # Join the thresholded saturation and blue-yellow images (OR)
    					ab1 = pcv.logical_or(bin_img1=maskeda_thresh, bin_img2=maskedb_thresh)
    					ab = pcv.logical_or(bin_img1=maskeda_thresh1, bin_img2=ab1)
        # Opening filters out bright noise from an image.

# Inputs:
#   gray_img - Grayscale or binary image data
#   kernel - Optional neighborhood, expressed as an array of 1's and 0's. If None (default),
#   uses cross-shaped structuring element.
    					opened_ab = pcv.opening(gray_img=ab)

# Depending on the situation it might be useful to use the 
# exclusive or (pcv.logical_xor) function. 

# Inputs: 
#   bin_img1 - Binary image data to be compared to bin_img2
#   bin_img2 - Binary image data to be compared to bin_img1
    					xor_img = pcv.logical_xor(bin_img1=maskeda_thresh, bin_img2=maskedb_thresh)
# Fill small objects (reduce image noise) 

# Inputs: 
#   bin_img - Binary image data 
#   size - Minimum object area size in pixels (must be an integer), and smaller objects will be filled
    					ab_fill = pcv.fill(bin_img=ab, size=200)
# Closing filters out dark noise from an image.

# Inputs:
#   gray_img - Grayscale or binary image data
#   kernel - Optional neighborhood, expressed as an array of 1's and 0's. If None (default),
#   uses cross-shaped structuring element.
    					closed_ab = pcv.closing(gray_img=ab_fill)
# Apply mask (for VIS images, mask_color=white)
    					masked2 = pcv.apply_mask(img=masked, mask=ab_fill, mask_color='white')
# Identify objects
# Inputs: 
#   img - RGB or grayscale image data for plotting 
#   mask - Binary mask used for detecting contours 
    					id_objects, obj_hierarchy = pcv.find_objects(img=masked2, mask=ab_fill)
# Define the region of interest (ROI) 
# Inputs: 
#   img - RGB or grayscale image to plot the ROI on 
#   x - The x-coordinate of the upper left corner of the rectangle 
#   y - The y-coordinate of the upper left corner of the rectangle 
#   h - The height of the rectangle 
#   w - The width of the rectangle 
    					roi1, roi_hierarchy= pcv.roi.rectangle(img=masked2, x=50, y=50, h=100, w=100)
# Decide which objects to keep
# Inputs:
#    img            = img to display kept objects
#    roi_contour    = contour of roi, output from any ROI function
#    roi_hierarchy  = contour of roi, output from any ROI function
#    object_contour = contours of objects, output from pcv.find_objects function
#    obj_hierarchy  = hierarchy of objects, output from pcv.find_objects function
#    roi_type       = 'partial' (default, for partially inside the ROI), 'cutto', or 
#                     'largest' (keep only largest contour)
    					roi_objects, hierarchy3, kept_mask, obj_area = pcv.roi_objects(img=img, roi_contour=roi1, 
                                                               roi_hierarchy=roi_hierarchy, 
                                                               object_contour=id_objects, 
                                                               obj_hierarchy=obj_hierarchy,
                                                               roi_type='partial')
# Object combine kept objects
# Inputs:
#   img - RGB or grayscale image data for plotting 
#   contours - Contour list 
#   hierarchy - Contour hierarchy array 
    					obj, mask = pcv.object_composition(img=img, contours=roi_objects, hierarchy=hierarchy3)
############### Analysis ################ 
# Find shape properties, data gets stored to an Outputs class automatically
# Inputs:
#   img - RGB or grayscale image data 
#   obj- Single or grouped contour object
#   mask - Binary image mask to use as mask for moments analysis 
    					analysis_image = pcv.analyze_object(img=img, obj=obj, mask=mask)
    					pcv.print_image(analysis_image, "plant/analysis_image.png")
    					image = Image.open('plant/analysis_image.png')
    					st.image(image, caption='Analysis_image',use_column_width=True)
# Shape properties relative to user boundary line (optional)
# Inputs:
#   img - RGB or grayscale image data 
#   obj - Single or grouped contour object 
#   mask - Binary mask of selected contours 
#   line_position - Position of boundary line (a value of 0 would draw a line 
#                   through the bottom of the image) 
    					boundary_image2 = pcv.analyze_bound_horizontal(img=img, obj=obj, mask=mask, 
                                               line_position=370)
    					pcv.print_image(boundary_image2, "plant/boundary_image2.png")
    					image = Image.open('plant/boundary_image2.png')
    					st.image(image, caption='Boundary Image',use_column_width=True)
# Determine color properties: Histograms, Color Slices and Pseudocolored Images, output color analyzed images (optional)
# Inputs:
#   rgb_img - RGB image data
#   mask - Binary mask of selected contours 
#   hist_plot_type - None (default), 'all', 'rgb', 'lab', or 'hsv'
#                    This is the data to be printed to the SVG histogram file  
    					color_histogram = pcv.analyze_color(rgb_img=img, mask=kept_mask, hist_plot_type='all')
# Print the histogram out to save it 
    					pcv.print_image(img=color_histogram, filename="plant/vis_tutorial_color_hist.jpg")
    					image = Image.open('plant/vis_tutorial_color_hist.jpg')
    					st.image(image, caption='Color Histogram',use_column_width=True)
# Divide plant object into twenty equidistant bins and assign pseudolandmark points based upon their 
# actual (not scaled) position. Once this data is scaled this approach may provide some information 
# regarding shape independent of size.
# Inputs:
#   img - RGB or grayscale image data 
#   obj - Single or grouped contour object 
#   mask - Binary mask of selected contours 
    					top_x, bottom_x, center_v_x = pcv.x_axis_pseudolandmarks(img=img, obj=obj, mask=mask)
    					top_y, bottom_y, center_v_y = pcv.y_axis_pseudolandmarks(img=img, obj=obj, mask=mask)
# The print_results function will take the measurements stored when running any (or all) of these functions, format, 
# and print an output text file for data analysis. The Outputs class stores data whenever any of the following functions
# are ran: analyze_bound_horizontal, analyze_bound_vertical, analyze_color, analyze_nir_intensity, analyze_object, 
# fluor_fvfm, report_size_marker_area, watershed. If no functions have been run, it will print an empty text file 
    					pcv.print_results(filename='vis_tutorial_results.txt')



    
    
    
    
    
    
    
    
    
    
    







if __name__ == '__main__':
	main()
