import time
import sys
import re
from python_graphql_client import GraphqlClient
from pprint import pprint
import requests
import openai
import os
from os.path import join
import openai
import time
MAX_TOKENS = 1024
SOLUTIONS = 5

MAVEN_TEMPLATE="""
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
         <modelVersion>4.0.0</modelVersion>

         <groupId>com.aprcomp</groupId>
         <artifactId>aprcomp_ai_java</artifactId>
         <version>1.0-SNAPSHOT</version>

         <properties>
         <maven.compiler.source>8</maven.compiler.source>
         <maven.compiler.target>8</maven.compiler.target>
         </properties>
         
         <dependencies>
            <dependency>
                <groupId>junit</groupId>
                <artifactId>junit</artifactId>
                <version>4.12</version>
                <scope>test</scope>
            </dependency>
         </dependencies>
</project>  """

def completion_openAI(
        prompt, max_tokens=1024, temperature=0, num=1,model="gpt-4"
        ):
    openai.api_key = ("")
    response = openai.ChatCompletion.create(
            model=model,
            messages = [
                {"role": "system", "content": "You are an expert algorithmic problem solver, which autocompletes function definitions and outputs the contents of the function in triple backticks (```) without responding with any other text." },
                {"role": "user", "content": prompt},
                ],
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=1.0,
            n=num,
            )
    return response


# Instantiate the client with an endpoint.
client = GraphqlClient(endpoint="https://leetcode.com/graphql/")

contest_query = """
query pastContests($pageNo: Int, $numPerPage: Int) {
pastContests(pageNo: $pageNo, numPerPage: $numPerPage) {
 pageNum
 currentPage
 totalNum
 numPerPage
 data {
  titleSlug
  startTime
  originStartTime
  }
 }
}
"""
contest_root = "https://leetcode.com/contest/api/info/{}"
problem_root = "https://leetcode.com/contest/{}/problems/{}/"

variables = {
        "pageNo": 1,
        "numPerPage": 120,
        }

data = client.execute(query=contest_query, variables=variables)

problem_query = """ query questionContent($titleSlug: String!) {
question(titleSlug: $titleSlug) {
content
difficulty
questionFrontendId
codeSnippets {
            lang
            langSlug
            code
        }
topicTags {
            name
        }
}
}
"""

full_query = """
query ($title_slug: String) {
    question(title_slug: $title_slug) {
        questionId
        questionFrontendId
        boundTopicId
        title
        titleSlug
        content
        translatedTitle
        translatedContent
        isPaidOnly
        difficulty
        likes
        dislikes
        isLiked
        similarQuestions
        exampleTestcases
        contributors {
            username
            profileUrl
            avatarUrl
        }
        topicTags {
            name
            slug
            translatedName
        }
        companyTagStats
        stats
        hints
        solution {
            id
            canSeeDetail
            paidOnly
            hasVideoSolution
            paidOnlyVideo
        }
        status
        sampleTestCase
        metaData
        judgerAvailable
        judgeType
        mysqlSchemas
        enableRunCode
        enableTestMode
        enableDebugger
        envInfo
        libraryUrl
        adminUrl
        challengeQuestion {
            id
            date
            incompleteChallengeCount
            streakCount
            type
        }
        note
    }
}
"""

from bs4 import BeautifulSoup


def python_process(problem_slug,problem_info, problem_description, snippets,difficulty=0):
    folder = "python"
    instance = join(folder,str(difficulty),"{}_{}".format(problem_slug,int(time.time())))
    os.makedirs(instance)
    python_snippet = {}
    for snippet in snippets:
        if snippet["lang"] == "Python3":
            python_snippet = snippet
            break
        # print(python_snippet)
    if not python_snippet["code"].startswith("class Solution"):
        ## skip the cases with special classes as this is difficult
        print("\n\n\nSKIP")
        return
    function_name = re.search(
            "class Solution:\n    def (.*)\(", python_snippet["code"]
            ).group(1)
    #print(function_name)

    examples = problem_description.split("Example")[1:]
    tests = []
    for id, example in enumerate(examples):
        inp = re.search("Input: (.*)\n", example).group(1).replace("null", "None")
        out = re.search("Output: (.*)\n", example).group(1).replace("null", "None")
        #print(inp, out)
        test = f"import solution\n\ndef test_{id}():\n\tassert solution.Solution().{function_name}({inp}) == {out}"
        tests.append(test)
        #print(test)
    prompt = '"""python\n {} """\n{}'.format(
            problem_description, python_snippet["code"]
            )

    description = '"""python\n {} """\n'.format(
            problem_description
            )
    while True: 
        try:
            completions = completion_openAI(
                    prompt,
                    num=SOLUTIONS,
                    max_tokens=MAX_TOKENS,
                    temperature=0.8,
                    model="gpt-4",
                    )["choices"] + completion_openAI(
                    prompt,
                    num=SOLUTIONS,
                    max_tokens=MAX_TOKENS,
                    temperature=0.8,
                    model="gpt-3.5-turbo",
                    )["choices"] 
            #print(completions)
            break
        except openai.error.RateLimitError as e:
            print("Sleep")
            time.sleep(60)
        except Exception as e:
            print("Got exception")
            print(e)
            sys.exit(1)

    for id,completion in enumerate(completions):
        completion_folder = "{}_{}".format(problem_slug,id)
        print("Making ",id)
        os.mkdir(join(instance,completion_folder))
        try:
            code = completion.message.content.split('```')[1]
            if code.startswith('python\n'):
                code = code[len('python\n'):]
            if not code.startswith('class'):
                code = python_snippet['code'] + code
            program_text = "from typing import *\n" + description + code
            with open(join(instance,completion_folder,"solution.py"), "w") as f:
                f.write(program_text)
                f.flush()
            with open(join(instance,completion_folder,"description.txt"), "w") as f:
                f.write(problem_description)
                f.flush()
            for id,test in enumerate(tests):
                with open(join(instance,completion_folder,"test_{}.py".format(id)),"w") as f:
                    f.write(test)
                    f.flush()
        except Exception as e:
            pass
        # print("")

id = 0
skipper = len(sys.argv) >1
for contest in data["data"]["pastContests"]["data"]:
    contest_data = requests.get(contest_root.format(contest["titleSlug"])).json()[
            "questions"
            ]
    for question in contest_data:
        id = id + 1
        if id > 2:
            print("DONEEE")
            sys.exit(0)
        problem_slug = question["title_slug"]
        print(problem_slug)
        if skipper and  problem_slug == sys.argv[1]:
            skipper = False
        if skipper:
            print("SKIP")
            continue
        problem_url = problem_root.format(contest["titleSlug"], question["title_slug"])
        problem_info = client.execute(
                query=problem_query, variables={"titleSlug": question["title_slug"]}
                )
        #print(problem_info["data"]["question"]["exampleTestcases"])
        problem_description = BeautifulSoup(
                re.sub('<sup>(.*?)</sup>',' ** \\1',problem_info["data"]["question"]["content"]), features="lxml"
                ).get_text()
        difficulty = problem_info["data"]["question"]["difficulty"]
        tags = problem_info["data"]["question"]["topicTags"]
        #pprint(tags)
        snippets = problem_info["data"]["question"]["codeSnippets"]
        #print(problem_description)
        print("Ready to process")
        python_process(problem_slug,problem_info, problem_description, snippets,difficulty)
        print("Python done")

        #input()

# requests.get(contest_root+"")
