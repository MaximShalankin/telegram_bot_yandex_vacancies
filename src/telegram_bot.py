def telegram_bot(token):
    
    """This tg bot helps track vacancies in Yandex company
    
    """
    
    import telebot
    import time
    from telebot import types
    import sys
    import os
    
    
    parent_dir = os.path.dirname(os.getcwd()) # For correct work with path
    path_logs = os.path.join(parent_dir, 'logging')
    path_functions = os.path.join(parent_dir, 'src')
    sys.path.insert(0, path_logs) # Here log file
    sys.path.insert(0, path_functions) # Here main functions
    
    from functions import read_logs, write_logs, get_new_vacancies, check_log_changes, result_explanation
    
    bot = telebot.TeleBot(token, threaded=False)
    
    @bot.message_handler(func=lambda message: True)
    def greetings(message):
        user = message.text

        keyboard = types.InlineKeyboardMarkup()
        key_ml = types.InlineKeyboardButton(text='Machine Learning', callback_data='ML')
        key_other = types.InlineKeyboardButton(text='Не хочу в ML', callback_data='piece_of')
        keyboard.add(key_ml)
        keyboard.add(key_other)

        bot.reply_to(message, 'Привет, я могу показать тебе текущие вакансии в Яндексе по тегу', reply_markup=keyboard)
  

    @bot.callback_query_handler(func=lambda call: True)
    def callback_worker(call):
        if call.data == "ML":

            check_log_changes(path_logs)
            date, vacancies, vacancies_new, vacancies_deleted = result_explanation(path_logs, tag='machinelearning')
            vacancies = '✅ ' + ' \n\n✅ '.join(i for i in vacancies)

            bot.send_message(call.from_user.id, f'На {date} доступны следующие вакансии:')
            bot.send_message(call.from_user.id, vacancies) 

            if vacancies_new:
                vacancies_new = '🌟 ' + ' \n\n🌟 '.join(i for i in vacancies_new)
                bot.send_message(call.from_user.id, 'Появились новые вакансии: ')
                bot.send_message(call.from_user.id, vacancies_new) 

            else:
                bot.send_message(call.from_user.id, 'Нет новых вакансий') 

            if vacancies_deleted:
                vacancies_deleted = '❌ ' + ' \n\n❌ '.join(i for i in vacancies_deleted)
                bot.send_message(call.from_user.id, 'Были удалены следующие вакансии: ')
                bot.send_message(call.from_user.id, vacancies_deleted) 

            else:
                bot.send_message(call.from_user.id, 'Нет удалённых вакансий') 



            msg = bot.send_message(call.from_user.id, 'Вот так вот')      
            bot.register_next_step_handler(msg, greetings)

        elif call.data == "piece_of":
            msg = bot.send_message(call.from_user.id, 'kek все хотят 😜')
            bot.register_next_step_handler(msg, greetings)
            
    return bot


def main():
    TOKEN = ... # place your TOKEN here
    tg_bot = telegram_bot(TOKEN)
    tg_bot.polling(none_stop=True)


if __name__ == '__main__':  
    main()