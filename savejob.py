import argparse

parser = argparse.ArgumentParser(description="Take inputs from user to collect job position information")
parser.add_argument("--file", "-f", required=True, help="The path to load your pdf resume file")
parser.add_argument("--url", "-u", required=True, help="The url to the job page")
parser.add_argument("--key", "-k", required=True, help="The user key for the foundation model")
parser.add_argument("--model", "-m", default="gpt-3.5-turbo", choices=["gpt-3.5-turbo", "gpt-4"],
                    help="The foundation model you want to select to complete the task")
args = parser.parse_args()


import os
os.environ["OPENAI_API_KEY"] = args.key

from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
loader = AsyncChromiumLoader([args.url])
html = loader.load()

from langchain_community.document_transformers import Html2TextTransformer
html2text = Html2TextTransformer()
html_transformed = html2text.transform_documents(html)

from langchain_text_splitters import RecursiveCharacterTextSplitter
chunk_size = 1000
chunk_overlap = 30
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=chunk_size, chunk_overlap=chunk_overlap
)
splits = text_splitter.split_documents(html_transformed)

from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_anthropic import ChatAnthropic
vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

import bs4
from langchain import hub
# prompt = hub.pull("rlm/rag-prompt")
llm = ChatOpenAI(model_name=args.model, temperature=0)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, CommaSeparatedListOutputParser, JsonOutputParser
from langchain_core.output_parsers.openai_functions import JsonOutputFunctionsParser

# question cannot be answered using the information provided answer with "N/A".

template = """
System: 
You are an applicant for a job. Based on the job description in the {context}. 
You collect information to answer {question}.
If you don't know the answer, say "N/A". Keep the answer succinct.

User: What's the title of the position? 
AI: Research Scientist

User: What's the working location of the position?
AI: Davis, CA

User: What's the degree requirement of the position?
AI: Bachelor's

User: How many years of working experience required by the position?
AI: 3

User: What's the salary range of the position?
AI: $10,000/month to $12,000/month

User: Does the company sponsor a working visa?
AI: No

User: Does the company requires citizenship?
AI: Yes

User: What's experience level of the position?
AI: Senior

Context: {context}

User: {question}

AI: """

prompt = ChatPromptTemplate.from_template(template)

retriever = vectorstore.as_retriever()
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

questions = [
"What's the name of the company or institution? Give me only the name.",
"What's the title of the position? Give me only the name of the title.",
"What's the working location of the position? Give me a short answer.",
"What's the degree requirement of the position? Answer in one word.",
"How many years of working experience or new graduate is required by the position? Answer in numbers.",
"What's the salary range of the position? Answer in numbers.",
"Does the company sponsor a working visa? Answer yes or no.",
"Does the company requires citizenship? Answer yes or no.",
"What's experience level of the position? For example, intern, full-time, senior, and so on. Answer in one word.",
]

csvRow = [rag_chain.invoke(question) for question in questions]
csvRow.append(args.url)

import csv
path = "job-record.csv"

fields = ["company", "position", "location", "degree requirement", "working years", "salary range", "sponsorship", "citizenship", "experience level", "link"]
if not os.path.isfile(path):
    with open(path,'w') as f:
        writer = csv.writer(f)
        writer.writerow(fields)

with open(path,'a') as f:
    writer = csv.writer(f)
    writer.writerow(csvRow)

