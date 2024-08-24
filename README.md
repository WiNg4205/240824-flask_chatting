# 24/08/24 - flask_chatting (#17)
This is a simple web app where the user types in a message and can click send to permanently save the message. It uses websockets which gives it an automatic update of the messages if the user has the app running on multiple tabs or browsers.

I used Flask for the backend and SQLite for the database. This gave me a refresher on the connect, cursor, execute, commit and close methods when itneracting with the db. This is one of my first times using websockets but I did not find it too difficult to code. Using vanilla js in the html file was also a nice refresher on how the dom can be manipulated and also event listeners.
