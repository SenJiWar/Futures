/*-------------------
*Description:        By www.yiwuku.com
*Website:            https://app.zblogcn.com/?id=711
*Author:             尔今 erx@qq.com
*update:             2015-4-20(Last:2017-02-16)
-------------------*/
$(function() {
    //Header
    var xts = document.location;
    var stt = $(".asl-title h3").text();
    $(".nav a").each(function() {
        if (this.href == xts.toString().split("#")[0]) {
            $(this).parent().addClass("cu");
            return false;
        }
        if ($(this).text() == stt) {
            $(this).parent().addClass("cu");
            return false;
        }
    });
    $(".nav>li").each(function() {
        $(this).find("a:eq(0)").addClass("link");
        var naurl = $(this).find("a:eq(0)").attr("href");
        var natxt = $(this).find("a:eq(0)").text();
        $(this).append('<a class="bg" href="' + naurl + '">' + natxt + '</a>');
    });
    $(".nav>li:has(ul)").hover(
        function() {
            $(this).find('ul').slideDown(200);
        },
        function() {
            $(this).find('ul').slideUp(200);
        });
    $(".search input").bind({
        focus: function() {
            $(this).parents(".search").addClass("fcs");
        },
        blur: function() {
            $(this).parents(".search").removeClass("fcs");
        }
    });
    var mbpwidth = $(window).width();
    var mnSub = 0;
    if (mbpwidth <= 600) {
        $(".nav").click(function() {
            $(this).find("li").toggle();
        });
        $(".lph-left").click(function() {
            $(".nav li").hide();
        });
        $(".nav>li:has(ul) a").click(function() {
            if (mnSub == 0) {
                mnSub = 1;
                return false;
            } else {
                mnSub = 0;
                $(this).unbind("click");
            }
        });
    }
    $(window).resize(function() {
        mbpwidth = $(window).width();
        if (mbpwidth > 600) {
            $(".nav li").show();
        }
    });
    //Left
    $(".lph-pageList .info .tags").each(function() {
        var listag = $(this).find("a").length;
        if (listag < 1) {
            $(this).find("i").hide();
            $(this).find("em").show();
        }
    });

    //Logdes-Mobi
    function mobides() {
        if ($(window).width() <= 600) {
            $(".lph-pageList .wrap li.pbox .word .des").each(function() {
                $(this).css("minHeight", "100px");
                var maxwidth = 56;
                var alltext = $(this).text();
                if ($(this).text().length > maxwidth) {
                    $(this).text($(this).text().substring(0, maxwidth));
                    $(this).html($(this).html() + '......');
                }
            });
        }
    };
    mobides();
    $(window).resize(mobides);
    //Lazy-img
    $("img.lazy").lazyload({
        effect: "fadeIn"
    });
    //Right
    $(".lph-right .kuaixun .kx-ul li").mouseenter(function(e) {
        $(".lph-right .kuaixun .kx-ul li").removeClass("hov");
        $(this).addClass("hov");
    })
    $(".pbz-bd .bdd:eq(1)").hide();
    var rightPzIleft = [0, '50%'],
        pbzttab = $("#pbzttab"),
        pbzttabHd = pbzttab.find(".pbz-hd a"),
        pbzttabBd = pbzttab.find(".pbz-bd .bdd"),
        pbzttabCoin = pbzttab.find(".pbz-hd i");
    pbzttabHd.mouseenter(function() {
        var idx = $(this).index();
        pbzttabHd.removeClass("cur");
        pbzttabHd.eq(idx).addClass("cur");
        pbzttabBd.css({ "display": "none" });
        pbzttabBd.eq(idx).css({ "display": "block" });
        pbzttabCoin.animate({ "left": rightPzIleft[idx] }, 300);
    })
    window.onload = function() {
        if ($(".lph-right .weixinewm").length < 1) return;
        var wexinewm_y = $(".lph-right .weixinewm").offset().top - 100;
        var lph_l = $(".lph-left").height();
        var lph_r = $(".lph-right").height();
        $(window).scroll(function() {
            if (lph_l > lph_r) {
                if ($(window).scrollTop() > wexinewm_y) {
                    $(".lph-right .weixinewm").addClass("weixinewm-fixed");
                } else {
                    $(".lph-right .weixinewm").removeClass("weixinewm-fixed");
                }
            }
        });
    }
    $(".lph-right .hotauthor .btns a.weixin").hover(function() {
            var thiss = $(this);
            thiss.find(".aut-ewm").show(10, function() {
                $(this).addClass("show");
            })
        }, function() {
            var this2 = $(this);
            $(this).find(".aut-ewm").removeClass("show");
            setTimeout(function() {
                this2.find(".aut-ewm").hide(10);
            }, 300)
        })
        //Footer
    $(window).scroll(function() {
        if ($(window).scrollTop() > 300) {
            $(".gotoBar .top").slideDown(400);
        } else {
            $(".gotoBar .top").slideUp(400);
        }
    });
    $(".gotoBar .top").click(function() {
        $("html, body").animate({ scrollTop: 0 }, {
            duration: 300,
            easing: 'linear'
        });
    })
});