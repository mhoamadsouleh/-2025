
from flask import Flask, request, render_template, redirect, url_for
import os
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file and file.filename.endswith('.py'):
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return redirect(url_for('index'))

@app.route('/run/<filename>')
def run(filename):
    subprocess.Popen(["python3", os.path.join(UPLOAD_FOLDER, filename)])
    return redirect(url_for('index'))

@app.route('/stop/<filename>')
def stop(filename):
    os.system("pkill -f " + os.path.join(UPLOAD_FOLDER, filename))
    return redirect(url_for('index'))

@app.route('/delete/<filename>')
def delete(filename):
    os.remove(os.path.join(UPLOAD_FOLDER, filename))
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
