from data.utils import DataModule
from .prompt import (Rationale,
                    Output,)

path = "data/test.json"
dataModule = DataModule(path)

rationale = Rationale()
rationale_outputs = rationale(dataModule.test_cases[0], 5)

output = Output()
consistent_output = output(dataModule.test_cases[0], rationale_outputs)

print(consistent_output)
print(dataModule.labels[0])

import pdb; pdb.set_trace()