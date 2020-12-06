#!/bin/sh

REST=localhost

echo GET humidity
curl http://$REST/sensor/humidity
echo GET temp
curl http://$REST/sensor/temp
echo GET pressure
curl http://$REST/sensor/pressure