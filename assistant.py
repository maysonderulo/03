from openai import OpenAI
client = OpenAI(sk-proj-MQ89fpGdHuRV81MM4HODT3BlbkFJ2CdbFMvJC6EgS4uMY0cb)

file = "C:\Users\홍서영\Desktop\들락날락 메뉴.xlsx"

def file_upload(file):
    file =  client.files.create(
    file=open(file,"rb"),
    purpose="assistants"
    )

    print(file)
  file_upload(file)
 

my_assistant = client.beta.assistants.create(
    instructions="You are an HR bot, and you have access to files to answer employee questions about company policies.",
    name="HR Helper",
    tools=[{"type": "file_search"}],
    tool_resources={"file_search": {"vector_store_ids": ["vs_123"]}},
    model="gpt-4-turbo"
)
print(my_assistant)



