import os
import sys
import getpass
import argparse
import magic

def check_file_type(filename):
    mime = magic.Magic(mime=True)
    file_type = mime.from_file(filename)
    
    if 'pdf' in file_type.lower():
        return 'PDF'
    elif 'msword' in file_type.lower() or 'wordprocessingml' in file_type.lower():
        return 'DOC'
    elif 'text' in file_type.lower():
        return 'TXT'
    else:
        return 'Unknown'

parser = argparse.ArgumentParser(description="Take inputs from user to generate a cover letter.")
parser.add_argument("--resume", required=True, 
                    help="The path to load your pdf resume file (txt, pdf, or doc).")
parser.add_argument("--jd", default='files/jd.txt', 
                    help="The path to load the job description txt file.")
parser.add_argument("--user", default='files/user_cv_prompt.txt', 
                    help="The user input txt file to guide the writing of cover letter.")
parser.add_argument("--model", "-m", default="gpt-3.5-turbo", choices=["gpt-3.5-turbo", "gpt-4"],
                    help="The foundation model you want to select to complete the task")
args = parser.parse_args()

# set the openai key
os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI key: ")

from langchain_community.document_loaders import PyPDFLoader, TextLoader, ReadTheDocsLoader
from langchain_chroma import Chroma
from langchain.memory.vectorstore import VectorStoreRetrieverMemory
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain.chains import ConversationChain, create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage

import bs4
from langchain import hub

chunk_size = 1000
chunk_overlap = 50
temperature = 0.2

# Create the LLM
llm = ChatOpenAI(model_name=args.model, temperature=temperature)

# Create rag QA of the job description
job_name = input('The title of the job: ')
company_name = input('The name of the company: ')

jd_file = open(args.jd, "r")
job_description = jd_file.read()
jd_file.close()
job_description = '\n'.join((f'The title of the job is {job_name}', f'The name of the company is {company_name}', job_description))

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=chunk_size, chunk_overlap=chunk_overlap, add_start_index=True
)

jd_splits = text_splitter.split_text(job_description)
jd_docs = text_splitter.create_documents(jd_splits)

jd_vectorstore = Chroma.from_documents(documents=jd_docs, embedding=OpenAIEmbeddings())

llm = ChatOpenAI(model_name=args.model, temperature=0.2)
jd_retriever = jd_vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

contextualize_q_system_prompt = """Given a chat history and the latest user question \
which might reference context in the chat history, formulate a standalone question \
which can be understood without the chat history. Do NOT answer the question, \
just reformulate it if needed and otherwise return it as is."""
contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

jd_history_aware_retriever = create_history_aware_retriever(
    llm, jd_retriever, contextualize_q_prompt
)

qa_system_prompt = """You are an assistant for question-answering tasks. \
Use the following pieces of retrieved context to answer the question. \
If you don't know the answer, just say that you don't know. \
keep the answer concise.\

{context}"""
qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", qa_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

jd_rag_chain = create_retrieval_chain(jd_history_aware_retriever, question_answer_chain)

# keep recording the chat history
chat_history = []

# questions on the job descriptions
questions = [
    "What's name of the company?",
    "What's the culture of it?",
    "What's the value mission of the company?"
    "What's the title of the job?",
    "What are the requirements of it, including but not limited to degree, citizenship and skills?",
    "What are the job responsibilities of it?",
]

for question in questions:
    msg = jd_rag_chain.invoke({"input": question, "chat_history": chat_history})
    chat_history.extend([HumanMessage(content=question), msg["answer"]])

# Load the resume and QA on resume
re_file = open(args.resume, "r")
re_file_type = check_file_type(args.resume)

if re_file_type == 'PDF':
    loader = PyPDFLoader(args.resume)
elif re_file_type == 'DOC':
    loader = ReadTheDocsLoader(args.resume)
elif re_file_type == 'TXT':
    loader = TextLoader(args.resume)
else:
    sys.exit(f"The file type of {args.resume} is not supported.")
re_pages = loader.load_and_split(text_splitter)
re_file.close()

re_vectorstore = Chroma.from_documents(documents=re_pages, embedding=OpenAIEmbeddings())
docs = re_vectorstore.similarity_search("What are the schools the applicant attended?", k=3)

re_retriever = re_vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})

re_system_prompt = """You are an applicant for a job with the given resume. \
Use the following pieces of retrieved context to answer questions about yourself towards the job. \
If you don't know the answer, just say that you don't know. \
keep the answer concise.\

{context}"""
re_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", re_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

re_question_answer_chain = create_stuff_documents_chain(llm, re_prompt)

re_rag_chain = create_retrieval_chain(re_retriever, re_question_answer_chain)

# resume questions
questions = [
    "Do you meet the degree requirement of the job?",
    "What projects you did that shows the required skills of the job and why?",
    "Can you show you are a good cultural fit for the job?"
    "Did you worked or interned in the company before? If so, tell me what position it was and what project you did."
]

for question in questions:
    msg = re_rag_chain.invoke({"input": question, "chat_history": chat_history})
    chat_history.extend([HumanMessage(content=question), msg["answer"]])

# based on the chat history, create a customized cover letter for the job
cv_system_prompt = """You are an applicant (with a resume) for a job (with a job description). \
Write as the first-person narrative. 
Use the chat history context and human input instruction to generate a cover letter customized for the job. \
If any message is negative for the job application, do not include it in the cover letter. \
If any information such as referrer and the time to start work are unknown, leave a placeholder for the user to fill in. \
keep the answer concise with a maximum of 4 paragraphs and 500 words.\
"""
cv_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", cv_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

user_file = open(args.user, "r")
user_input = user_file.read()

cv_chain = (
    cv_prompt
    | llm
    | StrOutputParser()
)

cover_letter = cv_chain.invoke({"input": user_input, "chat_history": chat_history})

# Save the written cover letter to output file
output_names = ["cover_letter", "_".join(job_name.strip().split()), "_".join(company_name.strip().split())]
output_file = '-'.join(output_names) + '.txt'
with open(output_file, "w") as f:
    f.writelines(cover_letter)
