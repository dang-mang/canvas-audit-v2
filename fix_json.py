import os
def fix_json(input_filename, output_filename):
    with open(input_filename) as f:
        newText=f.read().replace('}{', '},\n{')
    with open(input_filename, "w") as f:
        f.write(newText)
    
    os.system(f"python3 json_to_csv.py l {input_filename} {output_filename}")
