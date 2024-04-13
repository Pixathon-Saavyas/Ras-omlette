from uagents import Agent, Context,Model
import google.generativeai as genai
import requests

class Message(Model):
  msg:str
class DeltaVMessage(Model):
  msg:str

MAILROOM_API = "baa7af95-3df0-4786-8d43-6dbf028fd0a6"
        
prompt = ""

alice = Agent(name="alice",  port=8000,
    seed="alice secret phrase",
    mailbox=f"{MAILROOM_API}@https://agentverse.ai",
    endpoint=["http://127.0.0.1:8000/submit"],)
    

# list = ["i am happy","i am sad","ok"]


# Prints the unique address of the agent
#used to identitfy the agent on fetch network
print("uAgent address: ", alice.address)

# Network Adddress
print("Fetch network address: ", alice.wallet.address())


genai.configure(api_key="AIzaSyB0CxS1AjgcQUb2QEMvASd60854XKrSBCY")

generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                generation_config=generation_config,
                                safety_settings=safety_settings)

convo = model.start_chat(history=[])

def getGeminiResponse(str):
    # convo.send_message(f"Act like you are a movie recomendation system and  give me the output in form of titles only for the following:{str}")
    print(f"promt : {prompt}")
    convo.send_message(f"Act like you are a movie recomendation system and  give me the output in form of titles only for the following:{str}")
    
    list = convo.last.text.split("\n")
    newlist = [item.split('. ')[1] for item in list]
    print(newlist)
    str1=", ".join(newlist)
    print(str1)
    return str1



# Runs Only on start up
@alice.on_event("startup")
async def say_hello(ctx: Context):
    # Set up the model
    print(f"Starting {ctx.address}")
    
    

@alice.on_message(model=DeltaVMessage)
async def handle_query_response(ctx: Context, sender: str, msgg: DeltaVMessage):
    # Handling the incoming message
    print(f"msg: {msgg.msg}")
    movieList = getGeminiResponse(msgg.msg)
    print(movieList)
    await ctx.send("agent1qvr3ahrx2d5ewyvfeug0tjvl6cy7mtchusztw8mg7nc6vgwx3uje6jwkhag",Message(msg=movieList))
    # message = await handle_message(msg.message)
    
    # Logging the response
    # ctx.logger.info(message)
    
    # Sending the response back to the sender
    # await ctx.send(sender, Message(message=message))

if __name__ == "__main__":
    alice.run()