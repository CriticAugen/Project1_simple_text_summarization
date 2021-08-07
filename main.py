import summary
url='https://en.wikipedia.org/wiki/Bill_Gates'
bot=summary.summary_bot(url)
summ=bot.summarize(10,20)
for sen in summ:
    print(sen)