# CultureAdventureAPI

## Endpoints

`GET /listbooks` Returns a list of available books <br>
Format: <br>
{ <br>
title: string, <br>
image: string (is the URL of the image), <br>
first page number : 1, <br>
} <br>


`GET /images?book=&img=` Returns a png image <br>
book: title of book <br>
img: name of img (main.png for cover img, 1.png for page 1, 2.png for page 2, etc) <br>


`POST /getpage` OR `GET /getpage?bookTitle=&page=` Returns details of page <br>
bookTitle: title of book the page belongs to <br>
page: page number/id needed <br>
Format: <br>
{ <br>
audio: string (URL of audio file) <br>
content: string (context of page) <br>
image: string (URL of image) <br>
options: [ <br>
    header: string, linkedPage: string (page number) <br>
  ] <br>
} <br>

## Important links
api hosted on: http://ai.bdp.blue/ (root has internal server error for the funni and to ward off trolls) (IP is 34.97.37.148)
access the mongodb server with this uri (don't share): mongodb://api:Team4096isthebest@34.87.15.250:37017 <br>

## Other info
also the config file for the apache is in /etc/apache2/sites-available/000-default.conf and the defalut-ssl.conf is for 443  <br>
