from _generator import generator
from flask import Flask, request, jsonify, render_template


app = Flask(__name__)

@app.route('/')
def my_template():
    return render_template('chatwindow.html')

@app.route('/process', methods=['POST'])
def post_message():
    while True:
        user_input = request.json['message']

        if user_input == '아니오' :
            generator(user_input)
            bot_response = '대화가 종료됩니다. 이전의 대화기록은 삭제되었습니다. 새로운 대화를 시작하고 싶은 경우, 질문을 새로 입력해 주세요.'

            return jsonify({'message': bot_response})
        
        else :
            bot_response = generator(user_input)

            return jsonify({'message': bot_response})


if __name__ == '__main__' :
    app.run(host="0.0.0.0", port=7777, debug=True)