from flask import Flask
from app import views

app = Flask(__name__)

# url
app.add_url_rule('/base','base',views.base) 
app.add_url_rule('/','index',views.index)
app.add_url_rule('/yoloapp','yoloapp',views.yoloapp)
app.add_url_rule('/yoloapp/objectdetection','objectdetection',views.objectdetection,methods=['GET','POST'])
# 
if __name__ == "__main__":
    app.run(debug=True)