# REST=${REST:-"localhost:5000"}
REST="localhost"
url=$(shuf -n 1 ../all-image-urls.txt)
curl -d "{\"url\":\"$url\"}" -H "Content-Type: application/json" -X POST http://$REST/scan/url