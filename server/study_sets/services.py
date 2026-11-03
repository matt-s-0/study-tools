def get_study_folder_permission(folder, user) -> str | None:

    if not user.is_authenticated:
        return 'viewer' if folder.public else None
    if folder.owner_id == user.pk:
        return 'owner'
    if folder.editors.filter(pk=user.pk).exists():
        return 'editor'
    if folder.viewers.filter(pk=user.pk).exists():
        return 'viewer'
    if folder.public:
        return 'viewer'

    return None

def get_study_set_permission(study_set, user) -> str | None:
    
    if not user.is_authenticated:
        return 'viewer' if study_set.public else None

    if study_set.owner_id == user.pk:
        return 'owner'
    if study_set.folder_id and study_set.folder.owner_id == user.pk:
        return 'owner'

    if study_set.editors.filter(pk=user.pk).exists():
        return 'editor'
    if study_set.folder_id and study_set.folder.editors.filter(pk=user.pk).exists():
        return 'editor'

    if study_set.viewers.filter(pk=user.pk).exists():
        return 'viewer'
    if study_set.folder_id and study_set.folder.viewers.filter(pk=user.pk).exists():
        return 'viewer'
    if study_set.public:
        return 'viewer'

    return None