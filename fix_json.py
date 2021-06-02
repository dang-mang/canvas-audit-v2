import os
import sys
def fix_json(input_filename, directory = "data/", output_filename = "output.csv"):
    output_path = directory + output_filename
    remove_empty_lines(input_filename)
    with open(input_filename) as f:
        #newText=f.read().replace('}{', '},\n{').replace("]\n[",",").replace(",\n]","\n]")
        newText=f.read().replace('[', '').replace("]","").replace('}\n{','},\n{').replace('}{', '},\n{').replace(',\n,',',\n')
        newText= "[{0}]".format(newText)

    with open(input_filename, "w") as f:
        f.write(newText)
    
    os.system(f"python3 json_to_csv.py l {input_filename} {output_path}")

def remove_empty_lines(filename):
    """Overwrite the file, removing empty lines and lines that contain only whitespace."""
    with open(filename, 'r+') as f:
        lines = f.readlines()
        f.seek(0)
        f.writelines(line for line in lines if line.strip())
        f.truncate()

def main():
    print(sys.argv[1])
    fix_json(sys.argv[1])

if __name__ == "__main__":
    # execute only if run as a script
    main()

