# maoyan_movie

## 项目说明
此项目采用Python语言+flask框架+adminLTE模板+Bootstrap3开发的，旨在爬取猫眼电影中的TOP100电影排行榜、2019年动作电影、2019年喜剧电影的导演、演员、导演和演员图片、评论等信息，
每部电影都可以点进去查看其详情，也可以评论，但只有登录用户才可以评论。

电影信息不是实时爬取的，而是在后台通过cron定时爬取信息存储到DB中，然后前端页面打开时去DB中抓取展示的。

这是本人第一次使用GitHub上传项目，做的不好请多多包涵。。。
