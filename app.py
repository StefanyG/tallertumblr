# coding: utf-8
from flask import Flask, render_template , request , url_for, g, flash, redirect
import json, pytumblr, time

search=""
data=[]

app = Flask(__name__)
client = pytumblr.TumblrRestClient('3woTLqDJZ5zXBlRJphQbT96W75gz4jKR0E6LookITYlfXCjhAu') #mi API key

@app.route("/", methods=['GET','POST'])
def home():
    global search,data
    if request.method=="POST":
        search = request.form.get("search", None)
        dic = client.tagged(search,before=time.time())
        dic=dic+client.tagged(search,before=time.time()-100000)
        dic=dic+client.tagged(search,before=time.time()-200000)
        dic=dic+client.tagged(search,before=time.time()-300000)
        dic=dic+client.tagged(search,before=time.time()-400000)
        print ("len(dic)")
        data=[]
        for each in dic:
            if "photos" in each:
                data.append(each["photos"][0]['original_size']['url'])
        return redirect(url_for('results'))
    return render_template("home.html")

@app.route("/results")
def results():
    global search,data
    l=len(data)
    d1=[]
    d2=[]
    d3=[]
    d4=[]
    count=-1
    for each in data:
        if count<(l/4):
            d1.append(each)
        elif count<(l/2):
            d2.append(each)
        elif count<(l*3/4):
            d3.append(each)
        else:
            d4.append(each)
        count+=1
    return render_template("resultados.html",search=search,d1=d1,d2=d2,d3=d3,d4=d4)
if __name__ == "__main__":
    app.run()

