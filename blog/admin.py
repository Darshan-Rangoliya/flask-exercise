from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

class AdminUserView(ModelView):
    can_delete = False
    column_exclude_list = ['password']
    column_filters = ['username']
    column_searchable_list = ['username']

class AdminPostView(ModelView):
    can_edit = True
    can_delete = False
    can_create = True
    column_searchable_list = ['question',]
    # inline_models = ['post',]
