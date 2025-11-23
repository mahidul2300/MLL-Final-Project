from flask import Flask, render_template, request
import joblib 

app = Flask(__name__)


try:
    model = joblib.load("model.pkl")
    vectorizer = joblib.load("vectorizer.pkl")
except Exception as e:
    print(f"Error loading model or vectorizer: {e}")
    
    exit() 


CUSTOM_BLOCK_LIST = [
    "youteube.com", 
    "paypai.com",   
    "logln.net"
    "faecbook.login",  
]

CUSTOM_WHITE_LIST = [
    "www.facebook.com", 
    "www.amazon.com",   
    "www.whatsapp.web"
    "www.youtube.com",  
]


def normalize_url(url):
    
    url = url.strip()
    
    if not url.startswith("http://") and not url.startswith("https://"):
        return "http://" + url
    return url

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    url = ""

    if request.method == "POST":
        input_url = request.form.get("url", "")
        
        if input_url:
            
            url = input_url
            processed_url = normalize_url(input_url)
            
            
            is_blocked = False
            for blocked_domain in CUSTOM_BLOCK_LIST:
                if blocked_domain in processed_url:
                    result = "🚨 Phishing Website! (Fake)"
                    is_blocked = True
                    break
            
            if is_blocked:
                
                pass
            else:
                
                try:
                    features = vectorizer.transform([processed_url]) 
                    pred = model.predict(features)[0]

                    if pred == 1:
                        result = "🚨 Phishing Website! (Fake)"
                    else:
                        result = "✅ URL Looks Secure! (Real)"
                except Exception as e:
                    
                    result = f"Error processing URL: {e}"
                    print(f"Prediction Error: {e}")
        else:
            result = "Please enter a URL to check." 

    return render_template("index.html", result=result, url=url)

if __name__ == "__main__":
    
    print("Web app starting on http://127.0.0.1:8000/")
    app.run(debug=True, port=8000)