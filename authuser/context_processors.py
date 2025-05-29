from django.contrib.auth.models import AnonymousUser

def user_context(request):
    """
    Add user information to the template context for all templates
    """
    # Default empty context
    context = {
        'user': AnonymousUser(),
        'is_authenticated': False,
        'role': None,
        'is_adopter': False,
    }
    
    # If session has user information, add it to the context
    if request.session.get('username'):
        context['user'] = {
            'is_authenticated': True,
            'username': request.session.get('username'),
            'email': request.session.get('email'),
            'nama_lengkap': request.session.get('nama_lengkap'),
            'role': request.session.get('user_role'),
        }
        context['is_authenticated'] = True
        context['role'] = request.session.get('user_role')
        
        # Flag for pengunjung who is also an adopter
        if request.session.get('user_role') == 'pengunjung' and request.session.get('is_adopter'):
            context['is_adopter'] = True
    
    return context
