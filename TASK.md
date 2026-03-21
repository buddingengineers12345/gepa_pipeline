Create a folder 

./data with following files 
train.csv
test.csv
seed_prompt.txt

train.csv and test.csv must contain two columns 
'input' and 'output'

seed_prompt.txt must contain the initial prompt the user will be giving 

Write following python scripts 
- src/constants.py (Contains the key constants that needs to modified) such as task_lm, reflection_lm and so on 
- src/data_analysis.py (Does a detailed analysis of the data and creates a detailed report in .text format)
- src/optimization.py (runs the actual prompt optimization and returns the generated high quality prompt)
- pipeline.sh (that runs analysis or optimization or both)

all logs must be written to reports/ folder

Keep code minimal.

## Reference
Sample snippet for reference.
"""
import gepa

trainset, valset, _ = gepa.examples.aime.init_dataset()

seed_prompt = {
    "system_prompt": "You are a helpful assistant. Answer the question. "
                     "Put your final answer in the format '### <answer>'"
}

result = gepa.optimize(
    seed_candidate=seed_prompt,
    trainset=trainset,
    valset=valset,
    task_lm="openai/gpt-4.1-mini",
    max_metric_calls=150,
    reflection_lm="openai/gpt-5",
)

print("Optimized prompt:", result.best_candidate['system_prompt'])
""" 

## Reference
temp/ folder for reference. Do not copy paste the code and content. 