from models import *
from dingtalkchatbot.chatbot import DingtalkChatbot, ActionCard, FeedLink, CardItem

secret  = 'SEC25326438ad0cf300f9c5c0ed0d834548a378a7ad2db7151f155c37d377c5c738'
webhook = 'https://oapi.dingtalk.com/robot/send?access_token=021613341a77f023b55d7928185ba2a017da06514496263cc6652a35b6b8ffbd'

dt_bot  = DingtalkChatbot(webhook, secret=secret)

def notification(model):
    link = "http://www.qihuofy.com/article?id=%s" % model.article_id
    button = [CardItem(title=model.submit_date, url=link)]
    content = noti_content(model)
    action = ActionCard(title='您有新的文章评论', text= content, btns=button, btn_orientation=1, hide_avatar=1)
    dt_bot.send_action_card(action)

def noti_content(model):
    contact = model.name
    if len(model.contact) > 0:
        contact = '%s(%s)' %(model.name,model.contact)
    return '![图片](https://www.helloimg.com/images/2021/02/07/bbe23e79762d4c9ba1fae9c3a051a76b8f3485c22d8151e6.jpg) \n#### %s：%s' %(contact, model.comment)

if __name__ == "__main__":
    model = CommentModel()
    model.article_id = "234"
    model.name = "张三"
    model.contact = ""
    model.comment = "期货如何返佣？"
    model.submit_date = "2021-02-10"
    notification(model)

