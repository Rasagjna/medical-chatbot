from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model= "gemini-pro",temperature="0.8",convert_system_message_to_human=True)