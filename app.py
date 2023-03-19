
import os
import openai
from flask import Flask, request, jsonify

app = Flask(__name__)

# Set up OpenAI API key
openai.api_key = "YOUR_OPENAI_TOKEN"

def review_code(code_text):
    reviews = []

    # Split code text into 8000-character parts
    code_parts = [code_text[i:i+8000] for i in range(0, len(code_text), 8000)]

    for part in code_parts:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content":"You are a very experienced software engineer. You love to do code reviews and spot bugs in a code or git diffs or just file diffs. Furthermore, you pay very close attention. If you spot one error, you pay attention to other errors even more. You don't make up errors if they are not present."},
                    {"role": "user", "content": f"Please review the following code or diff and provide feedback if there are any issues. If it is a diff, lines started with - are removed, and + are added. If this is a diff it can include resulting file, that is ok. If it includes diff, it will be two parts old and new, you review only new. If diff includes two parts, you only review second. Also, if diff is ok just repond 'ok'. Find all errors. If you found one, try to find another. Otherwise, please respond with just 'ok'. If code is ok say just 'ok', do not say anything else. If two-parted diff resulting in good code, just say 'ok'. Do not repeat what changes are made.:\n{part}"}],
                temperature=0.22,
            )
        except Exception as e:
            print("Error during API call:", str(e))
            raise e

        reviews.append(response.choices[0].message.content)

    return "\n".join(reviews)

@app.route('/review', methods=['POST'])
def review_endpoint():
    code_text = request.form['code_text']
    review = review_code(code_text)
    return jsonify({"review": review})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
