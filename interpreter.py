import re

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
                var_value = var_value.replace("shari", "True").replace("thett", "False")
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

            condition = condition.replace("shari", "True").replace("thett", "False")


            for var in variables:
                condition = condition.replace(var, str(variables[var]))

            try:
                condition_result = bool(eval(condition, {}, {}))
            except:
                condition_result = False

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
                        var_value = var_value.replace("shari", "True").replace("thett", "False")
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
