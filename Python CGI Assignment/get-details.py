#!C:\Users\Preston\AppData\Local\Programs\Python\Python310\python.exe

print('content-type: text/html')

import cgitb
import cgi
import html
import os

cgitb.enable()

form = cgi.FieldStorage()

name = html.escape(form.getvalue('name', ''))
email = html.escape(form.getvalue('email', ''))
password = html.escape(form.getvalue('password', ''))
emotions = form.getlist('mood')
satisfactions = form.getvalue('satisfaction', '')
comments = html.escape(form.getvalue('comments'))
imagefile = form['file-inp']
location = form.getvalue('locs', '')

imagename = os.path.basename(imagefile.filename)
open('files/' + imagename, 'wb').write(imagefile.file.read())
url = 'files/' + imagefile.filename

print(f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Document</title>
    <link rel="stylesheet" href="style.css">
    <link rel="stylesheet" href="https://assets.ubuntu.com/v1/vanilla-framework-version-3.6.1.min.css" />
</head>
<body>
    <div class="container">
        <h3>Feedback Response</h3>
        Name : { name } <br>
        Email : { email } <br>
        Password : { password } <br>
        Emotions : { emotions } <br>
        Satisfaction : { satisfactions } <br>
        Further comments : { comments } <br>
        Bio photo<br>
        <img src="{ url }"><br>
        Location visited: { location }<br>
    </div>
</body>
</html>
""")
