# easycv
The app to create a cover letter based on the job description and your resume with LangChain + LLM
This is the v0.0 version of the project.

# Installation
```console
foo@bar:~$ cd easycv
foo@bar:easycv$ pip install -e .
```

# Usage Example
```console
foo@bar:easycv$ python easycv.py --resume files/resume.pdf --jd files/jd.txt --user files/user_cv_prompt.txt -m gpt-3.5-turbo
```
Users will be asked to provide your OpenAI key.
Users can modify the resume (pdf, txt, doc), job description (e.g. jd.txt), and user input instruction (e.g. user_cv_prompt.txt) to guide the cover letter writting.

# Design
The tool uses OpenAI ChatGPT as the LLM to generate a cover letter.
The difficulty in this project is: beyond a single RAG system, how to find the matching information between the job description and the resume of the user.
I use a two-phase RAG QA to save the related contents in the chat history which is fed to the LLM along with user instructions to generate a cover letter.
![Design Diagram](https://github.com/geshijoker/easycv/blob/main/easycv.drawio.svg)

# Features that are in development
- The Google Chrome extension user interface
- The REST API to call the backend "easycv" python script
- Add an agent ask the user follow-up questions and use Google search tool
