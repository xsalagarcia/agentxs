import re

user_input = '/set_path "/home/xevi/Documepts/Projectes/cli-llm/agentxs"'
matches = re.match(r'(?P<command>/set_path)\s+"(?P<path>[\w\s./\\-]+)"', user_input)
print(matches)