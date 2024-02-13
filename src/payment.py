import json

def record_payment(num_input_token, num_output_token, curr_price_dollar):
    with open("src/receipt.json", "r") as f:
        record = json.load(f)
    
    renewed_num_input_token = record["total_input_token"] + num_input_token
    renewed_num_output_token = record["total_output_token"] + num_output_token
    record["total_input_token"] = renewed_num_input_token
    record["total_output_token"] = renewed_num_output_token
    
    renewed_price_dollar = record["total_price_dollar"] + curr_price_dollar
    renewed_price_won = record["total_price_won"] + (curr_price_dollar * 1340)
    record["total_price_dollar"] = renewed_price_dollar
    record["total_price_won"] = renewed_price_won
    
    with open("src/receipt.json", "w", encoding='utf-8') as fix:
        json.dump(record, fix, indent='\t')
        
    with open("src/receipt.json", "r") as f:
        renewed_record = json.load(f)
    
    return renewed_record["total_price_dollar"]

def print_cost(num_input_token, num_output_token):
    # Price of gpt-3.5-turbo-0125
    per_input_price = 0.0000005
    per_output_price = 0.0000015
    currency_dollar = 1340
    
    curr_input_price_dollar = num_input_token * per_input_price
    curr_output_price_dollar = num_output_token * per_output_price

    total_price_dollar = record_payment(num_input_token, num_output_token, curr_input_price_dollar + curr_output_price_dollar)
    print(f"Current cost($): ${curr_input_price_dollar + curr_output_price_dollar:.7f}, Current cost(won): {(curr_input_price_dollar + curr_output_price_dollar) * currency_dollar:.7f}원")
    print(f"Total cost($): ${total_price_dollar:.7f}, Total cost(won): {total_price_dollar * currency_dollar:.7f}원")

if __name__ == "__main__":
    #%%
    import json

    with open("src/receipt.json", "r") as f:
        data = json.load(f)

    data["total_input_token"] = 0

    #%%
    with open("src/receipt.json", "w", encoding='utf-8') as fix:
        json.dump(data, fix, indent='\t')