import os
from flask import Flask, request, render_template

app = Flask(__name__)

def super_WAF(user_input):
    black_lists  = [";","|","&","`","$","(",")","#","id","ls","cat","less","more","nl","*","[","]","{","}"]
    
    if len(user_input) > 7:
        return "Gõ ít chữ thôi, quá 7 chặt tay!"
    elif any(keyword in user_input for keyword in black_lists ):
        return "Thấy mùi hackẻ lỏ, bắt bỏ tù giờ!"
    
    return user_input

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None

    if request.method == 'POST':
        user_input = request.form['input']
        user_input = super_WAF(user_input)
        command = "echo " + user_input
        result = os.popen(command).read()

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9001, debug=True)