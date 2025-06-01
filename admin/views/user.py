from sqladmin import ModelView

from models import User


class UserAdmin(ModelView, model=User):
    name = 'User'
    names = 'Users'
    icon = 'fa fa-user'

    is_async = True

    column_list = ['id', 'username', 'fullname', 'create_at', 'update_at']
    form_columns = ['username', 'fullname']
    column_default_sort = ('id', True)
    column_sortable_list = ['id', 'username', 'fullname', 'create_at', 'update_at']
    column_searchable_list = ['username', 'fullname']
