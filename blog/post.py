from flask import redirect,request,render_template
from .models import PostModel,db
from marshmallow import Schema,fields,post_load,INCLUDE,EXCLUDE
from datetime import datetime
from flask.views import MethodView
from flask_smorest import Blueprint,abort

class PostSchema(Schema):
    class Meta:
        unknown = INCLUDE
        ordered = True

    id= fields.Int()
    question = fields.Str(required=False,error_messages={'message':'This field is neccessary'})
    answer = fields.Str()
    user_id = fields.Int()
    # print_time = fields.DateTime(dump_default=datetime.now())  # we can also use load_default

    @post_load
    def makePost(self,data,**kwargs):
        return PostModel(**data)

class postQuerySchema(Schema):
    question = fields.Str()
    answer = fields.Str()
    user_id = fields.Int()


bpa = Blueprint('posts','posts',url_prefix='/posts',description='API of posts')

@bpa.route('/')
class Posts(MethodView):
    # @bpa.arguments(PostSchema,location='query') # here we have to specify from where data is comming into schema in this case it is from queryset
    @bpa.response(200,PostSchema(many=True))
    def get(self):
        return PostModel.query.all()

    @bpa.arguments(postQuerySchema,location='json')  # if we apply this decorator than we have to cathc variable in method here it is new_post . json data will go througth PostSchema
    @bpa.response(201,postQuerySchema)
    def post(self,new_post):
        new_data = PostModel(**new_post)
        db.session.add(new_data)
        db.session.commit()
        return new_post

@bpa.route('/<int:id>')
class PostById(MethodView):
    @bpa.response(200,PostSchema)
    def get(self,id):
        try:
            post = PostModel.query.get(id)
        except ModuleNotFoundError:
            abort(404,message='Post not found')
        return post

    @bpa.arguments(postQuerySchema,location='json')
    @bpa.response(200,PostSchema)
    def put(self,data,id):
        try:
            updated_data=db.session.query(PostModel).filter(PostModel.id==id).update(data)
        except ModuleNotFoundError:
            abort(404,message='Post not found')
        db.session.commit()
        return updated_data

    @bpa.response(204)
    def delete(self,id):
        try:
            db.session.query(PostModel).filter(PostModel.id==id).delete()
            db.session.commit()
        except ModuleNotFoundError :
            abort(404,message='Post not found')
        return {'message':'Post Deleted'}


# bp = Blueprint('user',__name__)

# @bp.post('/post')
# def addPost():
#     if request.is_json:
#         data = request.get_json()
#         new_post = PostModel(question=data['question'],answer=data['answer'],user_id=data['user_id'])
#         db.session.add(new_post)
#         db.session.commit()
#         return {'message':'post added successfully'}

# @bp.put('/<int:id>/post')
# def updatePost(id):
#     old_post = PostModel.query.get(id)
#     if request.is_json:
#         if old_post is not None:
#             new_post_data = request.get_json()
#             old_post.question = new_post_data['question']
#             old_post.answer = new_post_data['answer']
#             db.session.add(old_post)
#             db.session.commit()
#             return {'message':f'post {old_post.question} updated successfully'}

# @bp.delete('/<int:id>/post')
# def deletePost(id):
#     data = PostModel.query.get_or_404(id)
#     db.session.delete(data)
#     db.session.commit()
#     return {'message':f'question ->"{data.question}" is deleted'}

# @bp.get('/posts')
# def allPosts():
#     allPosts = PostModel.query.all()
#     # res = [PostSchema().dump(row) for row in allPosts] 
#     serialized = PostSchema().dump(allPosts,many=True)
#     return serialized

# @bp.post('/<int:total>/bulkadduser')
# def bulkadduser(total):
#     for index in range(1,total):
#         user = PostModel(question=f'demo{index}',answer=f'demo{index}',user_id=1)
#         db.session.add(user)
#         db.session.commit()
#     return {'message':f'total {total} data inserted in auth table'}