import time
import json
import telebot

##TOKEN DETAILS
TOKEN = "FCFA"

BOT_TOKEN = "5555491322:AAGlbXGRTo-nGDKAXBlyPy-ixzKepLboDUM"
PAYMENT_CHANNEL = "@MTNreferral" #add payment channel here including the '@' sign
OWNER_ID = 5270469995 #write owner's user id here.. get it from @MissRose_Bot by /id
CHANNELS = ["@MTNreferral"] #add channels to be checked here in the format - ["Channel 1", "Channel 2"] 
              #you can add as many channels here and also add the '@' sign before channel username
Daily_bonus =  250 #Put daily bonus amount here!
Mini_Withdraw = 20000  #remove 0 and add the minimum withdraw u want to set
Per_Refer = 1000 #add per refer bonus here

bot = telebot.TeleBot(BOT_TOKEN)

def check(id):
    for i in CHANNELS:
        check = bot.get_chat_member(i, id)
        if check.status != 'left':
            pass
        else:
            return False
    return True
bonus = {}

def menu(id):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('🆔 Compte')
    keyboard.row('🙌🏻 Parrainages', '🎁 Bonus', '💸 Solde')
    keyboard.row('⚙️ Définir le portefeuille', '📊Statistiques')
    bot.send_message(id, "*✅Vous avez bien rejoint les canaux*", parse_mode="Markdown",
                     reply_markup=keyboard)

@bot.message_handler(commands=['start'])
def start(message):
   try:
    user = message.chat.id
    msg = message.text
    if msg == '/start':
        user = str(user)
        data = json.load(open('users.json', 'r'))
        if user not in data['referred']:
            data['referred'][user] = 0
            data['total'] = data['total'] + 1
        if user not in data['referby']:
            data['referby'][user] = user
        if user not in data['checkin']:
            data['checkin'][user] = 0
        if user not in data['DailyQuiz']:
            data['DailyQuiz'][user] = "0"
        if user not in data['balance']:
            data['balance'][user] = 0
        if user not in data['wallet']:
            data['wallet'][user] = "none"
        if user not in data['withd']:
            data['withd'][user] = 0
        if user not in data['id']:
            data['id'][user] = data['total']+1
        json.dump(data, open('users.json', 'w'))
        print(data)
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(
           text='✅ Verifier', callback_data='check'))
        msg_start = "*🍔 Pour utiliser ce bot, vous devez rejoindre cette chaîne en cliquant sur ce lien 👉 - "
        for i in CHANNELS:
            msg_start += f"\n➡️ {i}\n"
        msg_start += "*"
        bot.send_message(user, msg_start,
                         parse_mode="Markdown", reply_markup=markup)
    else:

        data = json.load(open('users.json', 'r'))
        user = message.chat.id
        user = str(user)
        refid = message.text.split()[1]
        if user not in data['referred']:
            data['referred'][user] = 0
            data['total'] = data['total'] + 1
        if user not in data['referby']:
            data['referby'][user] = refid
        if user not in data['checkin']:
            data['checkin'][user] = 0
        if user not in data['DailyQuiz']:
            data['DailyQuiz'][user] = 0
        if user not in data['balance']:
            data['balance'][user] = 0
        if user not in data['wallet']:
            data['wallet'][user] = "none"
        if user not in data['withd']:
            data['withd'][user] = 0
        if user not in data['id']:
            data['id'][user] = data['total']+1
        json.dump(data, open('users.json', 'w'))
        print(data)
        markups = telebot.types.InlineKeyboardMarkup()
        markups.add(telebot.types.InlineKeyboardButton(
            text='✅ Verifier', callback_data='check'))
        msg_start = "*🍔 Pour utiliser ce bot, vous devez rejoindre cette chaîne en cliquant sur ce lien 👉 - \n➡️ @MTNreferral*"
        bot.send_message(user, msg_start,
                         parse_mode="Markdown", reply_markup=markups)
   except:
        bot.send_message(message.chat.id, "Cette commande ayant une erreur, veuillez attendre que le problème soit corrigé par l'administrateur")
        bot.send_message(OWNER_ID, "Votre bot a rencontré une erreur, corrigez-la rapidement!\n Error on command: "+message.text)
        return

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
   try:
    ch = check(call.message.chat.id)
    if call.data == 'check':
        if ch == True:
            data = json.load(open('users.json', 'r'))
            user_id = call.message.chat.id
            user = str(user_id)
            bot.answer_callback_query(
                callback_query_id=call.id, text=' ✅ Vous avez rejoint Maintenant, vous pouvez gagner de largent et partage le lien de parrainage pour gagner encore plus')
            bot.delete_message(call.message.chat.id, call.message.message_id)
            if user not in data['refer']:
                data['refer'][user] = True

                if user not in data['referby']:
                    data['referby'][user] = user
                    json.dump(data, open('users.json', 'w'))
                if int(data['referby'][user]) != user_id:
                    ref_id = data['referby'][user]
                    ref = str(ref_id)
                    if ref not in data['balance']:
                        data['balance'][ref] = 0
                    if ref not in data['referred']:
                        data['referred'][ref] = 0
                    json.dump(data, open('users.json', 'w'))
                    data['balance'][ref] += Per_Refer
                    data['referred'][ref] += 1
                    bot.send_message(
                        ref_id, f"*🏧Nouvelle recommandation au niveau 1, vous avez : +{Per_Refer} {TOKEN}*", parse_mode="Markdown")
                    json.dump(data, open('users.json', 'w'))
                    return menu(call.message.chat.id)

                else:
                    json.dump(data, open('users.json', 'w'))
                    return menu(call.message.chat.id)

            else:
                json.dump(data, open('users.json', 'w'))
                menu(call.message.chat.id)

        else:
            bot.answer_callback_query(
                callback_query_id=call.id, text='❌ Vous navez pas rejoint tous les canaux')
            bot.delete_message(call.message.chat.id, call.message.message_id)
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton(
                text='✅ Verifier', callback_data='check'))
            msg_start = "*🍔 Pour utiliser ce bot, vous devez rejoindre cette chaîne en cliquant sur ce lien 👉 - \n➡️ @MTNreferral*"
            bot.send_message(call.message.chat.id, msg_start,
                             parse_mode="Markdown", reply_markup=markup)
   except:
        bot.send_message(call.message.chat.id, "Cette commande ayant une erreur, veuillez attendre que le problème soit corrigé par l'administrateur")
        bot.send_message(OWNER_ID, "Votre bot a rencontré une erreur, corrigez-la rapidement!\n Error on command: "+call.data)
        return

@bot.message_handler(content_types=['text'])
def send_text(message):
   try:
    if message.text == '🆔 Compte':
        data = json.load(open('users.json', 'r'))
        accmsg = '*👮 Utilisateur : {}\n\n⚙️ Porte monnaie : *`{}`*\n\n💸 Solde : *`{}`* {}*'
        user_id = message.chat.id
        user = str(user_id)

        if user not in data['balance']:
            data['balance'][user] = 0
        if user not in data['wallet']:
            data['wallet'][user] = "none"

        json.dump(data, open('users.json', 'w'))

        balance = data['balance'][user]
        wallet = data['wallet'][user]
        msg = accmsg.format(message.from_user.first_name,
                            wallet, balance, TOKEN)
        bot.send_message(message.chat.id, msg, parse_mode="Markdown")
    if message.text == '🙌🏻 Parrainages':
        data = json.load(open('users.json', 'r'))
        ref_msg = "*⏯️ Total Invites : {} Utilisateurs\n\n👥 Système de parrainage\n\n1 Level:\n🥇 Level°1 - {} {}\n\n🔗 Lien de référence Partagez pour recevoir rapidement de gain⬇️\n{}*"

        bot_name = bot.get_me().username
        user_id = message.chat.id
        user = str(user_id)

        if user not in data['referred']:
            data['referred'][user] = 0
        json.dump(data, open('users.json', 'w'))

        ref_count = data['referred'][user]
        ref_link = 'https://telegram.me/{}?start={}'.format(
            bot_name, message.chat.id)
        msg = ref_msg.format(ref_count, Per_Refer, TOKEN, ref_link)
        bot.send_message(message.chat.id, msg, parse_mode="Markdown")
    if message.text == "⚙️Définir le portefeuille":
        user_id = message.chat.id
        user = str(user_id)

        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('🚫 Annuler')
        send = bot.send_message(message.chat.id, "_⚠️Envoyez votre numéro  MTN dans le format international  Exemple: au cameroun (+237xxxxxxxxx)._",
                                parse_mode="Markdown", reply_markup=keyboard)
        # Next message will call the name_handler function
        bot.register_next_step_handler(message, trx_address)
    if message.text == "🎁 Bonus":
        user_id = message.chat.id
        user = str(user_id)
        cur_time = int((time.time()))
        data = json.load(open('users.json', 'r'))
        #bot.send_message(user_id, "*🎁 Bonus Button is Under Maintainance*", parse_mode="Markdown")
        if (user_id not in bonus.keys()) or (cur_time - bonus[user_id] > 60*60*24):
            data['balance'][(user)] += Daily_bonus
            bot.send_message(
                user_id, f"Félicitations vous venez de recevoir {Daily_bonus} {TOKEN}")
            bonus[user_id] = cur_time
            json.dump(data, open('users.json', 'w'))
        else:
            bot.send_message(
                message.chat.id, "❌*Vous ne pouvez prendre le bonus qu'une fois toutes les 24 heures!*",parse_mode="markdown")
        return

    if message.text == "📊Statistiques":
        user_id = message.chat.id
        user = str(user_id)
        data = json.load(open('users.json', 'r'))
        msg = "*📊 Total members : {} Users\n\n🥊 Retrait total réussi : {} {}*"
        msg = msg.format(data['total'], data['totalwith'], TOKEN)
        bot.send_message(user_id, msg, parse_mode="Markdown")
        return

    if message.text == "💸 Solde":
        user_id = message.chat.id
        user = str(user_id)

        data = json.load(open('users.json', 'r'))
        if user not in data['balance']:
            data['balance'][user] = 0
        if user not in data['wallet']:
            data['wallet'][user] = "none"
        json.dump(data, open('users.json', 'w'))

        bal = data['balance'][user]
        wall = data['wallet'][user]
        if wall == "none":
            bot.send_message(user_id, "_❌ portefeuille Non défini_",
                             parse_mode="Markdown")
            return
        if bal >= Mini_Withdraw:
            bot.send_message(user_id, "_Enter Your Amount_",
                             parse_mode="Markdown")
            bot.register_next_step_handler(message, amo_with)
        else:
            bot.send_message(
                user_id, f"_❌Votre solde bas, vous devriez avoir au moins {Mini_Withdraw} {TOKEN} dans votre Solde_", parse_mode="Markdown")
            return
   except:
        bot.send_message(message.chat.id, "Cette commande ayant une erreur, veuillez attendre que le problème soit corrigé par l'administrateur")
        bot.send_message(OWNER_ID, "Votre bot a rencontré une erreur, corrigez-la rapidement !\n Erreur lors de la commande "+message.text)
        return

def trx_address(message):
   try:
    if message.text == "🚫 Annuler":
        return menu(message.chat.id)
    if len(message.text) == 34:
        user_id = message.chat.id
        user = str(user_id)
        data = json.load(open('users.json', 'r'))
        data['wallet'][user] = message.text

        bot.send_message(message.chat.id, "*💹Votre portefeuille  réglé sur " +
                         data['wallet'][user]+"*", parse_mode="Markdown")
        json.dump(data, open('users.json', 'w'))
        return menu(message.chat.id)
    else:
        bot.send_message(
            message.chat.id, "*⚠️ Ce n'est pas une adresse  valide!*", parse_mode="Markdown")
        return menu(message.chat.id)
   except:
        bot.send_message(message.chat.id, "Cette commande ayant une erreur, veuillez attendre que le problème soit corrigé par l'administrateur")
        bot.send_message(OWNER_ID, "Votre bot a rencontré une erreur, corrigez-la rapidement !\n Erreur lors de la commande: "+message.text)
        return

def amo_with(message):
   try:
    user_id = message.chat.id
    amo = message.text
    user = str(user_id)
    data = json.load(open('users.json', 'r'))
    if user not in data['balance']:
        data['balance'][user] = 0
    if user not in data['wallet']:
        data['wallet'][user] = "none"
    json.dump(data, open('users.json', 'w'))

    bal = data['balance'][user]
    wall = data['wallet'][user]
    msg = message.text
    if msg.isdigit() == False:
        bot.send_message(
            user_id, "_📛 Valeur invalide. Saisir uniquement une valeur numérique. Essaye encore_", parse_mode="Markdown")
        return
    if int(message.text) < Mini_Withdraw:
        bot.send_message(
            user_id, f"_❌ Retrait minimal {Mini_Withdraw} {TOKEN}_", parse_mode="Markdown")
        return
    if int(message.text) > bal:
        bot.send_message(
            user_id, "_❌ Vous ne pouvez pas retirer plus que votre solde_", parse_mode="Markdown")
        return
    amo = int(amo)
    data['balance'][user] -= int(amo)
    data['totalwith'] += int(amo)
    bot_name = bot.get_me().username
    json.dump(data, open('users.json', 'w'))
    bot.send_message(user_id, "✅* Le retrait est demandé automatiquement à notre propriétaire\n\n💹 Payment Channel :- "+PAYMENT_CHANNEL +"*", parse_mode="Markdown")

    markupp = telebot.types.InlineKeyboardMarkup()
    markupp.add(telebot.types.InlineKeyboardButton(text='🍀 BOT LINK', url=f'https://telegram.me/{bot_name}?start={OWNER_ID}'))

    send = bot.send_message(PAYMENT_CHANNEL,  "✅* Nouveau Retrait\n\n⭐ Amount - "+str(amo)+f" {TOKEN}\n🦁 User - @"+message.from_user.username+"\n💠 Wallet* - `"+data['wallet'][user]+"`\n☎️ *Références d'utilisateurs = "+str(
        data['referred'][user])+"\n\n🏖 Lien bot - @"+bot_name+"\n⏩ Veuillez patienter, notre propriétaire le confirmera*", parse_mode="Markdown", disable_web_page_preview=True, reply_markup=markupp)
   except:
        bot.send_message(message.chat.id, "Cette commande ayant une erreur, veuillez attendre que le problème soit corrigé par l'administrateur")
        bot.send_message(OWNER_ID, "Votre bot a rencontré une erreur, corrigez-la rapidement !\n Erreur lors de la commande: "+message.text)
        return

if __name__ == '__main__':
    bot.polling(none_stop=True)
