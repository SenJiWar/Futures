# coding: utf8
import tornado.web
import tornado.ioloop
import os,sys
from tornado.web import RequestHandler, StaticFileHandler
from tornado.options import options, define
from mysql import *
from utils import *
import json
import types
from notification import *

# 前端首页
class IndexHandler(RequestHandler):
    def get(self):
        index_array = []
        try:
            info = PageInfoModel("期货开户_股指期货开户_期货手续费返还_期货居间人_期货返佣网")
            info.navi_title = "期货开户享受交易所手续费返还"
            info.keywords = "期货开户_期货手续费_股指期货开户_期货居间人_期货返佣_期货手续费返还_期货居间合作"
            info.content = "通过期货返佣网可以办理期货开户和期货居间人合作事宜。期货开户、股指期货开户享受同行最低期货手续费加1分；资金量和交易量大可以申请期货返佣，期货手续费返还；期货居间合作，期货居间人享受最高期货居间返佣比例。"

            page = int(self.get_argument('page', strip=True, default=1))

            index_array = db_manager.index_articles()
            focuses = db_manager.focus_list()

            self.render("./html/index.html",index_array=index_array,info=info,focuses=focuses,page=page)

        except Exception as error:
            pass


# 管理员登录界面
class AdminLoginHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render("./admin/login.html")
    def post(self, *args, **kwargs):
        self.get()

# 管理员首页
class AdminIndexHandler(RequestHandler):
    def post(self, *args, **kwargs):
        account = self.get_argument('account', strip=True)
        password = self.get_argument('password',strip=True)
        if account == "admin" and password == "admin":
            self.set_cookie("username","admin",expires_days=0.5)
            self.render("./admin/index.html", items = db_manager.articles())
        else:
            arg = {
                'title': '登录错误',
                'error': "对不起,您输入的账号或密码错误~"
            }
            self.render("./admin/admin_error.html", **arg)

    def get(self, *args, **kwargs):
        user = self.get_cookie("username")
        if user == 'admin':
            self.render("./admin/index.html", items = db_manager.articles())
        else:
            arg = {
                'title': '验证错误',
                'error': "对不起,无法验证您的登录信息~"
            }
            self.render("./admin/admin_error.html", **arg)

# 管理员编辑
class AdminEditHandler(RequestHandler):
    def get(self, *args, **kwargs):
        article = ArticleModel()
        models = db_manager.navi_models(rec_child_items = False)
        self.render("./admin/edit.html", article = article, classes = models)

# 外部链接
class AdminLinksHanlder(RequestHandler):
    def get(self, *args, **kwargs):
        links = db_manager.links()
        self.render("./admin/links.html",links=links)

# 焦点图设置
class AdminFocusHanlder(RequestHandler):
    def get(self, *args, **kwargs):
        focuses = db_manager.focus_list()
        self.render("./admin/focus.html",focuses=focuses)
 
# 管理员上传文章
class AdminUploadArticleHandler(RequestHandler):

    @tornado.web.asynchronous
    def post(self, *args, **kwargs):

        article = ArticleModel()
        article.id = self.get_argument('id', strip=True, default="")
        article.title = self.get_argument('title', strip=True)
        article.author = self.get_argument('author', strip=True)
        article.content = self.get_argument('content', strip=True)
        article.article_tags = self.get_argument('article_tags', strip=True)
        article.sub_title = self.get_argument('sub_title', strip=True)
        article.is_hot = int(self.get_argument('is_hot', strip=True))
        article.is_index = int(self.get_argument('is_index', strip=True))
        article.classify = self.get_argument('classify', strip=True)
        article.keywords = self.get_argument('keywords', strip=True, default="")
        article.is_top = int(self.get_argument('is_top', strip=True))

        base64str = self.get_argument('thumbnail', strip=True, default="")
        article.thumbnail = save_image(base64str)
        
        # 获取当前的日期
        article.modify_date = date_time()

        try:
            if len(article.id) > 0 :
                db_manager.updateArticle(article)
            else :
                article.createtime = date_time()
                db_manager.insertArticle(article)
            self.write("保存成功")
            self.finish()
        except Exception as err:
            self.write("保存失败")
            self.finish()
        

# 添加外部链接
class AdminAddLinkHandler(RequestHandler):

    def post(self, *args, **kwargs):
        link = LinkModel()
        link.name = self.get_argument('name', strip=True, default="")
        link.url = self.get_argument('url', strip=True, default="")
        link.create_date = date_time()
        db_manager.addlink(link)
        self.redirect("/a_links.html")

# 删除链接
class AdminDeleteLinkHandler(RequestHandler):

    def get(self, *args, **kwargs):
        id = self.get_argument('id', strip=True, default="")
        db_manager.deletelink(id)
        self.redirect("/a_links.html")


# 删除文章
class DeleteArticleHandler(RequestHandler):

    def get(self, *args, **kwargs):
        id = int(self.get_argument('id', strip=True))
        try:
            db_manager.deleteArticleBy(id)
            self.redirect("/a_index.html")
        except:
            pass

# 预览文章
class PreviewArticleHandler(RequestHandler):

    def get(self, *args, **kwargs):
        id = int(self.get_argument('id', strip=True))
        try:
            article = db_manager.getArticleBy(id)
            info = PageInfoModel(article.title + "_期货返佣网")
            info.navi_title = article.title
            info.content = article.sub_title
            info.keywords = article.keywords
            relates = db_manager.relates_article(article.classify)
            comment_count = db_manager.commentsCountBy(id)
            self.render("./html/article.html", article=article,info=info, relates=relates,article_id=id,comment_count=comment_count)
        except:
            pass
        # 增加阅读数
        db_manager.articleViewCountInc(id)

# 编辑文章
class EidtArticleHandler(RequestHandler):
    
    def get(self, *args, **kwargs):
        id = int(self.get_argument('id', strip=True))
        try:
            article = db_manager.getArticleBy(id)
            models = db_manager.navi_models(rec_child_items = False)
            self.render("./admin/edit.html", article = article, classes = models)      
        except:
            pass

# 上传轮播图
class AdminUploadFocusHandler(RequestHandler):

    def post(self, *args, **kwargs):
        focus = FocusModel()
        focus.title = self.get_argument('title', strip=True)
        focus.url = self.get_argument('url', strip=True)
        focus.create_date = date_time()

        base64image = self.get_argument('thumbnail', strip=True)
        focus.image = save_image(base64image)

        try:
            db_manager.add_focus(focus)
            self.write("保存成功")
        except:
            self.write("保存失败")
            pass

# 删除轮播图
class AdminDeleteFocusHandler(RequestHandler):

    def get(self, *args, **kwargs):
        id = int(self.get_argument('id', strip=True))
        db_manager.delete_focus(id)
        self.redirect("a_focus.html")

# 标签列表
class TagHandler(RequestHandler):

    def get(self, *args, **kwargs):
        tag = self.get_argument('keyword', strip=True, default="")
        info = PageInfoModel(tag)
        info.title = tag + "_期货开户享受交易所手续费返还_期货返佣网"
        info.navi_title = tag
        info.content = tag
        info.keywords = tag

        # 分页设置
        page = int(self.get_argument('page', strip=True, default=1))

        page_count = 15
        articles = db_manager.articlesBytag(tag,page=page,limit_count=page_count)
        count = db_manager.articleCountBytag(tag)
        tol_page = (count-1)//page_count + 1

        baseUrl = "/tags?keyword=" + tag

        self.render("./html/tags.html",info=info, keyword=tag, articles = articles, cur_page=page, tol_page=tol_page, baseUrl=baseUrl)

class ClassesHandler(RequestHandler):

    def get(self, *args, **kwargs):
        tag = self.get_argument('keyword', strip=True, default="")
        info = PageInfoModel(tag)
        info.title = tag + "_期货开户享受交易所手续费返还_期货返佣网"
        info.navi_title = tag
        info.content = tag
        info.keywords = tag

        page = int(self.get_argument('page', strip=True, default=1))

        page_count = 15
        articles = db_manager.articlesByClass(tag,page=page,limit_count=page_count)
        count = db_manager.articleCountByClass(tag)
        tol_page = (count-1)//page_count + 1

        baseUrl = "/classes?keyword=" + tag

        self.render("./html/tags.html",info=info, keyword=tag, articles = articles, cur_page=page, tol_page=tol_page, baseUrl=baseUrl)

# 导航菜单的显示
class EditNaviHandler(RequestHandler):

    def get(self, *args, **kwargs):
        list = db_manager.child_navi_models()
        models = db_manager.navi_models(rec_child_items = False)
        self.render("./admin/navi.html",list=list,classes = models)

class AddNavigationHandler(RequestHandler):

    def post(self, *args, **kwargs):

        item = NaviItemModel()

        item.name = self.get_argument('name', strip=True, default="")
        item.url = self.get_argument('url', strip=True, default="")
        classify = self.get_argument('classify', strip=True, default="")

        if classify == "期货开户":
            item.sup_id = "1"
        elif classify == "手续费返还":
            item.sup_id = "2"
        elif classify == "原油期货开户":
            item.sup_id = "3"
        elif classify == "股指期货开户":
            item.sup_id = "4"
        elif classify == "期货资讯":
            item.sup_id = "5"
        item.create_date = date_time()

        try:
            db_manager.add_navi_item(item)
            self.write("保存成功")
        except:
            self.write("保存失败")
            pass

# 删除导航模块
class DeleteNaviItemHandler(RequestHandler):
    def get(self, *args, **kwargs):
        id = self.get_argument('id', strip=True, default="")
        db_manager.delete_navi_item(id)
        self.redirect("/a_navi.html")

# 发表评论
class PostCommentHandler(RequestHandler):
    def post(self, *args, **kwargs):
        
        model = CommentModel()
        id = self.get_argument('article_id', strip=True, default="")
        model.article_id = id
        model.name = self.get_argument('inp_name', strip=True, default="")
        model.contact = self.get_argument('inp_contact', strip=True, default="")
        model.comment = self.get_argument('inp_comment', strip=True, default="")
        model.submit_date = date_time()

        ## 发送钉钉通知
        notification(model)
        ## 添加评论
        db_manager.insert_comment(model)

        self.redirect("article?id="+id)
        
# 编辑器上传文件
class KDUploadJsonHandler(RequestHandler):
    
    def post(self, *args, **kwargs):

        # 响应数据
        response = {}

        # 文件类型 image、flash、media、file
        file_type = self.get_argument('dir', strip=True, default="")
        # 上传的文件
        file_metas = self.request.files["imgFile"]

        if len(file_metas) == 0 :
            response['error'] = 1
            response['message'] = "文件不能为空~"
            self.write(json.dumps(response))
            return

        # 存储文件
        for meta in file_metas:  
            filename = meta['filename']  
            ctype = meta['content_type'].split("/")[1]

            new_filename = md5string(filename) + "." + ctype
            file_path = "./html/resources/store_imgs/" + new_filename

            with open(file_path,'wb') as up: 
                up.write(meta['body'])  

            response['url'] = file_path.replace("./html","")
            
        response['error'] = 0

        self.write(json.dumps(response))


class KDFileManagerJsonHandler(RequestHandler):
    
    def post(self, *args, **kwargs):
        pass

# UI模块
class NaviBarModule(tornado.web.UIModule):
    def render(self):
        navi_items = db_manager.navi_models()
        return self.render_string("./html/navi.html",navi_items=navi_items)

class ContentRightModule(tornado.web.UIModule):
    def render(self):
        return self.render_string("./html/content_right.html")

class HotRecomendModule(tornado.web.UIModule):
    def render(self):
        articles = db_manager.hotArticle()
        return self.render_string("./html/hot_recoment.html",articles = articles)

class NewArticlesModule(tornado.web.UIModule):
    def render(self,page):
        page_count = 15
        articles = db_manager.articles(page=page,count=page_count)
        count = db_manager.article_count()
        tol_page = (count-1)//page_count + 1
        return self.render_string("./html/index_ latest.html", articles=articles,count=count,cur_page=page,tol_page=tol_page)

class ContentRightTagModule(tornado.web.UIModule):
    def render(self, tag):
        articles = db_manager.articlesByClass(tag)
        return self.render_string("./html/content_right_tag.html", tag=tag, articles=articles)

class LinksModule(tornado.web.UIModule):
    def render(self):
        links = db_manager.links()
        return self.render_string("./html/links.html", links=links)

class CommentsModule(tornado.web.UIModule):
    def render(self,article_id):
        list = db_manager.commentsBy(article_id)
        return self.render_string("./html/comments.html",comments=list)

# 测试用例
class TestHandler(RequestHandler):
    def get(self, *args, **kwargs):
        mm = save_image("aabba")        
        pass


define("port", default=8010, type=int, help="run server on the given port")

current_path = os.path.dirname(__file__)

application = tornado.web.Application(
    [
        (r'/', IndexHandler),
        (r'/test', TestHandler),
        (r'/adminlogin.html', AdminLoginHandler),
        (r'/a_index.html', AdminIndexHandler),
        (r'/a_edit.html', AdminEditHandler),
        (r'/a_links.html', AdminLinksHanlder),
        (r'/a_focus.html', AdminFocusHanlder),
        (r'/a_navi.html', EditNaviHandler),
        (r'/upload_article', AdminUploadArticleHandler),
        (r'/upload_focus', AdminUploadFocusHandler),
        (r'/delete_focus', AdminDeleteFocusHandler),
        (r'/add_link', AdminAddLinkHandler),
        (r'/delete_link', AdminDeleteLinkHandler),
        (r'/delete_article', DeleteArticleHandler),
        (r'/article', PreviewArticleHandler),
        (r'/edit_article', EidtArticleHandler),
        (r'/tags', TagHandler),
        (r'/classes', ClassesHandler),
        (r'/kd_upload_json', KDUploadJsonHandler),
        (r'/kd_file_manager_json', KDFileManagerJsonHandler),
        (r'/add_navi', AddNavigationHandler),
        (r'/delete_navi_item', DeleteNaviItemHandler),
        (r'/post_comment', PostCommentHandler),
        # 前端配置静态路径
        (r'^/resources/images/(.*)$', StaticFileHandler, {"path": os.path.join(current_path, "html/resources/images")}),
        (r'^/resources/store_imgs/(.*)$', StaticFileHandler, {"path": os.path.join(current_path, "html/resources/store_imgs")}),
        (r'^/resources/style/images/(.*)$', StaticFileHandler, {"path": os.path.join(current_path, "html/resources/images")}),
        (r'^/resources/script/(.*)$', StaticFileHandler, {"path": os.path.join(current_path, "html/resources/script")}),
        (r'^/resources/style/(.*)$', StaticFileHandler, {"path": os.path.join(current_path, "html/resources/style")}),
        # 后台配置静态路径
        (r'^/assets/(.*)$', StaticFileHandler, {"path": os.path.join(current_path, "admin/assets")}),
        (r'^/loginassets/(.*)$', StaticFileHandler, {"path": os.path.join(current_path, "admin/loginassets")}),
    ],
    ui_modules={
        "ContentRight": ContentRightModule,
        "HotRecomend": HotRecomendModule,
        "NewArticles": NewArticlesModule,
        "ContentRightTag": ContentRightTagModule,
        "Links": LinksModule,
        "NaviBar": NaviBarModule,
        "Comments": CommentsModule,
    },
    static_path=os.path.join(os.path.dirname(__file__), "statics"),
)

if __name__ == "__main__":

    tornado.options.parse_command_line()

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
