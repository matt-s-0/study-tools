from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django_ratelimit.decorators import ratelimit
from .forms import *
from .decorators import *

#################### Study Folders ####################

# View the create study folder page
@require_GET
@login_required
@ratelimit(key="user", rate="10/m", block=True)
def view_create_study_folder(request) -> HttpResponse:
    return render(request, 'study_folders/create_study_folder.html')

# View the edit study folder page
@require_GET
@validate_user_edit(StudyFolder)
@ratelimit(key="user", rate="10/m", block=True)
def view_edit_study_folder(request, pk) -> HttpResponse:
    return render(request, 'study_folders/edit_study_folder.html', {'study_folder': request.object})

# Handles study folder creation
@require_POST
@login_required
@clean_keys
@ratelimit(key="user", rate="5/m", block=True)
def create_study_folder(request):
    form = study_folder_form(request.POST, user=request.user)

    if form.is_valid():
        newForm = form.save(commit=False)
        newForm.owner = request.user

        newForm.save()
        form.save_m2m()

        return redirect('home')
    
    return render(request, 'study_folders/create_study_folder.html', {'form': form})

# Handles editing study folders
@require_POST
@validate_user_edit(StudyFolder)
@clean_keys
@ratelimit(key="user", rate="10/m", block=True)
def edit_study_folder(request, pk):
    form = study_folder_form(request.POST, instance=request.object)

    if form.is_valid(): 
        form.save()
        return redirect('home')
        
    return render(request, 'study_folders/edit_study_folder.html', {'form': form, 'study_folder': request.object})

# Handles study folder deletion
@require_POST
@validate_user_edit(StudyFolder)
@ratelimit(key="user", rate="10/m", block=True)
def delete_study_folder(request, pk) -> HttpResponse:
    request.object.delete()
    
    return redirect('home')

# Handles viewing study folders
@require_GET
@validate_user_access(StudyFolder)
@ratelimit(key="user", rate="20/m", block=True)
def view_study_folder(request, pk):

    context = {
        'study_folder': request.object
    }

    if request.userRelation == 'owner':
        return render(request, 'study_folders/owner_study_folder.html', context)
    elif request.userRelation == 'viewer':
        return render(request, 'study_folders/editor_study_folder.html', context)
    return render(request, 'study_folders/viewer_study_folder.html', context)

#################### Study Sets ####################

# View the create study set page
@require_GET
@login_required
@ratelimit(key="user", rate="10/m", block=True)
def view_create_study_set(request) -> HttpResponse:
    return render(request, 'study_sets/create_study_set.html')

# View the edit study set page
@require_GET
@validate_user_edit(StudySet)
@ratelimit(key="user", rate="10/m", block=True)
def view_edit_study_set(request, pk) -> HttpResponse:
    return render(request, 'study_sets/edit_study_set.html', {'study_set': request.object})

# Handles creating a study set
@require_POST
@login_required
@clean_keys
@ratelimit(key="user", rate="5/m", block=True)
def create_study_set(request):
    form = study_set_form(request.POST, user=request.user)

    if form.is_valid():
        newForm = form.save(commit=False)
        newForm.owner = request.user

        newForm.save()
        form.save_m2m()

        return redirect('home')
    
    return render(request, 'study_sets/create_study_set.html', {'form': form})

# Handles editing a study set
@require_POST
@validate_user_edit(StudySet)
@clean_keys
@ratelimit(key="user", rate="10/m", block=True)
def edit_study_set(request, pk):
    form = study_folder_form(request.POST, instance=request.object)

    if form.is_valid(): 
        form.save()
        return redirect('home')
        
    return render(request, 'study_sets/edit_study_set.html', {'form': form, 'study_set': request.object})

# Handles study set deletion
@require_POST
@validate_user_edit(StudySet)
@ratelimit(key="user", rate="10/m", block=True)
def delete_study_set(request, pk) -> HttpResponse:
    request.object.delete()
    
    return redirect('home')

# Handles viewing study sets
@require_GET
@validate_user_access(StudySet)
@ratelimit(key="user", rate="20/m", block=True)
def view_study_set(request, pk):

    context = {
        'study_set': request.object
    }

    if request.userRelation == 'owner':
        return render(request, 'study_sets/owner_study_set.html', context)
    elif request.userRelation == 'viewer':
        return render(request, 'study_sets/editor_study_set.html', context)
    return render(request, 'study_sets/viewer_study_set.html', context)

#################### Study Terms ####################

# Handles creating study terms
@require_POST
@validate_user_edit(StudyTerm)
@clean_keys
@ratelimit(key="user", rate="30/m", block=True)
def create_study_term(request, pk):
    form = study_term_form(request.POST)

    if form.is_valid():
        newForm = form.save(commit=False)
        newForm.study_set = request.object

        newForm.save()
        form.save_m2m()

# Handles editing a study term
@require_POST
@validate_user_edit(StudyTerm)
@clean_keys
@ratelimit(key="user", rate="30/m", block=True)
def edit_study_term(request, pk):
    form = study_term_form(request.POST, instance=request.object)

    if form.is_valid(): 
        form.save()

# Handles study term deletion
@require_POST
@validate_user_edit(StudyTerm)
@ratelimit(key="user", rate="100/m", block=True)
def delete_study_term(request, pk):
    request.object.delete()

#################### AI Services ####################

from ai_services import grade
@require_POST
@validate_user_access(StudyTerm)
@ratelimit(key="user", rate="10/m", block=True)
def grade_answers(request, pk, answers):

    
    return


from ai_services import answer_check
@require_POST
@validate_user_access(StudyTerm)
@ratelimit(key="user", rate="45/m", block=True)
def check_answer(request, pk):
    user_answer = request.POST.get("answer")

    question = object.term #type:ignore
    correct_answer = object.definition #type:ignore

    result = answer_check.check(question, correct_answer, user_answer)

    return JsonResponse({
        "correct": result,
    })


from ai_services import generate_choices
@require_POST
@validate_user_edit(StudySet)
@ratelimit(key="user", rate="5/h", block=True)
def generate_study_set_answer_choices(request, pk):

    
    return

@require_POST
@validate_user_edit(StudyTerm)
@ratelimit(key="user", rate="8/m", block=True)
def generate_study_term_answer_choices(request, pk):

    
    return