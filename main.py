import os
import discord
import requests
import json 
import random
import re
from replit import db
from keep_alive import keep_alive

client = discord.Client()

sad_words = ["sad","depressed","unhappy","miserable","depressing","alone naturally"]
ct = ["horny","nut"]
a = ["mornin","Morning","Mornin","morning"]
b = ["Good morning","Mornin","mornin","Indeed"]
c = ["<@!295244555148591106>","<@295244555148591106>","<@&903902509985316884>"]
d = ["Calm down and wait","He will respond soon, please wait"]
e = ["Gg"]
f = ["valo","brawl"]
g = ["Ruk mai bhi ping karta hu sale ko <@!295244555148591106>","ok calm down no spam please"]


starter_encouragements = [
  "Hang in there","You are a great person ","keep calm n keep herr goin","OP bolte chaddi kholte"
]


if "responding" not in db.keys():
  db["responding"] = True


def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements =db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragement(index):
  encouragements = db["encouragements"]
  if len(encouragements)> index:
    del encouragements[index]
    db["encouragements"] = encouragements



@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
@client.event
async def on_message(message):
  if message.author == client.user:
    return
  msg = message.content
  #print(msg)
  if message.content.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)
  if msg.startswith("$discourage"):
    await message.channel.send("Get a life")

  if db["responding"]: 
    options = starter_encouragements
    if "encouragements" in db.keys():
      options.extend(db["encouragements"])

      
    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))
    if any(word in msg for word in ct):
      await message.channel.send("||https://www.youtube.com/watch?v=8cKQfWLrjJk||")
    if any(word in msg for word in a):
      await message.channel.send(random.choice(b))
    #if any(word in msg for word in c):
      #await message.channel.send(random.choice(d))
    if any(word in msg for word in e):
      await message.channel.send("Well played, gg indeed")
    if any(word in msg for word in f):
      await message.channel.send("Pro tip: Grind on gettin some bitches too")
    if any(word in msg for word in c):
      await message.channel.send(random.choice(g))
    #if re.search("gg",msg):
      #await message.channel.send("Well played, gg! ")
    
    
    
    

  if msg.startswith("$new"):
    encouraging_message = msg.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added")

  if msg.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del",1)[1])
      delete_encouragement(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)
  if msg.startswith("$list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("$responding"):
    value = msg.split("$responding ",1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off")
      
keep_alive()
client.run(os.environ['TOKEN'])