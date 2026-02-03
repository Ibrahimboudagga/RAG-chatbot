# mini-rag 
this is a minimal implementation of the rag model for question answering

(Optional) Setup you command line interface for better readability
export PS1="\[\033[01;32m\]\u@\h:\w\n\[\033[00m\]\$ "

## run the fastapi server
uvicorn main:app --reload --host 0.0.0.0 --port 5000