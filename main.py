from telegram.ext import Updater, MessageHandler, Filters, ConversationHandler
from telegram.ext import CommandHandler
import find_name
import parsing_pdf
import octopart


def work_with_octopart(dck_pnm, max_len, lst_not_type):
    all_text = []
    sum_inf = 0
    if max_len[0] > 6:
        for max_el in max_len:
            key_type = find_dck_len(max_el, dck_pnm)
            inf_type, s = octopart.get_inf_PN(dck_pnm[key_type][1:], True)
            if inf_type is not None:
                all_text.append(inf_type)
                sum_inf += s
            del dck_pnm[key_type]
            if max_el < 6:
                break
    else:
        inf, s = octopart.get_inf_PN(lst_not_type)
        all_text.append(inf)
        sum_inf += s

    return all_text, sum_inf


def find_dck_len(len_type, dck):
    for key in dck:
        if len(dck[key]) == len_type:
            return key
    return None


def start(update, context):
    # markup = ReplyKeyboardMarkup([['/PN'], ['/OCTOPART']], one_time_keyboard=False)
    update.message.reply_text("Отправьте файл со спецификации электронных компонентов в формате PDF")
    return 1


def read_file(update, context):
    context.bot.get_file(update.message.document).download()
    # writing to a custom file
    with open("file_0.pdf", 'wb') as f:
        context.bot.get_file(update.message.document).download(out=f)

    fail_pdf = open("numbers_files", encoding='UTF-8')
    nums = int(fail_pdf.read()) + 1
    new_inf(nums)

    parsing_fail = parsing_pdf.Parsing()
    name_fail = f'file_{nums}.pdf'
    clean_fail = parsing_fail.read_pdf(name_fail)

    if clean_fail is None or len(clean_fail) == 0:
        update.message.reply_text('Не смог распознать электронные компоненты в отправленном файле')
        return 1
    update.message.reply_text('Я получил файл и все данные отсортировал')

    dck_PN, lst_not_type, len_types = find_name.test(clean_fail)
    all_inf, s = work_with_octopart(dck_PN, len_types, lst_not_type)

    if s > 5:
        fl = True
    else:
        fl = False

    l = 0
    for i in all_inf:
        for j in i:
            if l == 5 and fl:
                break
            update.message.reply_text(j)
            l += 1

    update.message.reply_text(f'Было выслано {l} Part Numbers из {s}')
    return 1


def error(update, context):
    update.message.reply_text('')


def new_inf(nums):
    fail_pdf = open("numbers_files", 'w')
    print(nums, file=fail_pdf)
    fail_pdf.close()


def main():
    BOT_TOKEN = '5525985364:AAHhrVKr3DwjaV7hTARLVfQUtB8xmWAGetE'

    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # updater.dispatcher.add_handler(MessageHandler(Filters.document, read_file))
    start_dialog = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            1: [MessageHandler(Filters.document, read_file)],
        },
        fallbacks=[CommandHandler('menu', start)])
    dp.add_handler(start_dialog)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
