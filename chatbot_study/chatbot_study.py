from flask import Flask, request, jsonify, abort
import socket
import json


# 챗봇 엔진 서버 접속 정보
host = "127.0.0.1"  # 챗봇 엔진 서버 IP 주소
port = 5050  # 챗봇 엔진 서버 통신 포트

# Flask 어플리케이션
app = Flask(__name__)

@app.route('/')    
def hello():
    print ('여기에 HTML 입력하면 되나?')
    print ('안됨. 인터프리터 화면에만 출력됨')
    #return '그럼 여기에 입력하면 ok?'
    return '<h1>제목입니다</h1> </br> <div>그냥 의미없는 <strong>파이썬을 이용한 HTML 요소 생성</strong> 테스트 문구</div> <br> <span>그렇다고 이렇게 일일이 HTML을 작성할 수는 없는 노릇인데, <em>어떻게 하면 좋을까요?</em> </span>'
def hello_itsme():
    return 'Hello Flask'
hello_itsme()
#함수 두개 실행 안됨.... 하나만 됨


# 챗봇 엔진 서버와 통신
def get_answer_from_engine(bottype, query):
    # 챗봇 엔진 서버 연결
    mySocket = socket.socket()
    mySocket.connect((host, port))

    # 챗봇 엔진 질의 요청
    json_data = {
        'Query': query,
        'BotType': bottype
    }
    message = json.dumps(json_data)
    mySocket.send(message.encode())

    # 챗봇 엔진 답변 출력
    data = mySocket.recv(2048).decode()
    ret_data = json.loads(data)

    # 챗봇 엔진 서버 연결 소켓 닫기
    mySocket.close()
   
    print("답변1")
    print(ret_data['Answer'])
    print("답변2")
    print(ret_data)
    print("답변3")
    print(type(ret_data))
    print("\n")
    return ret_data


@app.route('/', methods=['GET'])
def index():
    print('hello')

# 챗봇 엔진 query 전송 API


@app.route('/query/<bot_type>', methods=['POST'])
def query(bot_type):
    body = request.get_json()

    try:
        if bot_type == 'TEST':
            # 챗봇 API 테스트
            
            ret = get_answer_from_engine(bottype=bot_type, query=body['query'])

            return jsonify(ret)

        elif bot_type == "KAKAO":
            # 카카오톡 스킬 처리
            pass

        elif bot_type == "NAVER":
            # 네이버톡톡 Web hook 처리
            pass
        else:
            # 정의되지 않은 bot type인 경우 404 오류
            abort(404)

    except Exception as ex:
        # 오류 발생시 500 오류
        abort(500)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
