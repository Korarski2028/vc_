from flask import Flask, request, render_template_string
import subprocess
import os

app = Flask(__name__)

@app.route("/")
def login_form():
    return '''
        <style>
            body {
                font-family: sans-serif;
                background-color: #f2f2f2;
            }
            h1 {
                text-align: center;
            }
            form {
                background-color: #ffffff;
                border: 1px solid #dddddd;
                padding: 20px;
                width: 300px;
                margin: 0 auto;
                margin-top: 20px;
            }
            input[type=text], input[type=password] {
                width: 100%;
                padding: 12px 20px;
                margin: 8px 0;
                display: inline-block;
                border: 1px solid #ccc;
                box-sizing: border-box;
            }
            input[type=submit] {
                background-color: #4CAF50;
                color: white;
                padding: 14px 20px;
                margin: 8px 0;
                border: none;
                cursor: pointer;
                width: 100%;
            }
        </style>
        <h1>Vmware Infra Script Tool</h1>
        <form action="/login" method="post">
            <label for="username">Username:</label><br>
            <input type="text" id="username" name="username"><br>
            <label for="password">Password:</label><br>
            <input type="password" id="password" name="password"><br><br>
            <input type="submit" value="Submit">
        </form> 
    '''

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    # For now, just print the credentials to the console
    print(f"Username: {username}, Password: {password}")
    
    with open("Scripts.txt", "r") as f:
        scripts = f.read().splitlines()

    return render_template_string('''
        <style>
            body {
                font-family: sans-serif;
                background-color: #f2f2f2;
            }
            h1 {
                text-align: center;
            }
            form {
                background-color: #ffffff;
                border: 1px solid #dddddd;
                padding: 20px;
                width: 400px;
                margin: 0 auto;
                margin-top: 20px;
            }
            input[type=text], textarea, select {
                width: 100%;
                padding: 12px 20px;
                margin: 8px 0;
                display: inline-block;
                border: 1px solid #ccc;
                box-sizing: border-box;
            }
            input[type=submit] {
                background-color: #4CAF50;
                color: white;
                padding: 14px 20px;
                margin: 8px 0;
                border: none;
                cursor: pointer;
                width: 100%;
            }
            .adhoc-button {
                background-color: #008CBA;
                color: white;
                padding: 5px 10px;
                border: none;
                cursor: pointer;
            }
        </style>
        <h1>Vmware Infra Script Tool</h1>
        <form action="/execute" method="post">
            <label for="vcenter_name">vCenter Name:</label><br>
            <input type="text" id="vcenter_name" name="vcenter_name">
            <button type="button" class="adhoc-button" onclick="addAdhocScript('vcenter_name')">Add-Hoc-Script</button><br><br>
            <label for="cluster_name">Cluster Name:</label><br>
            <input type="text" id="cluster_name" name="cluster_name">
            <button type="button" class="adhoc-button" onclick="addAdhocScript('cluster_name')">Add-Hoc-Script</button><br><br>
            <label for="server_list">Please enter server list:</label><br>
            <textarea id="server_list" name="server_list" rows="4" cols="50"></textarea>
            <button type="button" class="adhoc-button" onclick="addAdhocScript('server_list')">Add-Hoc-Script</button><br><br>
            
            <div id="adhoc-script-container"></div>

            <label for="script">Select a script:</label><br>
            <select id="script" name="script">
                {% for script in scripts %}
                <option value="{{ script }}">{{ script }}</option>
                {% endfor %}
            </select><br><br>
            
            <input type="submit" value="Send">
        </form>

        <script>
            function addAdhocScript(target) {
                const container = document.getElementById('adhoc-script-container');
                const existingTextarea = document.getElementById('adhoc_script');
                if (existingTextarea) {
                    return;
                }

                const textarea = document.createElement('textarea');
                textarea.id = 'adhoc_script';
                textarea.name = 'adhoc_script';
                textarea.rows = '10';
                textarea.cols = '50';
                textarea.placeholder = 'Paste your ad-hoc script here';
                
                const sendButton = document.createElement('button');
                sendButton.type = 'submit';
                sendButton.name = 'adhoc_submit';
                sendButton.value = 'send';
                sendButton.className = 'adhoc-button';
                sendButton.textContent = 'Send-Adhoc';

                container.appendChild(textarea);
                container.appendChild(sendButton);
            }
        </script>
    ''', scripts=scripts)



@app.route("/execute", methods=["POST"])
def execute():
    vcenter_name = request.form["vcenter_name"]
    cluster_name = request.form["cluster_name"]
    server_list = request.form["server_list"]
    script_name = request.form.get("script")
    adhoc_script = request.form.get("adhoc_script")
    adhoc_submit = request.form.get("adhoc_submit")

    with open("vCenter.txt", "w") as f:
        f.write(vcenter_name)
        
    with open("Cluster.txt", "w") as f:
        f.write(cluster_name)
        
    with open("Server_list.txt", "w") as f:
        f.write(server_list)
    
    script_path = ""
    if adhoc_submit:
        script_path = "ad-hoc.ps1"
        with open(script_path, "w") as f:
            f.write(adhoc_script)
        script_name = "ad-hoc.ps1"
    elif adhoc_script:
        script_path = "adhoc_script.ps1"
        with open(script_path, "w") as f:
            f.write(adhoc_script)
        script_name = "adhoc_script.ps1"
    else:
        script_path = f"{script_name}"
    
    try:
        powershell_command = ["pwsh", "-File", script_path]
        if adhoc_submit:
            powershell_command.extend(["-ScriptBlock", f''{adhoc_script}'''])
        elif vcenter_name:
            powershell_command.extend(["-vCenter", vcenter_name])
        if cluster_name:
            powershell_command.extend(["-Cluster", cluster_name])
        if server_list:
            powershell_command.extend(["-Target", f''{server_list}'''])
            
        result = subprocess.run(powershell_command, capture_output=True, text=True)
        output = result.stdout + result.stderr
        
        with open("Scripts.txt", "r") as f:
            scripts = f.read().splitlines()

        return render_template_string('''
            <style>
                body {
                    font-family: sans-serif;
                    background-color: #f2f2f2;
                }
                h1 {
                    text-align: center;
                }
                form {
                    background-color: #ffffff;
                    border: 1px solid #dddddd;
                    padding: 20px;
                    width: 400px;
                    margin: 0 auto;
                    margin-top: 20px;
                }
                input[type=text], textarea, select {
                    width: 100%;
                    padding: 12px 20px;
                    margin: 8px 0;
                    display: inline-block;
                    border: 1px solid #ccc;
                    box-sizing: border-box;
                }
                input[type=submit] {
                    background-color: #4CAF50;
                    color: white;
                    padding: 14px 20px;
                    margin: 8px 0;
                    border: none;
                    cursor: pointer;
                    width: 100%;
                }
                textarea#output {
                    background-color: black;
                    color: white;
                    font-family: monospace;
                    font-size: 1.2em;
                    height: 300px;
                }
            </style>
            <h1>Vmware Infra Script Tool</h1>
            <form action="/execute" method="post">
                <label for="vcenter_name">vCenter Name:</label><br>
                <input type="text" id="vcenter_name" name="vcenter_name" value="{{ vcenter_name }}"><br><br>
                <label for="cluster_name">Cluster Name:</label><br>
                <input type="text" id="cluster_name" name="cluster_name" value="{{ cluster_name }}"><br><br>
                <label for="server_list">Please enter server list:</label><br>
                <textarea id="server_list" name="server_list" rows="4" cols="50">{{ server_list }}</textarea><br><br>
                
                <div id="adhoc-script-container">
                    {% if adhoc_script %}
                    <textarea id="adhoc_script" name="adhoc_script" rows="10" cols="50">{{ adhoc_script }}</textarea>
                    {% endif %}
                </div>

                <label for="script">Select a script:</label><br>
                <select id="script" name="script">
                    {% for script in scripts %}
                    <option value="{{ script }}" {% if script == selected_script %}selected{% endif %}>{{ script }}</option>
                    {% endfor %}
                </select><br><br>
                
                <input type="submit" value="Send">
            </form>
            <br>
            <textarea id="output" readonly>{{ output }}</textarea>
            <br>
            <button id="copy-button">Copy to Clipboard</button>
            <button id="clear-button">Clear Console</button>

            <script>
                document.getElementById("copy-button").addEventListener("click", function() {
                    const outputText = document.getElementById("output").value;
                    navigator.clipboard.writeText(outputText).then(function() {
                        const button = document.getElementById("copy-button");
                        button.textContent = "Copied!";
                        setTimeout(function() {
                            button.textContent = "Copy to Clipboard";
                        }, 2000);
                    }, function(err) {
                        console.error("Could not copy text: ", err);
                    });
                });

                document.getElementById("clear-button").addEventListener("click", function() {
                    document.getElementById("output").value = "";
                });
            </script>
        ''', vcenter_name=vcenter_name, cluster_name=cluster_name, server_list=server_list, scripts=scripts, selected_script=script_name, output=output, adhoc_script=adhoc_script)

    except Exception as e:
        print(f"Error starting script: {e}")
        return f"Error starting script: {e}"
    finally:
        if adhoc_script and os.path.exists("adhoc_script.ps1"):
            os.remove("adhoc_script.ps1")
        if adhoc_submit and os.path.exists("ad-hoc.ps1"):
            os.remove("ad-hoc.ps1")



if __name__ == "__main__":
        app.run(debug=True)
