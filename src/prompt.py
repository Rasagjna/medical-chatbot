prompt_template = """You are helpful information giving QA System and make sure you don't answer anything 
not related to following context. You are always provide useful information & details available in the given context. Use the following pieces of context to answer the question at the end. 
If you don't know the answer, just say that you don't know, don't try to make up an answer. 

{context}

Question: {question}
Helpful Answer:"""

template2="""
Given the following conversation and a follow-up message, \
rephrase the follow-up message to a stand-alone question or instruction that \
represents the user's intent, add all context needed if necessary to generate a complete and \
unambiguous question or instruction, only based on the history, don't make up messages. \
Maintain the same language as the follow up input message.
Chat History:
{chat_history}

Follow Up Input: {question}
Standalone question or instruction:
"""