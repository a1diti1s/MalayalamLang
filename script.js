function runCode() {
    let code = document.getElementById("code-editor").value.trim();
    let output = document.getElementById("output");
    output.textContent = ""; 

    if (code === "") {
        output.textContent = "Error: No code entered.";
        return;
    }

    let lines = code.split("\n").map(line => line.trim());
    if (lines[0] !== "namaskaram;" || lines[lines.length - 1] !== "nanni namaskaram;") {
        output.textContent = "Error: Program must start with 'namaskaram;' and end with 'nanni namaskaram;'";
        return;
    }

    let variables = {};
    let insideIfBlock = false;
    let conditionMet = false;
    let insideElseBlock = false;

    for (let i = 1; i < lines.length - 1; i++) {
        let line = lines[i];

        let printMatch = line.match(/parayuu\s+"(.+?)";/);
        if (printMatch) {
            if (!insideIfBlock || conditionMet || insideElseBlock) {
                output.textContent += printMatch[1] + "\n";
            }
            continue;
        }
        let varMatch = line.match(/ithu\s+(\w+)\s*=\s*(.+);/);
        if (varMatch) {
            let varName = varMatch[1];
            let varValue = varMatch[2].trim();


            if (!isNaN(varValue)) {
                varValue = Number(varValue);
            } else if (varValue.startsWith('"') && varValue.endsWith('"')) {
                varValue = varValue.slice(1, -1); 
            } else {
                output.textContent += `Error: Invalid value assignment - ${varValue}\n`;
                return;
            }

            variables[varName] = varValue;
            continue;
        }

        let ifMatch = line.match(/enkil\s*\((.+)\)\s*{/);
        if (ifMatch) {
            let condition = ifMatch[1];

            try {

                condition = condition.replace(/\b(\w+)\b/g, match => 
                    variables[match] !== undefined ? variables[match] : match
                );
                conditionMet = eval(condition);
                insideIfBlock = true;
            } catch (error) {
                output.textContent += "Error: Invalid condition - " + condition + "\n";
                return;
            }
            continue;
        }

        if (line === "illenkil{") {
            insideElseBlock = !conditionMet; 
            continue;
        }

        if (line === "}") {
            insideIfBlock = false;
            insideElseBlock = false;
            conditionMet = false;
            continue;
        }
        output.textContent += "Error: Unknown statement - " + line + "\n";
    }
}
