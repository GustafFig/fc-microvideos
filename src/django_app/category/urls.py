from django.urls import path

from django_app import container

from .api import CategoryResource

urlpatterns = [
    path('categories/', CategoryResource.as_view(
        create_use_case=container.Container.use_case_category_create_category,
        list_use_case=container.Container.use_case_category_list_category,
    )),
    path('categories/<uuid:id>/', CategoryResource.as_view(
        get_use_case=container.Container.use_case_category_get_category,
        update_use_case=container.Container.use_case_category_update_category,
        delete_use_case=container.Container.use_case_category_delete_category,
    ))
]
