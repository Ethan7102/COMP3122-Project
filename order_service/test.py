import json

data = '{"test":[{"1":"2","3":"4"}],"test2":"3"}'
data = json.loads(data)
print(data["test"][0])