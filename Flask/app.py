#!/usr/bin/env python3
# coding: utf-8

'''
TODO:
	frontend
		Layout styling
		control elements
	backend
		calling scripts
			download youtube video
				link
			display picture
				infinite
				show for X seconds
			display text
				color
		handling frontend calls

FRONTEND WORKFLOW:
	display controls
		youtube link field, play button
		picture upload button, seconds chooser, display button
		text field (FUTURE: calculate width for pixels and turn red if not on 1 screen), color chooser, write button

FUTURE:
	session ids? identifying multi user.
	Queue
'''

from flask import Flask,render_template, request,json
from twython import Twython
#import hashlib
import os
#import signal
import subprocess
from os import listdir
from os.path import isfile, join


app = Flask(__name__)




def kill_old_process():
    file = open("/tmp/python_duo_external.pid.txt","r")
    pid=file.read()
    file.close()
 #   print "killing " + pid
    subprocess.Popen(["sudo", "kill", str(pid)])




def run_process(string):
    kill_old_process()
    pr = subprocess.Popen(["sudo","/media/external/scripts/twitter.py", "--led-rows=16", "--led-cols=32", "--led-chain=2",  "--led-parallel=3", "--led-brightness=50", "--led-multiplexing=0",  "-t", string], preexec_fn=os.setpgrp)
    pid = pr.pid
    file = open("/tmp/python_duo_external.pid.txt","w")
    file.write(str(pid))
    file.close()








def run_process(exec_this):
    global pr
    try:
            subprocess.Popen(["sudo", "kill", str(pr.pid)])
    except:
        pass

    pr = subprocess.Popen(exec_this.split(), preexec_fn=os.setpgrp)

    
    
#    if(external_proc.pid):
#        external_proc.kill();
#    external_proc = subprocess.Popen("/media/external/scripts/twitter.sh")



@app.route('/')
def hello():
	return render_template('main.html', current_task='Nothing') # TODO: should display what the schild is currently doing




@app.route('/api/youtube', methods=['POST', 'PUT'])
def youtube():
	print('youtube was called') # DEBUG
	if request.method == 'POST':
		videolink = request.form['yt_video']
		# TODO: Needs to call backend script, backend script should return success code which gets returned below
		return json.dumps({'status':'OK','msg':'Downloaded video {}'.format(videolink)})
	elif request.method == 'PUT':
		videolink = request.form['yt_video']
		# TODO: As far as I know the current backend script can only download but not display?
		return json.dumps({'status':'OK','msg':'Playing video {}'.format(videolink)})






@app.route('/api/pictures', methods=['POST', 'PUT'])
def picture():
    print('picture was called') # DEBUG
    pic = request.form['pic']
    run_process("scripts/display_picture.sh " + pic)

    return json.dumps({'status':'OK','picture':pic})



@app.route('/api/pictures', methods=['GET'])
def get_pics():
    pictures = [f for f in listdir("pics") if isfile(join("pics", f))]
    return json.dumps(pictures)





@app.route('/api/text', methods=['POST'])
def write_text():
	print('write_text was called') # DEBUG
	text = request.form['text']
	textcolor = request.form['color']

	# TODO: Needs to call backend script, backend script should return success code which gets returned below
	return json.dumps({'status':'OK','msg':'Displaying text {} in color {}'.format(text, textcolor)})






APP_KEY="UIVprpANKRSJqx56Pey9mkwB4"
APP_SECRET="UbolouemM0Ds32Oy6KK7WAWiay32e5O8JEwzB8ng9qMNiPE9yN"
ACCESS_TOKEN="1062250213555998720-YNBc4AGKAJoFatWksqD3qmVoNEwtdv"
ACCESS_SECRET="PxaD0PZqL0y0RD7SV1I4zfI3WSW3GVxxj8BUaD2jgCk0S"


@app.route('/api/twitter', methods=['GET'])
def get_tweets():
    print('get_tweets called') # DEBUG

    twitter = Twython(APP_KEY,APP_SECRET,ACCESS_TOKEN,ACCESS_SECRET)
    results = twitter.cursor(twitter.search, q='@blinkenschild')

    tweets=[]
    for result in results:
        if result["text"].startswith("@blinkenschild"):
            uname=result["user"]["screen_name"]
            text=result["text"]
            tweet = {"user": uname, "msg": text.replace('@blinkenschild','')}
            tweets.append(tweet)


    

#    print hashlib.md5(tweets)
    return json.dumps(  tweets );





@app.route('/api/twitter', methods=['POST'])
def show_tweet():
    print('show_tweet called') # DEBUG
    text = request.form['tweet']
    run_process(text)
    # hier sollten wir den tweet anzeigen.. das keonenn wir direkt in python machen..
    return json.dumps({'status':'OK','msg':'TWEET {}'.format(text)})







if __name__=="__main__":
	app.run()
