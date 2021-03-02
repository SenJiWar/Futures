
class PageInfoModel:
    title = ""
    navi_title = ""
    content = ""
    keywords = ""

    def __init__(self,title):
        self.title = title
    
class NaviItemModel:
    id=""
    name=""
    link=""
    sup_id=""
    create_date=""
    childItems = []

    @classmethod
    def initWith(self,res):
        item = NaviItemModel()
        item.id = res[0]
        item.name = res[1]
        item.link = res[2]
        item.sup_id =res[3]
        item.create_date = res[4]
        return item
    
    def super_title(self):
        if self.sup_id == 0:
            return self.name
        elif self.sup_id == 1:
            return "期货居间人"
        elif self.sup_id == 2:
            return "期货居间返佣"
        elif self.sup_id == 3:
            return "期货居间合作"
        elif self.sup_id == 4:
            return "居间常见问题"
        else:
            return ""
        
class ArticleModel:
    id = ''
    title = ""
    author = ""
    createtime = ""
    content = ""
    article_tags = ''
    sub_title = ''
    is_hot = 0
    thumbnail = ''
    is_index = 0
    classify = ""
    vcount = 0
    keywords = ""
    modify_date = ""
    is_top = 0

    @classmethod
    def initWith(self,res):
        article = ArticleModel()
        article.id = res[0]
        article.title = res[1]
        article.author = res[2]
        article.createtime = res[3]
        article.content = res[4]
        article.article_tags = res[5]
        article.is_hot = res[6]
        article.sub_title = res[7]
        article.thumbnail = res[8]
        article.is_index = res[9]
        article.classify = res[10]
        article.vcount = res[11]
        article.keywords = res[12]
        article.is_top = res[14]
        return article
    
    def tags(self):
        return self.article_tags.split(";")

    def formatDate(self):
        index = self.createtime.find(" ")
        if index != -1:
            sub = self.createtime[0:index]
            array = sub.split("-")
            return array[1]+"-"+array[2]
        else:
            return ""

    def html_content(self):
        return self.content.replace("&quot;","'")

    def __str__(self):
        aa = '标题：' + self.title + '\n'
        bb = '作者：' + self.author + '\n'
        cc = '创建时间：' + self.createtime + '\n'
        dd = "文章内容：" + self.content + "\n"
        ee = '文章类型：' + self.article_tags + "\n"
        gg = '是否热门：' + str(self.is_hot) + '\n'
        return aa + bb + cc + dd + ee + gg

class LinkModel:
    id = ""
    name = ""
    url = ""
    create_date = ""

    @classmethod
    def initWith(self,res):
        link = LinkModel()
        link.id = res[0]
        link.name = res[1]
        link.url = res[2]
        link.create_date = res[3]
        return link

class FocusModel:
    id = ""
    title = ""
    image = ""
    url = ""
    create_date = ""

    @classmethod
    def initWith(self,res):
        focus = FocusModel()
        focus.id = res[0]
        focus.title = res[1]
        focus.image = res[2]
        focus.url = res[3]
        focus.create_date = res[4]
        return focus

class CommentModel:
    id = ""
    article_id = ""
    name = ""
    contact = ""
    comment = ""
    submit_date = ""

    @classmethod
    def initWith(self,res):
        model = CommentModel()
        model.id = res[0]
        model.article_id = res[1]
        model.name = res[2]
        model.contact = res[3]
        model.comment = res[4]
        model.submit_date = res[5]
        return model



