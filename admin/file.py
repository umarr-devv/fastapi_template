from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from sqladmin import ModelView, action

from models import File


class FileAdmin(ModelView, model=File):
    name = 'File'
    names = 'Files'
    icon = 'fa fa-file'

    is_async = True

    column_list = ['id', 'file_name', 'file_type', 'create_at', 'update_at']
    form_columns = ['file_name', 'file_type']
    column_default_sort = ('id', True)
    column_sortable_list = ['id', 'file_name', 'file_type', 'create_at', 'update_at']
    column_searchable_list = ['file_name', 'file_type.name']

    @action(
        name='Action', label='Action', confirmation_message='Do this?'
    )
    async def do_action(self, request: Request):
        referer = request.headers.get("referer", "/admin")
        return RedirectResponse(url=referer, status_code=303)
