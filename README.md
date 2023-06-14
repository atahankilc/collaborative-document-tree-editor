Project: Collaborative Document Tree Editor

Project Members:

- Aylin Topçu e2448926
- Atahan Kılıç e2376762

Usage:

- install requirements using `pip install -r requirements.txt`
- run Server.py under server folder using `python Server.py --port <port_number>`
- run Django project under backend folder using `python manage.py runserver --port <port_number>`

Test Users:

- username: user_1 password: 123456_1
- username: user_2 password: 123456_2

Sample Document Template:

```
{"root":'document',"elements":{"document":{"attrs":[],"children":['meta','abstract'],"occurs":'1'},"meta":{"attrs":[],"children":['author','date','title'],"occurs":'1'},"abstract":{"attrs":[],"children":[],"occurs":'?'},"author":{"attrs":[],"children":[],"occurs":'?'},"date":{"attrs":[],"children":[],"occurs":'?'},"title":{"attrs":[],"children":[],"occurs":'1'}}}
```

````
{"root":'document',"elements":{"document":{"attrs":[],"children":['meta','abstract', 'section'],"occurs":'1'},"meta":{"attrs":[],"children":['author','date','title'],"occurs":'1'},"abstract":{"attrs":[],"children":[],"occurs":'?'},"author":{"attrs":[],"children":[],"occurs":'?'},"date":{"attrs":[],"children":[],"occurs":'?'},"title":{"attrs":[],"children":[],"occurs":'1'}, "section":{"attrs":[],"children":["text"],"occurs":'?'}}}
````