from const import API_KEY
from openai import OpenAI
from .payment import print_cost

client = OpenAI(api_key=API_KEY)

class Rationale:
    def __init__(self) -> None:
        self.prompt = None
        
    def __call__(self, test_case: str, sample_num: int) -> list:
        self.setup_prompt(test_case)
        rationale_list = []
        
        response = client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages=self.prompt,
                temperature=0.3,
                max_tokens=256,
                n=sample_num,
                seed=42,
            )

        print_cost(response.usage.prompt_tokens, response.usage.completion_tokens)
        
        for i in range(sample_num):
            rationale_list.append(response.choices[i].message.content)
        
        return rationale_list
    
    def setup_prompt(self, test_case: str) -> None:
        self.prompt = [
            {
                "role": "system",
                "content": "You are an expert of mathematics. So, you are good at solving mathematic problems. Your task is to reason to solve the given problem. Your response should be always rationale for solving the given problem. Don't provide final answer, just output your rationale."
            },
            {
                "role": "user",
                "content": "John found that the average of 15 numbers is 40. If 10 is added to each number then the mean of the numbers is? Answer Choices: A)50 B)45 C)65 D)78 E)64"
            },
            {
                "role": "assistant",
                "content": "If 10 is added to each number, then the mean of the numbers also increases by 10. So the new mean would be 50."
            },
            {
                "role": "user",
                "content": "If a/b = 3/4 and 8a + 5b = 22,then find the value of a. Answer Choices: A)1/2 B)3/2 C)5/2 D)4/2 E)7/2"
            },
            {
                "role": "assistant",
                "content": "If a/b = 3/4,then b = 4a/3. So 8a + 5(4a/3) = 22. This simplifies to 8a + 20a/3 = 22,which means 44a/3 = 22. So a is equal to 3/2."
            },
            {
                "role": "user",
                "content": "A person is traveling at 20 km/hr and reached his destiny in 2.5 hr then find the distance? Answer Choices: A)53 km B)55 km C)52 km D)60 km E)50 km"
            },
            {
                "role": "assistant",
                "content": "The distance that the person traveled would have been 20 km/hr * 2.5 hrs = 50 km."
            },
            {
                "role": "user",
                "content": "How many keystrokes are needed to type the numbers from 1 to 500? Answer Choices: A)1156 B)1392 C)1480 D)1562 E)1788"
            },
            {
                "role": "assistant",
                "content": "There are 9 one-digit numbers from 1 to 9. There are 90 two-digit numbers from 10 to 99. There are 401 three-digit numbers from 100 to 500. 9 + 90(2) + 401(3) = 1392."
            },
            {
                "role": "user",
                "content": f"{test_case}"
            },
        ]
        
class Output:
    def __init__(self) -> None:
        self.prompts = []
        
    def __call__(self, test_case: str, rationale_list: list) -> str:
        self.setup_prompt(test_case, rationale_list)
        
        for i in range(len(rationale_list)):
            output_dict = {}
            prompt = self.prompts[i]
            
            response = client.chat.completions.create(
                        model="gpt-3.5-turbo-0125",
                        messages=prompt,
                        temperature=0.3,
                        max_tokens=256,
                        n=1,
                        seed=42,
                    )
            
            print_cost(response.usage.prompt_tokens, response.usage.completion_tokens)
        
            key = response.choices[0].message.content[14:][0]
            
            if key not in output_dict.keys():
                output_dict[key] = 1
            else:
                output_dict[key] += 1
        
        consistent_output, _ = sorted(output_dict.items(), reverse=True, key=lambda x : x[1])[0]
        
        return consistent_output
    
    def setup_prompt(self, test_case, rationale_list) -> None:
        messages = [
            {
                "role": "system",
                "content": "You are an expert of mathematics. So, you are good at solving mathematic problems. Your task is to answer to the given problem based on the given rationale. Your output always begin with 'The answer is '"
            },
            {
                "role": "user",
                "content": "John found that the average of 15 numbers is 40. If 10 is added to each number then the mean of the numbers is? Answer Choices: A)50 B)45 C)65 D)78 E)64\nIf 10 is added to each number, then the mean of the numbers also increases by 10. So the new mean would be 50."
            },
            {
                "role": "assistant",
                "content": "The answer is A."
            },
            {
                "role": "user",
                "content": "If a/b = 3/4 and 8a + 5b = 22,then find the value of a. Answer Choices: A) 1/2 B) 3/2 C) 5/2 D) 4/2 E) 7/2\nIf a/b = 3/4,then b = 4a/3. So 8a + 5(4a/3) = 22. This simplifies to 8a + 20a/3 = 22,which means 44a/3 = 22. So a is equal to 3/2."
            },
            {
                "role": "assistant",
                "content": "The answer is B."
            },
            {
                "role": "user",
                "content": "A person is traveling at 20 km/hr and reached his destiny in 2.5 hr then find the distance? Answer Choices: A)53 km B)55 km C)52 km D)60 km E)50 km\nThe distance that the person traveled would have been 20 km/hr * 2.5 hrs = 50 km."
            },
            {
                "role": "assistant",
                "content": "The answer is E."
            },
            {
                "role": "user",
                "content": "How many keystrokes are needed to type the numbers from 1 to 500? Answer Choices: A)1156 B)1392 C)1480 D)1562 E)1788\nThere are 9 one-digit numbers from 1 to 9. There are 90 two-digit numbers from 10 to 99. There are 401 three-digit numbers from 100 to 500. 9 + 90(2) + 401(3) = 1392."
            },
            {
                "role": "assistant",
                "content": "The answer is B."
            },
            {
                "role": "user",
                "content": ""
            },
        ]
        
        for rationale in rationale_list:
            messages[-1]["content"] = test_case + "\n" + rationale
            self.prompts.append(messages)