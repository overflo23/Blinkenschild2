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
import os
import subprocess
from os import listdir
from os.path import isfile, join
from TC import *


BASEPATH="/home/pi/Blinkenschild2"


app = Flask(__name__)







def kill_old_processes():
    try:
        os.system(BASEPATH+"/scripts/killall.sh")
    except:
        pass



def run_process(exec_this):
    kill_old_processes()
    pr = subprocess.Popen(exec_this.split(),  preexec_fn=os.setsid) 



def hex2rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))



#def hex2rgb(hexcode):
#    print("hex: " + hexcode)
#    return tuple(map(ord,hexcode[1:].decode('hex')))


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





# display chosen picture
@app.route('/api/pictures', methods=['POST', 'PUT'])
def picture():
    pic = request.form['pic']
#    run_process("sudo " + BASEPATH + "/bin/led-image-viewer --led-rows=16 --led-cols=32 --led-chain=2  --led-parallel=3 --led-brightness=100 --led-multiplexing=0  -C "+ BASEPATH +"/Flask/"  +pic)   
    run_process("scripts/display_picture.sh " + pic)
    return json.dumps({'status':'OK','picture':pic})


# send a list of pics to the  client
@app.route('/api/pictures', methods=['GET'])
def get_pics():
    pictures = [f for f in listdir("pics") if isfile(join("pics", f))]
    return json.dumps(pictures)




@app.route('/api/text', methods=['POST'])
def write_text():
    print('write_text was called') # DEBUG
    text = request.form['text']
    textcolor = hex2rgb(request.form['textcolor'])
    bordercolor = hex2rgb(request.form['bordercolor'])

    run_process("scripts/display_text.sh " + text +" " + str(textcolor[0]) +","+str(textcolor[1]) +"," + str(textcolor[2])  + " " + str(bordercolor[0]) + "," + str(bordercolor[1]) +"," + str(bordercolor[2])) 

    return json.dumps({'status':'OK','msg':'Displaying text {}'.format(text)})








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

    return json.dumps(  tweets );





@app.route('/api/twitter', methods=['POST'])
def show_tweet():
    print('show_tweet called') # DEBUG
    text = request.form['tweet']
    run_process("scripts/display_twitter.sh " + text )
    return json.dumps({'status':'OK','msg':'TWEET {}'.format(text)})







if __name__=="__main__":
	app.run()
