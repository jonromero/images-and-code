# Under GPL
# I should add more stuff here :D
# Jon Vlachogiannis

#javascript:var fileref=document.createElement("script");fileref.setAttribute("type","text/javascript");fileref.setAttribute("src", "/home/darksun4/Sources/ImagesAndCode/dynload.js");hi();


import Image
import operator # used for getting the max in a dictionary
import re # used to get the tags
from datetime import *

def preloader():
	print "Reading image"
	im = Image.open("twox2-1a.png")
	
	pix = im.load()
	#f = open('pixels.dat', 'w+')

	list_of_pixels = list()
	for i in range(im.size[0]):
		for j in range(im.size[1]):
			hex_color = "#%X%X%X" % pix[i,j][:3] #get rid of alpha		
			line = "D[replace_me]=new Array(%d,%d,'%s');" % (i, j, hex_color)
					
			# add to list 
	 		list_of_pixels.append(line)
 		        #print "Added", line
			
	# for common color and use it for background
	# Todo: Use a dictionary. Also rewrite the two for in a more pythonic way
	common_colors_list = list()
	for pixel in list_of_pixels:
		common_colors_list.append(pixel.split('#')[1].split("');\n")[0])
				
	common_colors_dict = dict()
	for common_color in common_colors_list:
		common_colors_dict[common_color] = common_colors_list.count(common_color)
					
	most_common_color = max(common_colors_dict.iteritems(), key=operator.itemgetter(1))[0]
	print "Color", most_common_color, "is found", common_colors_dict[most_common_color], "times"
					
	pixels_not_written = 0
	
	i = 0
	optimized_list_of_pixels = list()
	for pixel in list_of_pixels:
		if not most_common_color in pixel:
			#f.write(pixel)
			optimized_list_of_pixels.append(pixel.replace("replace_me",str(i)))
			i += 1
		else:
			pixels_not_written += 1
			
	#f.close()
							
	print "Skipping %s pixels" % pixels_not_written
	print len(optimized_list_of_pixels)
	return optimized_list_of_pixels


# evals the tags that are in the file
def process(template_file, output_file):
	html_data = open(template_file, "r").read()

	# find all the tags inside {{tag}}
	eval_tags = re.findall(r'{{(.+?)}}', html_data)
	
	for tag in eval_tags:
		print tag, eval(tag)
		replace_tag = "{{%s}}" % tag
		html_data = html_data.replace(replace_tag, str(eval(tag)))
	
	f = open(output_file, "w+")
	f.write(html_data)
	f.close()
	print "Done"


def jsImport(inc_file):
	return '<script type="text/javascript" src="%s"></script>' % inc_file


def jsPreloadData():
	js_hdata =  "var D = new Array();\n"
	js_data = ""

	return js_hdata + js_data.join(preloader())


def jsRun(func_name):
	js_func_content = "for (var i=0; i<D.length-1; i++){\n	\
	                        jg.setColor(D[i][2]);\n \
	                        jg.fillRect(D[i][0], D[i][1], 1, 1);\n \
                           }\n" 

	js_func_declaration = "function %s(){\n %s\n jg.paint();\n }\n" % (func_name, js_func_content)

	if func_name == 'shareTheLove':
		js_canvas = "var cnv = document.getElementsByTagName('body').item(0); \n"
	else:
		js_canvas = "var cnv = document.getElementById('myCanvas'); \n"

	js_canvas += "var jg = new jsGraphics(cnv);\n"

	return js_func_declaration + js_canvas +  ("%s();" % func_name)


def createJSFilesForDynamicLoading():
	f = open("images_and_code.js", "w+")
	
	# load the extra lib
	f.write('alert("Welcome to Two-by-2 WebComic! Check the latest at http://www.emotionull.com/twox2/");' + "document.write('<script src=\"http://www.kokoblogo.gr/jon/wz_jsgraphics.js\" type=\"text/JavaScript\"></script>');")

	# load our data
	f.write(jsPreloadData() + jsRun('shareTheLove'))

	f.close()


process("template.html", "output.html")
createJSFilesForDynamicLoading()	
