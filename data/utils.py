import json

class DataModule:
    def __init__(self, path) -> None:
        self.path = path
        self.test_cases = []
        self.labels = []
        
        self.process()
    
    def process(self):
        json_data = []
        
        with open(self.path, 'r') as f:
            for line in f:
                json_data.append(json.loads(line))

        
        for i in range(len(json_data)):
            self.test_cases.append(json_data[i]["question"] + " " + json_data[i]["options"][0] + " " + json_data[i]["options"][1] + " " + json_data[i]["options"][2] + " " + json_data[i]["options"][3] + " " + json_data[i]["options"][4]) 
            self.labels.append(json_data[i]["correct"])