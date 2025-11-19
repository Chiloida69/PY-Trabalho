from flask import Flask, render_template
import os
from supabase import create_client, Client
# Initialize Supabase client
url: str = os.environ.get("https://dsbdurojqeclyncssnek.supabase.co")
key: str = os.environ.get("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRzYmR1cm9qcWVjbHluY3NzbmVrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM1NjA0MzksImV4cCI6MjA3OTEzNjQzOX0.U6OZ2b2Vws4fAjt4jrgQXlMHC1r00phCq5jaumKPu0c")   
supabase: Client = create_client(url, key)
# Initialize Flask app
app = Flask(__name__)

@app.route('/testgratis.html')
def main():
    return render_template('testgratis.html')
@app.route('/templates/cadastro.html')
def cadastro():
    return render_template('cadastro.html')

if __name__ == '__main__':
    app.run(debug=True)
