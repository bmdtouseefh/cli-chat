
from google import genai
from fastapi import FastAPI
from fastapi import Depends

from database import session, Session, Chats, User
from sqlalchemy import select, insert

app = FastAPI()

client = genai.Client(api_key="AIzaSyAdN472me0CDtniux59_ACalokXaZ2Mxs8")


def get_db():
    db = session()
    try: 
        yield db
    finally:
        db.close()


@app.get("/chat")
def chat(user_input: str, db: Session = Depends(get_db)):
    stmt=select(Chats.prompt, Chats.response_text)
    chat_entries = db.execute(stmt).all()
    formatted_history = []
    for prompt, response_text in chat_entries:
        # Add user's turn
        formatted_history.append({"role": "user", "parts": [{"text": prompt}]})
        # Add model's turn
        formatted_history.append({"role": "model", "parts": [{"text": response_text}]})

    chatSession = client.chats.create(model="gemini-2.0-flash",history=formatted_history) 
    if not user_input:
        return("Enter something")
    try:
        response = chatSession.send_message(user_input)
        current_chat = Chats(user_id=1, prompt=user_input, response_text=response.text)
        db.add(current_chat)
        db.commit()
        updated_raw_history_texts = [entry for entry in db.scalars(select(Chats)).all()]
        return({"Gemini":f"{response.text}", "All":updated_raw_history_texts})

    except Exception as e:
        return(f"some error {e}")


@app.post("/register")
def register(username: str, password: str, db: Session = Depends(get_db)):
    user=User(username=username, password=password)
    db.add(user)
    db.commit()
    return ({f"Added User":{user.username}})
    

@app.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    stmt=select(User).where(User.username==username and User.password==password)
    userTrue=db.scalar(stmt)
    if userTrue is not None:
        return ({f"Logged in as User":{username}})
    else:
        return('Not exists')




