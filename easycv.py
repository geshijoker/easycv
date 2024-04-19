import argparse

parser = argparse.ArgumentParser(description="Take inputs from user to generate a cover letter")
parser.add_argument("--resume", required=True, help="The path to load your pdf resume file")
parser.add_argument("--jd", default='files/jd.txt', help="The path to load the job description txt file")
parser.add_argument("--key", "-k", required=True, help="The user key for the foundation model")
parser.add_argument("--model", "-m", default="gpt-3.5-turbo", choices=["gpt-3.5-turbo", "gpt-4"],
                    help="The foundation model you want to select to complete the task")
args = parser.parse_args()

import os
os.environ["OPENAI_API_KEY"] = args.key

from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

job_name = input('The name of the job: ')
company_name = input('The name of the company: ')

jd_file = open(args.jd, "r")
job_description = jd_file.read()

chunk_size = 1000
chunk_overlap = 30
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=chunk_size, chunk_overlap=chunk_overlap
)
jd_splits = text_splitter.split_text(job_description)
print(len(jd_splits))
for split in jd_splits:
    print('---------------------------------')
    print(split)

# from langchain_community.vectorstores import Chroma
# from langchain_openai import ChatOpenAI, OpenAIEmbeddings
# from langchain_anthropic import ChatAnthropic
# vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

# import bs4
# from langchain import hub
# # prompt = hub.pull("rlm/rag-prompt")
# llm = ChatOpenAI(model_name=args.model, temperature=0)

# def format_docs(docs):
#     return "\n\n".join(doc.page_content for doc in docs)

# from langchain_core.runnables import RunnablePassthrough
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser, CommaSeparatedListOutputParser, JsonOutputParser
# from langchain_core.output_parsers.openai_functions import JsonOutputFunctionsParser

# # question cannot be answered using the information provided answer with "N/A".

# template = """
# System: 
# You are an applicant for a job. Based on the job description in the {context}. 
# You collect information to answer {question}.
# If you don't know the answer, say "N/A". Keep the answer succinct.
# List them in JSON style.

# User: What's the title of the position? 
# AI: Research Scientist

# User: What's the working location of the position?
# AI: Davis, CA

# User: What's the degree requirement of the position?
# AI: Bachelor's

# User: How many years of working experience required by the position?
# AI: 3

# User: What's the salary range of the position?
# AI: $10,000/month to $12,000/month

# User: Does the company sponsor a working visa?
# AI: No

# User: Does the company requires citizenship?
# AI: Yes

# User: What's experience level of the position?
# AI: Senior

# Context: {context}

# User: {question}

# AI: """

# prompt = ChatPromptTemplate.from_template(template)

# retriever = vectorstore.as_retriever()
# rag_chain = (
#     {"context": retriever | format_docs, "question": RunnablePassthrough()}
#     | prompt
#     | llm
#     | StrOutputParser()
# )


"What experiences meets the required "


"Tell us a little bit about you and why you think you would be a good fit at Stripe? "
