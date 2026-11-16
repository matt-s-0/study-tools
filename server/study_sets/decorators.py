from functools import wraps
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden, HttpResponse
from . import services

# login_required is built into validate_user_access & validate_user_edit

# validate_user_access & validate_user_edit do similar things
# -> validate_user_access checks if the user is a viewer, editor, or owner, otherwise renders a http forbidden
# -> validate_user_access checks if the user is a editor or owner
# They both also userRelation to the request, which is either None (not in group), 'viewer', 'editor', or 'owner'

def validate_user_access(model):
    def decorator(viewFunc):
        @wraps(viewFunc)

        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')

            pk = kwargs.get('pk')
            object = get_object_or_404(model, pk=pk)

            if hasattr(object, 'study_set_folder'):
                # is a study set
                user_type = services.get_study_set_permission(object, request.user)
            elif hasattr(object, 'term'):
                # is a study term
                user_type = services.get_study_set_permission(object.study_set, request.user)
            else:
                # is a study folder
                user_type = services.get_study_folder_permission(object, request.user)

            if not user_type or not (user_type == 'owner' or user_type == 'editor' or user_type == 'viewer') and object.public == False:
                return HttpResponseForbidden(f'You do not have permission to access: {object._meta.verbose_name}')
            
            request.object = object
            request.user_relation = user_type

            return viewFunc(request, *args, **kwargs)
        return _wrapped_view
    return decorator
    
def validate_user_edit(model):
    def decorator(viewFunc):
        @wraps(viewFunc)

        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')

            pk = kwargs.get('pk')
            object = get_object_or_404(model, pk=pk)

            if hasattr(object, 'study_set_folder'):
                # is a study set
                user_type = services.get_study_set_permission(object, request.user)
            elif hasattr(object, 'term'):
                # is a study term
                user_type = services.get_study_set_permission(object.study_set, request.user)
            else:
                # is a study folder
                user_type = services.get_study_folder_permission(object, request.user)

            if not user_type or not (user_type == 'owner' or user_type == 'editor'):
                return HttpResponseForbidden(f'You do not have permission to edit: {object._meta.verbose_name}')
            
            request.object = object
            request.user_relation = user_type

            return viewFunc(request, *args, **kwargs)
        return _wrapped_view
    return decorator


# clean_keys removes keys that are '' / None, which Django does not do by default.
def clean_keys(viewFunc):
    def _wrapped_view(request, *args, **kwargs):
        if request.method == 'POST':
            postData = request.POST.copy()

            for key in list(postData.keys()):
                if not postData[key]:
                    postData.pop(key)

            request.POST = postData

        return viewFunc(request, *args, **kwargs)

    return _wrapped_view