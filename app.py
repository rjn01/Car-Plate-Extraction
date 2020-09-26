
from flask import Flask, render_template, redirect, request
import main 
import detect

app =  Flask(__name__)

@app.route('/')  #It is the route  of the url

def hello():  # this would be shown on the url
    return render_template('index.html') 
    
@app.route('/', methods = ['POST']) #we have to write the method as POST as we are using post method
#we dont write  GET bcoz it is automatically assigned to the request

def submit_data():
    if request.method== 'POST':
        f = request.files["userfile"]  #for files we have to use .files
        path = "./static/{}".format(f.filename)
        f.save(path)  #save file which is sent by user.
        
        
        path = detect.object(path)
        print(path)
        if path:
            output = main.text_reader(path)
            print(output)
            result_dic = {
            'img' : f.filename,
            'text' : output
        }
        

        else:
            result_dic = {
            'img' : f.filename,
            'text' : "NO number plate detected"
            }

    return(render_template("index.html", your_text = result_dic))
    

if __name__== "__main__":
    #app.debug=True  
    #if we make any changes to code then we don't have to run the program again through terminal
    # we can also write in the run command
    app.run(debug=True)
