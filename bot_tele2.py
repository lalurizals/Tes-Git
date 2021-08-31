import telebot
import base64
from PIL import Image
import io
import requests
import psycopg2
import json
from datetime import datetime
import random
import string
import hashlib
import time

from telebot.types import MessageEntity

tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


API_TOKEN = '1854541892:AAH4yOIjQuu0t6qJsbUztoYwSwoAhN6Weks'
bot = telebot.TeleBot(API_TOKEN)

#connect to the DB
mydb = psycopg2.connect (
                host = "pgsql",
                user = "postgres",
                password = "*R4h4s14d0nk#",
                database = "pelanggan"
)

#cursor
cursor = mydb.cursor()

@bot.message_handler(func=lambda message: True)
def handle_all_message(message):
    #bot.reply_to(message, message.text)
    #print(message)
    print(message.text)
    if message.text == 'Help' or message.text == 'help':
        
        bot.send_message(message.chat.id,"Halo " + str(message.from_user.username) + ".. Silahkan foto dan kirim struk belanja anda") 
        file_id_sticker = 'CAACAgIAAxkBAAPYYPef2_CT4tQprLEcmjjfrRxZKCsAAtgBAAJWnb0KmNR_KWfOQDkgBA'
        bot.send_sticker(message.chat.id, file_id_sticker)

@bot.message_handler(content_types=['photo'])
def handle_photo_message(message):
   file_info = bot.get_file(message.photo[-1].file_id)
   file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(API_TOKEN, file_info.file_path))

   chatid = str(message.from_user.id)
   username = str(message.from_user.username)
   firstname = str(message.from_user.first_name)
   lastname = str(message.from_user.last_name)

   print(chatid)
   print(username)
   print(firstname)
   print(lastname)

   timestamp = str(time.time())
   print(timestamp)
   waktu = str(time.ctime())
   print(waktu)

   kode = timestamp + chatid + username
   print(kode)
   kodefix = hashlib.md5(kode.encode()).hexdigest()
   print(kodefix)
    
   filefix = file.content
   filefix2 = base64.b64encode(filefix)

   cursor.execute("insert into public.laporan (chatid, username, firstname, lastname, gambar, kode, tanggal) values (%s, %s, %s, %s, %s, %s, %s)", (chatid, username, firstname, lastname, filefix2, kodefix, tanggal))
   mydb.commit()
   
   image = Image.open(io.BytesIO(filefix))
   #image.show()

   bot.send_message(message.chat.id, "Terimaksih telah mengirim")

@bot.message_handler(content_types=['sticker'])
def handle_sticker(message):
    print(message)
    file_id_sticker = 'CAACAgIAAxkBAAPYYPef2_CT4tQprLEcmjjfrRxZKCsAAtgBAAJWnb0KmNR_KWfOQDkgBA'
    bot.send_sticker(message.chat.id, file_id_sticker)
    
bot.polling()