# collaborative-document-tree-editor

Project Selection: Collaborative Document Tree Editor

Project Member 1: Aylin Topcu 2448926

Project Member 2: Atahan Kılıç 2376762

Description of the project content:

DocTreeClass.py: This file contains the implementation of the DocTree class.

ElementClass.py: This file contains the implementation of the Element class.

UserClass.py: This file contains the implementation of the User class.

Enums.py: This file contains the implementations of the Status (used for authentication status) and Occurs 
(used for child occurrence data in the template) Enum classes used in the project. 

Decorators.py: This file contains the implementations of the singleton, update_users and auth_required 
decorators used in the project.

(DEPRECATED) demo.py: A demo for showing different functionalities of the project.

Server.py: This file contains the implementation of the server side of the project. It starts the server and 
and listens for incoming connections. It creates an agent thread for each of the incoming connections.

Agent.py: This file contains the implementation of the agent class. It is used for handling the requests coming from 
the clients and sending the notifications to the clients.

Client.py: This file contains the implementation of the client side of the project. It connects to the server and
sends requests to the server. It also listens for the notifications coming from the server.

CommandHandler.py: This file contains the implementation of the CommandHandler class. It is used for directing 
the requests coming from client to document class. "help" command can be used to see the available commands and their
usages.

Document.py: This file contains the implementation of the Document and DocumentInstancePerUser classes. Document class
is used for making the library calls defined in DocTreeClass and ElementClass. DocumentInstancePerUser is a wrapper 
class for Document class. It is used for keeping the document instance of each user separately and making the
library calls.

Editor.py: This file contains the implementation of the Editor class. It is used for managing the document instances.
New, open, close, delete, list commands are implemented in this class.

requirements.txt: This file contains the required packages for the project. Currently, it contains only the lxml 
package used for converting the xml string to HTML. "pip install -r requirements.txt" command can be used for 
installing the required packages.
