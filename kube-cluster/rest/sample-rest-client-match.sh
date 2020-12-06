# REST=${REST:-"localhost:5000"}
REST=localhost

python rest-client.py $REST url https://storage.googleapis.com/cu-csci-5253/lfw/Zico/Zico_0003.jpg 10
#
# match above
#
python rest-client.py $REST match 215a00cf1bc966348bbd55aa0c8a8b82d1636a68e7d60fdf790329e2 10
#
# no match above
#
python rest-client.py $REST match fb82e0120bbf3a26b38f6d939cb510f3ead0aa98b0afdfc972ea277e 10