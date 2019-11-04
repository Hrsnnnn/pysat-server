"""views for user.info
"""

import utils.response as Response

from school.models import SchoolHelper
from utils.params import ParamType
from user.models import PermissionHelper
from user.models import UserHelper
from user.models import VerifyHelper
from program.models import ProgramHelper

def get_info(package):
    """process the request of getting user's info
    """
    params = package.get('params')
    username = params.get(ParamType.UsernameWithDefault)
    if username is None:
        user = package.get('user')
    else:
        user = UserHelper.get_user_by_username(username)
    if user is None:
        return Response.error_response("No User")

    user = UserHelper.user_filter(user)
    permission_public = user.get('permission')
    user_id = user.get('id')
    school_id = PermissionHelper.get_user_school(user_id)
    if school_id == 0:
        schoolname = 'public area'
        permission_private = permission_public
    else:
        permission_private = PermissionHelper.get_permission(user_id, school_id)
        school = SchoolHelper.get_school(school_id)
        schoolname = school.get('schoolname')

    download = ProgramHelper.count_user_downloadlog(user_id)

    del user['permission']
    user.update({
        'school_name' : schoolname,
        'permission_public' : permission_public,
        'permission_pirvate' : permission_private,
        'download' : download
    })
    return Response.success_response({'user' : user})

def modify_info(package):
    # pylint: disable-msg=too-many-locals
    # pylint: disable-msg=too-many-return-statements
    # pylint: disable-msg=too-many-branches
    """Process the request of modyfying user's info
    """
    user = package.get('user')
    if user is None:
        return Response.error_response('User Not Logged In')
    user_id = user.get('id')
    params = package.get('params')
    username = params.get(ParamType.UsernameWithDefault)
    realname = params.get(ParamType.RealnameForModify)
    motto = params.get(ParamType.MottoForModify)
    modify_private_permission = params.get(ParamType.PermissionPrivateForModify)
    modify_public_permission = params.get(ParamType.PermissionPublicForModify)

    if modify_private_permission is not None:
        modify_private_permission = int(modify_private_permission)
    if modify_public_permission is not None:
        modify_public_permission = int(modify_public_permission)

    if username is None:                    #修改本人信息
        if modify_private_permission is not None:
            return Response.error_response('Access Denied')
        if modify_public_permission is not None:
            return Response.error_response('Access Denied')
        UserHelper.modify_user(user_id, {
            'realname' : realname,
            'motto' : motto,
        })
        return Response.checked_response('Modify Success')


    schoolid = PermissionHelper.get_user_school(user_id)
    private_permission = PermissionHelper.get_permission(
        user_id, schoolid
    )
    public_permission = user.get('permission')

    if public_permission <= 1:                              #如果是屌丝
        return Response.error_response('Access Denied')
    if private_permission <= 1:                             #如果是屌丝
        return Response.error_response('Access Denied')

    #现在修改人员权限 >= 2
    target_user = UserHelper.get_user_by_username(username)
    target_userid = target_user.get('id')
    target_schoolid = PermissionHelper.get_user_school(target_userid)
    target_public_permission = target_user.get('permission')
    target_private_permission = PermissionHelper.get_permission(
        target_userid, target_schoolid
    )

    if modify_private_permission is not None:
        if modify_private_permission >= private_permission:     #不能越界
            return Response.error_response('Access Denied')
    if modify_public_permission is not None:
        if modify_public_permission >= public_permission:       #不能越界
            return Response.error_response('Access Denied')

    if schoolid == 0:                                       #如果是在野管理员
        if target_public_permission > public_permission:    #不能改领导权限
            return Response.error_response('Access Denied')
        if modify_private_permission is not None:       #不能修改学校权限
            return Response.error_response('Access Denied')
        if modify_public_permission is not None:        #修改在野权限
            UserHelper.modify_user(target_userid, {
                'permission' : modify_public_permission
            })
        if public_permission <= 4:
            if realname is not None:
                return Response.error_response('Access Denied')
            if motto is not None:
                return Response.error_response('Access Denied')
            return Response.checked_response('Modify Success')
        #现在管理员的权限 >= 8 可以随意修改
        UserHelper.modify_user(target_userid, {
            'permission' : modify_public_permission,
            'realname' : realname,
            'motto' : motto
        })
        return Response.checked_response('Modify Success')

    if target_private_permission > private_permission:  #不能该领导权限
        return Response.error_response('Access Denied: Can\'t modify your superior')
    #现在是有学校的管理员
    if target_schoolid != schoolid:                     #不是一个学校
        return Response.error_response('Access Denied: Not The Same School')
    if modify_public_permission is not None:            #不能改变在野权限
        return Response.error_response('Access Denied: Can\'t modify public permission')
    if modify_private_permission is not None:
        PermissionHelper.set_permission(
            target_userid, target_schoolid, modify_private_permission
        )
    if private_permission <= 4:
        if realname is not None:
            return Response.error_response('Access Denied')
        if motto is not None:
            return Response.error_response('Access Denied')
        return Response.checked_response('Modify Success')
    #现在管理员权限 >= 8 可以随意修改
    UserHelper.modify_user(target_userid, {
        'realname' : realname,
        'motto' : motto
    })
    return Response.checked_response('Modify Success')


def set_phone(package):
    """process the request of modifying user's phone
    """
    params = package.get('params')
    phone = params.get(ParamType.Phone)
    code = params.get(ParamType.CAPTCHA)
    session = package.get('session')
    user = package.get('user')
    if not VerifyHelper.check_code(session, phone, code):
        return Response.error_response("CAPTCHA Error")
    UserHelper.modify_user(user['id'], {'phone' : phone})
    return Response.checked_response("Success")
