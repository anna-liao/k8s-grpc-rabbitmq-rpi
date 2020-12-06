# REST=${REST:-"localhost:5000"}
REST=localhost
url=$(shuf -n 1 ../all-image-urls.txt)
echo $url
python rest-client.py $REST url "$url" 1