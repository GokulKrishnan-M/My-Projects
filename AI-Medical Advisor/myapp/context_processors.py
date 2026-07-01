from .models import User


def portal_user(request):
    """Expose the current portal user (if any) for shared templates."""
    uid = request.session.get("uid")
    if not uid:
        return {"portal_user": None}

    try:
        user = User.objects.get(loginId=uid)
    except User.DoesNotExist:
        user = None

    return {"portal_user": user}
