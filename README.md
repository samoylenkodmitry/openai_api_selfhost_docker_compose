# OpenAI API selfhosted with docker and docker-compose
This will allow you to host your own OpenAI API endpoint with predefined message
# Is it free?
You must obtain OpenAI API token first.
# Instructions
## Define token and message
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
vim DEFAULT_EMAIL # Edit lentsencrypt `DEFAULT_EMAIL`
```
Start nginx reverse-proxy if you not have one:
```
cd nginx
docker-compose up -d
```
Come back and start enpoint docker:
```
docker-compose up -d
```
