"""requests: session
"""

from django.views.decorators.csrf import csrf_exempt

import server.utils.response as Response
import server.utils.models.session as Session
import server.utils.models.user as User

from server.utils.params import check_params, ParamType
from server.utils.request import get_ip

@csrf_exempt
def start_session(request):
    """process the request of creating a session
    """
    if request.method == 'POST':
        ip_address = get_ip(request)

        token = Session.add_session(ip_address=ip_address)
        return Response.success_response(data={'token' : token})
    return Response.invalid_request()


@csrf_exempt
def check_session(request):
    """process the request of check session
    """
    if request.method == 'GET':
        ip_address = get_ip(request)
        
        token = request.GET.get('token')
        error = check_params({
            ParamType.Token : token
        })
        if error is not None:
            return error

        session_id = Session.get_session_id(token, ip_address)
        if session_id is None:
            return Response.error_response("NoSession")
        
        user = User.get_user_by_session(session_id)
        user = User.user_filter(user)
        return Response.success_response({'user' : user})
    return Response.invalid_request()
