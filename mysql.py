import pymysql
from models import *

class DBManager():
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='Admin6688', db='futures_db', charset='UTF8')

    def db_ping(self):
        try:
            self.db.ping()()
        except:
            self.db.close()
            self.db = pymysql.connect(host='localhost', port=3306, user='root', passwd='Admin6688', db='futures_db', charset='UTF8')

    def article_count(self):
        
        self.db_ping()
        db_cursor = self.db.cursor()
        sql = "select count(0) from articles"

        try:
            res = db_cursor.execute(sql)
            for res in db_cursor.fetchall():
                return res[0]
            self.db.commit()
        except :
            self.db.rollback()
            raise
        finally:
            db_cursor.close()

    # 管理员获取文章列表
    def articles(self,page=1,count=50):

        self.db_ping()
        db_cursor = self.db.cursor()
        sql = "select * from articles order by is_top desc, id desc limit %d,%d" %((page-1)*count,count)

        try:
            db_cursor.execute(sql)
            models = []

            for res in db_cursor.fetchall():
                model = ArticleModel.initWith(res)
                models.append(model)

            self.db.commit()

            return  models

        except :
            self.db.rollback()
            raise
        finally:
            db_cursor.close()

    # 插入文章
    def insertArticle(self, model):

        self.db_ping()
        db_cursor = self.db.cursor()

        sql = "insert into articles (title, author, create_date, content, article_tags, sub_title, is_hot, thumbnail, is_index, classify, keywords, modify_date,is_top) \
               VALUES ('%s','%s','%s','%s','%s','%s', '%d', '%s', '%d',  '%s', '%s', '%s', '%s')" % \
              (model.title, model.author, model.createtime, model.content, model.article_tags, model.sub_title, model.is_hot, model.thumbnail, model.is_index, model.classify, model.keywords, model.modify_date, model.is_top)

        try:
            db_cursor.execute(sql)
            self.db.commit()
        except :
            self.db.rollback()
            raise
        finally:
            db_cursor.close()
    
    # 更新文章
    def updateArticle(self, model):

        self.db_ping()
        db_cursor = self.db.cursor()

        sql = "update articles set title='%s',author='%s',content='%s',article_tags='%s',sub_title='%s',is_hot='%s',thumbnail='%s',is_index='%s',classify='%s',keywords='%s',modify_date='%s',is_top='%s' \
        where id='%s'" %(model.title,model.author,model.content,model.article_tags,model.sub_title,model.is_hot,model.thumbnail,model.is_index,model.classify,model.keywords,model.modify_date,model.is_top,model.id)

        # sql = "replace into articles (title, author, modify_date, content, article_tags, sub_title, is_hot, thumbnail, id, is_index, classify, keywords) \
        #        VALUES ('%s','%s','%s','%s','%s','%s', '%d', '%s', '%s', '%d',  '%s', '%s')" % \
        #       (model.title, model.author, model.modify_date, model.content, model.article_tags, model.sub_title, model.is_hot, model.thumbnail,model.id, model.is_index, model.classify, model.keywords)
        try:
            db_cursor.execute(sql)
            self.db.commit()
        except :
            self.db.rollback()
            raise
        finally:
            db_cursor.close()

    # 删除文章
    def deleteArticleBy(self,id):

        self.db_ping()
        db_cursor = self.db.cursor()
        sql = "delete from articles where id = '%d'" % (id)

        try:
            db_cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()
            raise
        finally:
            db_cursor.close()

    # 获取文章
    def getArticleBy(self,id):

        self.db_ping()
        db_cursor = self.db.cursor()
        sql = "select * from articles where id = '%d'" % (id)

        try:
            db_cursor.execute(sql)
            res = db_cursor.fetchall()[0]
            article = ArticleModel.initWith(res)

            self.db.commit()

            return  article
        except:
            self.db.rollback()
            raise

        finally:
            db_cursor.close()

    # 获取热门推荐
    def hotArticle(self):

        self.db_ping()
        db_cursor = self.db.cursor()
        sql = "select * from articles where is_hot = 1 order by id desc limit 5 "

        try:
            res = db_cursor.execute(sql)
            models = []

            for res in db_cursor.fetchall():
                model = ArticleModel.initWith(res)
                models.append(model)

            self.db.commit()

            return  models

        except :
            self.db.rollback()
            raise
        finally:
            db_cursor.close()
    
    # 文章阅读量自增
    def articleViewCountInc(self,id):

        self.db_ping()
        db_cursor = self.db.cursor()
        sql = "update articles set vcount = vcount + 1 where id = %s" %(id)

        try:
            res = db_cursor.execute(sql)
            self.db.commit()
        except :
            self.db.rollback()
        finally:
            db_cursor.close()

    # 根据标签获取文章
    def articlesBytag(self,tag, page = 1 ,limit_count=5):

        self.db_ping()
        db_cursor = self.db.cursor()
        sql = "select * from articles where article_tags like '%"
        sql = sql + tag + "%' order by id desc limit " + str((page-1)*limit_count)+ "," + str(limit_count)

        try:
            res = db_cursor.execute(sql)
            models = []

            for res in db_cursor.fetchall():
                model = ArticleModel.initWith(res)
                models.append(model)

            self.db.commit()

            return  models

        except :
            self.db.rollback()
            raise
        finally:
            db_cursor.close()

    # 根据相关标签的文章数
    def articleCountBytag(self,tag):

        self.db_ping()
        db_cursor = self.db.cursor()
        sql = "select count(*) from articles where article_tags like '%"
        sql = sql + tag + "%'"

        try:
            res = db_cursor.execute(sql)

            for res in db_cursor.fetchall():
                return  res[0]

        except :
            self.db.rollback()
            raise
        finally:
            db_cursor.close()

    # 根据分类获取文章
    def articlesByClass(self,type, page = 1, limit_count=5):

        self.db_ping()
        db_cursor = self.db.cursor()
        sql = "select * from articles where classify = '%s' order by id desc limit %d,%d " % (type,(page-1)*limit_count,limit_count)
        
        try:
            res = db_cursor.execute(sql)
            models = []
            
            for res in db_cursor.fetchall():
                model = ArticleModel.initWith(res)
                models.append(model)

            self.db.commit()
                
            return  models

        except :
            self.db.rollback()
            raise
        finally:
            db_cursor.close()


    # 根据类型获取文章数量
    def articleCountByClass(self,type):

        self.db_ping()
        db_cursor = self.db.cursor()
        sql = "select count(*) from articles where classify = '%s'" % (type)
       
        try:
            res = db_cursor.execute(sql)
            
            for res in db_cursor.fetchall():                
                return  res[0]

        except :
            self.db.rollback()
            raise
        finally:
            db_cursor.close()

    # 分类下的热门的文章
    def relates_article(self,type):

        self.db_ping()
        db_cursor = self.db.cursor()
        sql = "select * from articles where classify = '%s' order by vcount desc limit 3" % (type)

        try:
            res = db_cursor.execute(sql)
            models = []
            
            for res in db_cursor.fetchall():
                model = ArticleModel.initWith(res)
                models.append(model)

            self.db.commit()
                
            return  models

        except :
            self.db.rollback()
            raise
        finally:
            db_cursor.close()


    # 首页列表：0，期货居间人：1，期货返佣：2
    def index_articles(self):

        self.db_ping()
        db_cursor = self.db.cursor()
        sql = "select * from articles where is_index = 1 order by id desc limit 6 "

        try:
            res = db_cursor.execute(sql)
            models = []
            
            for res in db_cursor.fetchall():
                model = ArticleModel.initWith(res)
                models.append(model)

            self.db.commit()
                
            return  models

        except :
            self.db.rollback()
            raise
        finally:
            db_cursor.close()

    # 插入评论数据
    def insert_comment(self, model):

        self.db_ping()
        db_cursor = self.db.cursor()

        sql = "insert into comments (article_id, name, contact, comment,submit_date) \
               VALUES ('%s','%s','%s','%s','%s')" % \
              (model.article_id, model.name, model.contact, model.comment,model.submit_date)

        try:
            db_cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()
            raise
        finally:
            db_cursor.close()

    # 获取评论数据
    def commentsBy(self,id):

        self.db_ping()
        db_cursor = self.db.cursor()
        sql = "select * from comments where article_id = '%s' order by submit_date desc" % (id)

        try:
            res = db_cursor.execute(sql)
            models = []
            
            for res in db_cursor.fetchall():
                model = CommentModel.initWith(res)
                models.append(model)

            self.db.commit()
                
            return  models

        except :
            self.db.rollback()
            raise
        finally:
            db_cursor.close()

    # 获取评论个数
    def commentsCountBy(self,id):

        self.db_ping()
        db_cursor = self.db.cursor()
        sql = "select count(*) from comments where article_id = '%s'" % (id)

        try:
            res = db_cursor.execute(sql)
            
            for res in db_cursor.fetchall():
                return res[0]

            self.db.commit()
                
        except :
            self.db.rollback()
            raise
        finally:
            db_cursor.close()

    # 获取链接
    def links(self):

        self.db_ping()
        db_cursor = self.db.cursor()
        sql = "select * from links"

        try:
            res = db_cursor.execute(sql)
            models = []
            
            for res in db_cursor.fetchall():
                model = LinkModel.initWith(res)
                models.append(model)

            self.db.commit()
                
            return  models

        except :
            self.db.rollback()
            raise
        finally:
            db_cursor.close()

    # 添加链接
    def addlink(self,link):

        self.db_ping()
        db_cursor = self.db.cursor()

        sql = "insert into links (name, url, create_date) \
            VALUES ('%s','%s','%s')" % \
            (link.name, link.url, link.create_date)
        try:
            db_cursor.execute(sql)
            self.db.commit()
        except :
            self.db.rollback()
            raise
        finally:
            db_cursor.close()

    # 删除链接
    def deletelink(self,id):

        self.db_ping()
        db_cursor = self.db.cursor()

        sql = "delete from links where id = %s" % (id)
        try:
            db_cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()
            raise
        finally:
            db_cursor.close()

    # 获取轮播图数据
    def focus_list(self):

        self.db_ping()
        db_cursor = self.db.cursor()

        sql = "select * from focus"
        try:
            res = db_cursor.execute(sql)
            models = []
            
            for res in db_cursor.fetchall():
                model = FocusModel.initWith(res)
                models.append(model)

            self.db.commit()
                
            return  models

        except :
            self.db.rollback()
            raise
        finally:
            db_cursor.close()

    # 添加轮播图数据
    def add_focus(self,focus):

        self.db_ping()
        db_cursor = self.db.cursor()

        sql = "insert into focus (title, image, url, create_date) \
            VALUES ('%s','%s','%s', '%s')" % \
            (focus.title, focus.image, focus.url, focus.create_date)
        try:
            db_cursor.execute(sql)
            self.db.commit()
        except :
            self.db.rollback()
            raise
        finally:
            db_cursor.close()

    # 删除轮播数据
    def delete_focus(self,id):

        self.db_ping()
        db_cursor = self.db.cursor()

        sql = "delete from focus where id = %s" % (id)
        try:
            db_cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()
            raise
        finally:
            db_cursor.close()

    # 获取导航数据
    def navi_models(self,rec_child_items = True):

        self.db_ping()
        db_cursor = self.db.cursor()
        sql = "select * from navi_items where sup_id = 0"

        try:
            res = db_cursor.execute(sql)
            models = []
            
            for res in db_cursor.fetchall():
                model = NaviItemModel.initWith(res)
                if rec_child_items :
                    model.childItems = self.navi_models_by_supid(model.id)
                models.append(model)

            self.db.commit()
                
            return  models

        except :
            self.db.rollback()
            raise
        finally:
            db_cursor.close()

    # 子导航菜单
    def child_navi_models(self):

        self.db_ping()
        db_cursor = self.db.cursor()
        sql = "select * from navi_items where sup_id != 0 order by id desc"

        try:
            row = db_cursor.execute(sql)
            models = []
            for res in db_cursor.fetchall():
                model = NaviItemModel.initWith(res)
                models.append(model)

            self.db.commit()
                
            return  models

        except :
            self.db.rollback()
            raise
        finally:
            db_cursor.close()

    # 获取子导航
    def navi_models_by_supid(self,sup_id):

        self.db_ping()
        db_cursor = self.db.cursor()
        sql = "select * from navi_items where sup_id = %s order by id desc" %(sup_id)

        try:
            row = db_cursor.execute(sql)
            models = []
            for res in db_cursor.fetchall():
                model = NaviItemModel.initWith(res)
                models.append(model)

            self.db.commit()
                
            return  models

        except :
            self.db.rollback()
            raise
        finally:
            db_cursor.close()

    # 插入导航模块
    def add_navi_item(self,item):

        self.db_ping()
        db_cursor = self.db.cursor()
        sql = "insert into navi_items (name, link, sup_id, create_date) \
            VALUES ('%s','%s','%s', '%s')" % \
            (item.name, item.url, 0, item.create_date)
        try:
            db_cursor.execute(sql)
            self.db.commit()
        except Exception as error:
            self.db.rollback()
            raise
        finally:
            db_cursor.close()

    # 删除导航数据
    def delete_navi_item(self,id):

        self.db_ping()
        db_cursor = self.db.cursor()
        sql = "delete from navi_items where id = %s" % (id)

        try:
            db_cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()
            raise
        finally:
            db_cursor.close()
    

db_manager = DBManager()
