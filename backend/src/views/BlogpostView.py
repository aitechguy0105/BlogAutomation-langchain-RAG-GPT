# /src/views/BlogpostView.py
from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.BlogpostModel import BlogpostModel, BlogpostSchema
from bs4 import BeautifulSoup
blogpost_api = Blueprint('blogpost_api', __name__)
blogpost_schema = BlogpostSchema()

def save_daily_article(data):
    data = blogpost_schema.load(data)
    post = BlogpostModel(data)
    post.save()

@blogpost_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
    """
    Create Blogpost Function
    """
    req_data = request.get_json()
    req_data['owner_id'] = g.user.get('id')
    data = blogpost_schema.load(req_data)
    if 'error' in data:
        return custom_response(data.error, 400)
    post = BlogpostModel(data)
    post.save()
    data = blogpost_schema.dump(post)
    return custom_response(data, 201)


@blogpost_api.route('/', methods=['GET'])
def get_all():
    """
    Get All Blogposts
    """
    posts = BlogpostModel.get_all_blogposts()
    data = blogpost_schema.dump(posts, many=True)

    return custom_response(data, 200)

@blogpost_api.route('/all_blogposts_count', methods=['GET'])
def get_all_blogposts_count():
    """
    Get All Blogposts
    """
    count = BlogpostModel.get_all_blogposts_count()
    data = {"count": count}
    return custom_response(data, 200)
@blogpost_api.route('/popular_article_related_articles', methods=['GET'])
def get_most_popular_article_related_articles():
    """
    Get most popular Blogpost
    """
    post = BlogpostModel.get_most_popular_article()
    data = blogpost_schema.dump(post)
    # print('blogpostview ', data)
    posts_related = BlogpostModel.get_popular_articles_with_category(data['category_id'])
    
    posts_related = posts_related[1:]
    data_list = blogpost_schema.dump(posts_related, many=True)
    data_list.insert(0, data)
    for data in data_list:
        article = data.pop("contents")
        # article = data["contents"]
        soup = BeautifulSoup(article, 'html.parser')
        
        summary = ""
        paragraphs = soup.find_all('p')
        if len(paragraphs) > 1:
            summary = paragraphs[0].get_text()

        # Insert the "summary" item
        data["summary"] = summary
        img_url = soup.find('img')['src']
        data['img_url'] = img_url

    return custom_response(data_list, 200)

@blogpost_api.route('/related_articles/<string:category_id>', methods=['GET'])
def get_popular_articles_with_category(category_id):
    """
    Get most popular Blogpost with a specific category
    """
    # category = request.args.get('category')  # Assuming the category is passed as a query parameter
    
    posts = BlogpostModel.get_popular_articles_with_category(category_id)
    data_list = blogpost_schema.dump(posts, many=True)
    data_list = data_list[1:]
    for data in data_list:
        article = data.pop("contents")
        # article = data["contents"]
        soup = BeautifulSoup(article, 'html.parser')

        summary = ""
        paragraphs = soup.find_all('p')
        if len(paragraphs) > 1:
            summary = paragraphs[0].get_text()

        # Insert the "summary" item
        data["summary"] = summary
        img_url = soup.find('img')['src']
        data['img_url'] = img_url

    return custom_response(data_list, 200)
@blogpost_api.route('/popular_articles_month', methods=['GET'])
def get_popular_articles_month():
    """
    Get most popular Blogposts month
    """
    posts = BlogpostModel.get_popular_articles_month()
    data_list = blogpost_schema.dump(posts, many=True)
    for data in data_list:
        article = data.pop("contents")
        # article = data["contents"]
        soup = BeautifulSoup(article, 'html.parser')

        summary = ""
        paragraphs = soup.find_all('p')
        if len(paragraphs) > 1:
            summary = paragraphs[0].get_text()

        # Insert the "summary" item
        data["summary"] = summary
        img_url = soup.find('img')['src']
        data['img_url'] = img_url

    return custom_response(data_list, 200)
@blogpost_api.route('/articles_by_category/<string:category_id>/<int:page_num>/<int:articles_per_page>', methods=['GET'])
def get_articles_by_category(category_id, page_num, articles_per_page):
    """
    Get articles by category
    """
    # category = request.args.get('category')
    # page_num = request.args.get('page_num')
    # articles_per_page = request.args.get('articles_per_page')
    posts = BlogpostModel.get_articles_by_category(category_id, page_num, articles_per_page)

    data_list = blogpost_schema.dump(posts, many=True)
    for data in data_list:
        article = data.pop("contents")
        # article = data["contents"]
        soup = BeautifulSoup(article, 'html.parser')

        summary = ""
        paragraphs = soup.find_all('p')
        if len(paragraphs) > 1:
            summary = paragraphs[0].get_text()

        # Insert the "summary" item
        data["summary"] = summary
        img_url = soup.find('img')['src']
        data['img_url'] = img_url
    return custom_response(data_list, 200)

@blogpost_api.route('/articles_by_new/<int:page_num>/<int:articles_per_page>/<string:search_keywords>', methods=['GET'])
def get_articles_by_new_search(page_num, articles_per_page, search_keywords):
    """
    Get articles by created data
    """
    # new = request.args.get('new')
    # page_num = request.args.get('page_num')
    # articles_per_page = request.args.get('articles_per_page')
    posts = BlogpostModel.get_articles_by_new_search(page_num, articles_per_page, search_keywords)
    data_list = blogpost_schema.dump(posts, many=True)
    for data in data_list:
        article = data.pop("contents")
        # article = data["contents"]
        soup = BeautifulSoup(article, 'html.parser')

        summary = ""
        paragraphs = soup.find_all('p')
        if len(paragraphs) > 1:
            summary = paragraphs[0].get_text()

        # Insert the "summary" item
        data["summary"] = summary
        img_url = soup.find('img')['src']
        data['img_url'] = img_url
        
    return custom_response(data_list, 200)


def get_one_article_by_new():
    
    post = BlogpostModel.get_one_article_by_new()
    data = blogpost_schema.dump(post)
    return data

@blogpost_api.route('/articles_by_new/<int:page_num>/<int:articles_per_page>', methods=['GET'])
def get_articles_by_new(page_num, articles_per_page):
    """
    Get articles by created data
    """
    # new = request.args.get('new')
    # page_num = request.args.get('page_num')
    # articles_per_page = request.args.get('articles_per_page')
    posts = BlogpostModel.get_articles_by_new(page_num, articles_per_page)
    data_list = blogpost_schema.dump(posts, many=True)
    for data in data_list:
        article = data.pop("contents")
        # article = data["contents"]
        soup = BeautifulSoup(article, 'html.parser')

        summary = ""
        paragraphs = soup.find_all('p')
        if len(paragraphs) > 1:
            summary = paragraphs[0].get_text()

        # Insert the "summary" item
        data["summary"] = summary
        # print('test')
        # print(str(soup))
        # img_url = ''
        # test = soup.find('img')
        # if test is None:
        #     print('None')
        # else :
            
        img_url = soup.find('img')['src']
        data['img_url'] = img_url
    return custom_response(data_list, 200)


@blogpost_api.route('/articles_by_popular/<int:page_num>/<int:articles_per_page>/<string:search_keywords>', methods=['GET'])
def get_articles_by_popular_search(page_num, articles_per_page, search_keywords):
    """
    Get articles by created data
    """
    # new = request.args.get('new')
    # page_num = request.args.get('page_num')
    # articles_per_page = request.args.get('articles_per_page')
    posts = BlogpostModel.get_articles_by_popular_search(page_num, articles_per_page, search_keywords)
    data_list = blogpost_schema.dump(posts, many=True)
    for data in data_list:
        article = data.pop("contents")
        # article = data["contents"]
        soup = BeautifulSoup(article, 'html.parser')

        summary = ""
        paragraphs = soup.find_all('p')
        if len(paragraphs) > 1:
            summary = paragraphs[0].get_text()

        # Insert the "summary" item
        data["summary"] = summary
        img_url = soup.find('img')['src']
        data['img_url'] = img_url
    return custom_response(data_list, 200)

@blogpost_api.route('/articles_by_popular/<int:page_num>/<int:articles_per_page>', methods=['GET'])
def get_articles_by_popular(page_num, articles_per_page):
    """
    Get articles by created data
    """
    # new = request.args.get('new')
    # page_num = request.args.get('page_num')
    # articles_per_page = request.args.get('articles_per_page')
    posts = BlogpostModel.get_articles_by_popular(page_num, articles_per_page)
    data_list = blogpost_schema.dump(posts, many=True)
    for data in data_list:
        article = data.pop("contents")
        # article = data["contents"]
        soup = BeautifulSoup(article, 'html.parser')

        summary = ""
        paragraphs = soup.find_all('p')
        if len(paragraphs) > 1:
            summary = paragraphs[0].get_text()

        # Insert the "summary" item
        data["summary"] = summary
        img_url = soup.find('img')['src']
        data['img_url'] = img_url
    return custom_response(data_list, 200)

@blogpost_api.route('/search/<string:search_keywords>', methods=['GET'])
def get_search_result(search_keywords):
    """
    Get Search result
    """
    posts = BlogpostModel.get_search_result(search_keywords)
    data_list = blogpost_schema.dump(posts, many=True)
    for data in data_list:
        article = data.pop("contents")
        # article = data["contents"]
        soup = BeautifulSoup(article, 'html.parser')

        summary = ""
        paragraphs = soup.find_all('p')
        if len(paragraphs) > 1:
            summary = paragraphs[0].get_text()

        # Insert the "summary" item
        data["summary"] = summary
        img_url = soup.find('img')['src']
        data['img_url'] = img_url
    return custom_response(data_list, 200)

@blogpost_api.route('/<int:blogpost_id>', methods=['GET'])
def get_one(blogpost_id):
    """
    Get A Blogpost
    """
    post = BlogpostModel.get_one_blogpost(blogpost_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = blogpost_schema.dump(post)
    data['rating'] = data['rating'] + 1

    post.update(data)
    return custom_response(data, 200)


@blogpost_api.route('/<int:blogpost_id>', methods=['PUT'])
@Auth.auth_required
def update(blogpost_id):
    """
    Update A Blogpost
    """
    req_data = request.get_json()
    post = BlogpostModel.get_one_blogpost(blogpost_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = blogpost_schema.dump(post)
    if data.get('owner_id') != g.user.get('id'):
        return custom_response({'error': 'permission denied'}, 400)

    data = blogpost_schema.load(req_data, partial=True)
    if 'error' in data:
        return custom_response(data.error, 400)
    post.update(data)

    data = blogpost_schema.dump(post)
    return custom_response(data, 200)


@blogpost_api.route('/<int:blogpost_id>', methods=['DELETE'])
@Auth.auth_required
def delete(blogpost_id):
    """
    Delete A Blogpost
    """
    post = BlogpostModel.get_one_blogpost(blogpost_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = blogpost_schema.dump(post)
    if data.get('owner_id') != g.user.get('id'):
        return custom_response({'error': 'permission denied'}, 400)

    post.delete()
    return custom_response({'message': 'deleted'}, 204)


def custom_response(res, status_code):
    """
    Custom Response Function
    """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )

