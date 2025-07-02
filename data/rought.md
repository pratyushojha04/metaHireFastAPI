backend.csv,cloud engineer.csv,data analyst.csv,devops.csv,frontend development.csv,machine learning.csv,tester.csv




I have 
backend.csv,cloud engineer.csv,data analyst.csv,devops.csv,frontend development.csv,machine learning.csv,tester.csv
in data folder ,each with columns (id,question,answer,company(Google, Amazon, Meta, Netflix, TCS, Infosys),role(SDE, Machine Learning Engineer, Frontend Dev, Backend Dev, Fullstack, Data Scientist, Data Analyst)),difficulty(Easy, Medium, Hard),category())
use fastapi backend create use mongodb trasfer these data in csv to mongo db .with all the columns intact .

also create a logic to extarct the questions randomly in the below formate 

request ->
{
    "role" : [SDE, Machine Learning Engineer, Frontend Dev, Backend Dev, Fullstack, Data Scientist, Data Analystogle, Amazon, Meta, Netflix, TCS, Infosys],
    "level" : "fresher", // fresher or experienced both will get same questions beacouse theoritical questions are same for all .
    "company" : [Google, Amazon, Meta, Netflix, TCS, Infosys],
    "resumeText" : " " // we can not process without llm
}
response ->
{
"id":[list of ids of all 8 questions in order as questions,and id of 2 coding question]

    "questions" : [
list of 8 random  questions 

    ],

    [list of 2 coding question in order as questions, and id of 2 coding question each containing (question,problem_description,company,difficulty,category,hint)]
    
}


request ->
{
    "id" : [
list of 8 questions sended in previous response and 2 coding questions sended in previous response in order as questions
    "language" : "python
    ],
    "answers" : [
answer given by user for all 8 qustiosn in sequence and code written by user in the str formate 

    ],
}
response ->
{
    "score" : 15,
    //check the correctness of code on the basis of testcases using ouput of user code and our testcases saved in the database and give give marks out 15 (10 for theory , 5 for coding 0.5 for each testcases )
    "feedback" : ""// for now hard coded feedback
}
to calculate score we will use cosine similarity using id we can get the actual answer and campare with user anwer .
while selecting the random questions below will be the input and based on which you will select the random questions 
design the api