from data.utils import DataModule
from .prompt import (Rationale,
                    Output,)

path = "data/test.json"
dataModule = DataModule(path)
consistent_output_list = []
score = 0

for i in range(len(dataModule.test_cases)):
    rationale = Rationale()
    rationale_outputs = rationale(dataModule.test_cases[i], 5)

    for j in range(len(rationale_outputs)):
        output = Output()
        consistent_output = output(dataModule.test_cases[i], rationale_outputs[j])
        
        consistent_output_list.append(consistent_output)
        
for pred, label in zip(consistent_output_list, dataModule.labels):
    if pred == label:
        score += 1

print(score / len(dataModule.labels))

import pdb; pdb.set_trace()