from xbmcswift2 import Plugin
from yogaglo.YogaGloApi import YogaGloApi

yg_apis = {'queues': 'https://www.yogaglo.com/api/v3/queues',
           'followupteachers': 'https://www.yogaglo.com/api/v3/followupteachers',
           'videos': 'https://www.yogaglo.com/api/v3/videos',
           'histories': 'https://www.yogaglo.com/api/v3/histories'}

plugin = Plugin()


@plugin.route('/')
def index():
    items = [
        {'label': 'My Practice',
         'path': plugin.url_for('show_mypractice', url=yg_apis['queues'])},
        {'label': 'Following',
         'path': plugin.url_for('following', url=yg_apis['followupteachers'])},
        {'label': 'Watched',
         'path': plugin.url_for('show_history', url=yg_apis['histories'])},
    ]

    return items


@plugin.route('/classes/mypractice/<url>')
def show_mypractice(url):
    api = YogaGloApi(plugin)
    return api.myqueue(url)


@plugin.route('/classes/following/<url>')
def show_myfollowing(url):
    api = YogaGloApi(plugin)
    return api.following_videos(url)


@plugin.route('/classes/watched/<url>')
def show_history(url):
    api = YogaGloApi(plugin)
    return api.myhistory(url)


@plugin.route('/classes/teacher/<url>/<id>')
def show_teacher(url, id):
    api = YogaGloApi(plugin)
    return api.teacher_videos(url, id)


@plugin.route('/following/<url>')
def following(url):
    items = [{
        'label': 'Videos',
        'path': plugin.url_for('show_myfollowing',
                               url=yg_apis['followupteachers'])}]

    api = YogaGloApi(plugin)
    following = api.teachers_followed(url)
    # adjust the path that is storing teacher id
    for item in following:
        item['path'] = plugin.url_for('show_teacher', url=yg_apis['videos'],
                                      id=item['path'])

    items.extend(following)
    return items

if __name__ == '__main__':
    plugin.run()
