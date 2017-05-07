from django.contrib.auth import get_user_model


def get_data(instance, exclude_fields=None):
    if exclude_fields is None:
        exclude_fields = []
    else:
        exclude_fields = list(exclude_fields)
    exclude_fields.append('_state')

    data = vars(instance)
    for ef in exclude_fields:
        data.pop(ef)
    return data


def sync_calsusers(calsusers=None, relayusers=None):
    User = get_user_model()
    if not calsusers:
        calsusers = User.objects.using('cals').all()
    if not relayusers:
        relayusers = User.objects.using('default').all()
    created = set()
    updated = set()
    exclude_fields = [
        'last_login',
        'is_superuser',
        'is_staff',
    ]
    for cu in calsusers:
        try:
            ru = relayusers.get(id=cu.id)
        except User.DoesNotExist:
            ru = User.objects.using('default').create(
                **get_data(cu, exclude_fields)
            )
            created.add(ru)
            continue
        updated.add(ru)
    return (created, updated)
