from flask import *
from jpype import *
import os
import javaobj
import requests
import gzip
import io
import StringIO
import base64

app = Flask(__name__)
startJVM(getDefaultJVMPath(), "-Djava.class.path=%s/mop-login.jar" % os.getcwd())

@app.route('/getvc', methods=['GET'])
def get_vc():
    mobile = request.args.get('mobile')
    pwd = request.args.get('pwd')
    print(mobile, pwd)
    return get_vc_java(mobile, pwd)


def get_vc_java(mobile, pwd):
    try:
        Main = JClass("Main")
        Main.getSendBase64(mobile, pwd, 0)
        b = Main.getSendBase64(mobile, pwd, 1)
        b = base64.b64decode(b)
        bb = io.BytesIO()
        g = gzip.GzipFile(mode='wb', compresslevel=9, fileobj=bb)
        g.write(b)
        g.close()
        r = requests.post(
            url='http://112.5.185.82:8880/MBOP/mbop_services',
            data=bb.getvalue()
        )
        b = StringIO.StringIO(r.content)
        b = gzip.GzipFile(fileobj=b)
        o = javaobj.loads(b.read())
        # print(o.obj.verifyCode)
        return o.obj.verifyCode
    except:
        return 'error'


if __name__ == '__main__':
    app.run()
