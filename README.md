# Chatbot_with_college_rules_documents

You can start with entering 'python app.py' into your cmd window (which should be located in your right folder path).
A few seconds later, link will pop up on your cmd window.
Copy and paste the link.
Now, start a chat.
I am using module from langchain and openai. To execute some file, you need openai api key. Input your key into '키입력' section.

Model folder, it consists of several files and two folders for user interface, such as static and templates.

'_add_index.py' is literally adding new index to your faiss file. To execute this, there should be faiss index folder already saved in a local folder on your computer.
'_create_vectorstore.py' is a function to save faiss index on your computer.
'_generator.py' gets a question from user, and generates an answer.
'_ingest_data.py' processes documents. You can use any other documents here. It can be pdf, txt, etc.
'app.py' is connected to _generator.py. This directly gets a question from user and send to _generator.py. Finally, return an answer to user.
Any comments about the code are welcome.