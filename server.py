from flask import Flask, request, jsonify
import re

app = Flask(__name__)

def execute_malayalam_code(code):
    variables = {} 
    lines = [line.strip() for line in code.splitlines() if line.strip()]

    if lines[0] != "namaskaram;" or lines[-1] != "nanni namaskaram;":
        return "Error: Program must start with 'namaskaram;' and end with 'nanni namaskaram;'"
    
    output = []
    i = 1  
    
    while i < len(lines) - 1:
        line = lines[i]
      
        var_match = re.match(r'ithu\s+(\w+)\s*=\s*(.+);', line)
        if var_match:
            var_name, var_value = var_match.groups()
            try:
                variables[var_name] = eval(var_value, {}, variables)  
            except:
                variables[var_name] = var_value.strip('"')  
            i += 1
            continue

        print_match = re.match(r'parayuu\s+"(.+?)";', line)
        if print_match:
            output.append(print_match.group(1))
            i += 1
            continue

        if_match = re.match(r'enkil\s*\((.+?)\)\s*\{', line)
        if if_match:
            condition = if_match.group(1)
            try:
                condition_result = eval(condition, {}, variables)  # Directly evaluate using variables
            except Exception as e:
                return f"Error in condition: {condition} -> {e}"

            if_block = []
            i += 1
            while i < len(lines) - 1 and lines[i] != "}":
                if_block.append(lines[i])
                i += 1
            i += 1 

            else_block = []
            if i < len(lines) - 1 and lines[i] == "illenkil{":
                i += 1
                while i < len(lines) - 1 and lines[i] != "}":
                    else_block.append(lines[i])
                    i += 1
                i += 1  

            selected_block = if_block if condition_result else else_block
            for blk_line in selected_block:
            
                var_match = re.match(r'ithu\s+(\w+)\s*=\s*(.+);', blk_line)
                if var_match:
                    var_name, var_value = var_match.groups()
                    try:
                        variables[var_name] = eval(var_value, {}, variables)
                    except:
                        variables[var_name] = var_value.strip('"')
                    continue
        
                print_match = re.match(r'parayuu\s+"(.+?)";', blk_line)
                if print_match:
                    output.append(print_match.group(1))
            continue

        return f"Error: Unknown statement - {line}"

    return "\n".join(output)

@app.route("/execute", methods=["POST"])
def execute():
    data = request.get_json()
    code = data.get("code", "")
    
    result = execute_malayalam_code(code)
    
    return jsonify({"output": result})

if __name__ == "__main__":
    app.run(debug=True)
