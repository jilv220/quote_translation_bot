#!/bin/bash
pkg_name=${PWD##*/} 
cp -r ./ /opt/${pkg_name}
chmod +w -R /opt/${pkg_name}/*

cp twitter-bot.service.example twitter-bot.service
sed -i "s/PWD/${pkg_name}/g" twitter-bot.service
cp twitter-bot.service /etc/systemd/user/twitter-bot.service
cp twitter-bot.timer.example /etc/systemd/user/twitter-bot.timer

rm twitter-bot.service