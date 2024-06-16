curl --location "http://127.0.0.1:8000/signup/" --header "Content-Type: application/json" --data-raw "{\"email\": \"test@test.com\", \"password\": \"123\"}"
curl --location "http://127.0.0.1:8000/signin/" --header "Content-Type: application/json" --data-raw "{\"email\": \"test@test.com\", \"password\": \"123\"}"
curl --location "http://127.0.0.1:8000/me/" --header "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo3LCJleHAiOjE3MTg3MjU5NTl9.QHZFsl72ipu5qj-oT7-eHXA41gQjmmddnjVx2DI57ok"
