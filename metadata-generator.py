import os
import os.path
import shutil
template = """
    {{
        "id": {id},
        "line_numbers": [],
        "dependencies": [],
        "language": "python",
        "test_framework": "pytest",
        "test_script": "run_test",
        "test_timeout": 5,
        "bug_type": "Test Failure",
        "subject": "{subject}",
        "bug_id": "{bug_id}",
        "source_file": "solution.py",
        "failing_test_identifiers": [{failing_test_identifiers}],
        "passing_test_identifiers": [{passing_test_identifiers}],
        "count_neg": {failing_test_identifiers_count},
        "count_pos": {passing_test_identifiers_count},
        "pub_test_script": "run_public_tests",
        "pvt_test_script": "run_private_tests",
        "root_abspath": "/experiment/{subject}/{bug_id}/src",
        "entrypoint": {
            "file": "solution.py",
        },
    }},
"""

root = os.getcwd()

file = open("meta-data.candidate.json", "w")
file.write("[")
id = 0
skipper = ""
for subject in sorted(os.listdir('./')):
    if os.path.isfile(subject) or subject in ['testcases', 'crawler', 'configs', 'target'] or subject.startswith('.'):
        continue
    
    # if not subject.startswith(skipper):
    #      continue
    # else:
    #      skipper = "NONE"
    
    for bug_id in sorted(os.listdir(subject)):
        if os.path.isfile(os.path.join(subject,bug_id)) or bug_id == ".aux" or bug_id == "base":
            continue
        id = id + 1

        shutil.copy(os.path.join(root, 'run_test_local'),
                    os.path.join(subject, bug_id, 'run_test'))
        os.chdir(os.path.join(subject, bug_id))

        passing_test_identifiers = []
        failing_test_identifiers = []
        print("I AM IN {}".format(os.getcwd()))
        for test in sorted(os.listdir("src")):
            if "test" not in test:
                continue
            test_file = test
            
            
            res = os.system("./run_test '{}'".format(test))
            # print(res)
            if res == 0:
                passing_test_identifiers.append(test)
            else:
                failing_test_identifiers.append(test)

        # input()
        os.chdir(root)
        shutil.copy(os.path.join(root, 'run_test'),
                    os.path.join(subject, bug_id, 'run_test'))

        file.write(template.format(subject=subject,
                                   id=id,
                                   bug_id=bug_id,
                                   passing_test_identifiers=','.join(map(lambda x : f'"{x}"',passing_test_identifiers)),
                                   failing_test_identifiers=','.join(map(lambda x : f'"{x}"',failing_test_identifiers)),
                                   failing_test_identifiers_count=len(failing_test_identifiers),
                                   passing_test_identifiers_count=len(passing_test_identifiers)
                                   ))

file.write("]")
file.close()
