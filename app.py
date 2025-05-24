from flask import Flask, render_template, request, redirect, send_from_directory
import os
import datetime

app = Flask(__name__)
CONFIG_FOLDER = 'configs'
os.makedirs(CONFIG_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        host = request.form['host']
        port = request.form['port']
        user = request.form['user']
        password = request.form['password']
        sni = request.form['sni']
        payload = request.form['payload']
        name = request.form['name']

        # Create .npv-like config content (custom format)
        content = f"""[NPV-CONFIG]
Host: {host}
Port: {port}
User: {user}
Password: {password}
SNI: {sni}
Payload: {payload}
Generated: {datetime.datetime.now()}
"""

        filename = f"{name.replace(' ', '_')}.npv"
        filepath = os.path.join(CONFIG_FOLDER, filename)
        with open(filepath, 'w') as f:
            f.write(content)

        return redirect('/configs')
    return render_template('create.html')

@app.route('/configs')
def list_configs():
    files = os.listdir(CONFIG_FOLDER)
    return render_template('configs.html', files=files)

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(CONFIG_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
