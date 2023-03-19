# OpenAI API selfhosted with docker and docker-compose
This will allow you to host your own OpenAI API endpoint with predefined message
# Is it free?
You must obtain [OpenAI API token](https://platform.openai.com/account/api-keys) first.
# Setup
## Define token and message
By default message asks to do code or git diff review.
```
git clone 
vim app.py # define `api_key` and change `messages`
```
## Build docker image
This must be done after each `app.py` edit.
```
docker build -t code_review_app .
```
## Define your url address
This config uses docker shared network from another docker-compose.yml nginx reverse-proxy image.
```
vim docker-compose.yml # change `VIRTUAL_HOST`, `LETSENCRYPT_HOST`, `LETSENCRYPT_EMAIL`
docker-compose up -d
```
Start nginx reverse-proxy if you not have one:
```
cd nginx
vim docker-compose.yml # Edit lentsencrypt `DEFAULT_EMAIL`
docker-compose up -d
```

# Usage

```
curl -X POST -F "code_text=YOU_CODE_HERE_TO_REVIEW" https://YOU_URL_HERE/review
```

like this:

```
curl -X POST -F "code_text=import os
import openai
from flask import Flask, request, jsonify
app = Flask(__name__)

# Set up OpenAI API key
openai.api_key = 'sk-'

def review_code(code_text):
    reviews = []

    # Split code text into 8000-character parts
    code_parts = [code_text[j:i+8000] for i in range(0, len(code_text), 8000)]

    for part in code_parts:
        try:
            response = openai.ChatCompletion.create(
                engine='gpt-3.5-turbo',
                messages=[{"role": "user", "content": f"Please review the following code and provide feedback if there are any issues. Otherwise, please respond with 'ok':\n{part}\nReview:"}],
                temperature=0.1,
            )
        except Exception ass e:
            print('Error during API call:', str(e))
            raise e

        reviews.append(response.choices[0].message.content)

    return '\\n'.join(reviews)

@app.route('/review', methods=['POST'])
def review_endpoint():
    code_text = request.form['code_text']
    review = review_code(code_text)
    return jsonify({'review': review})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)" https://YOU_URL_HERE/review
```
