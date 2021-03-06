"""views for school.theme
"""
import utils.response as Response

from school.models import SubjectHelper
from program.models import ProgramHelper
from utils.params import ParamType
from user.models import PermissionHelper

def create_theme(package):
    #pylint: disable-msg=too-many-return-statements
    """create a theme
    """
    user = package.get('user')
    params = package.get('params')
    target_schoolid = params.get(ParamType.SchoolIdWithDefault)
    name = params.get(ParamType.ThemeName)
    msg = params.get(ParamType.ThemeDescription)
    deadline = params.get(ParamType.ThemeDeadline)

    userid = user.get('id')
    school_id = PermissionHelper.get_user_school(userid)
    private_permission = PermissionHelper.get_permission(userid, school_id)
    public_permission = user['permission']

    if public_permission < 2 and private_permission < 2:
        return Response.error_response('Access Denied')

    if public_permission > 1 and private_permission > 1:            #如果这是一个双重管理员
        if target_schoolid is None:
            SubjectHelper.add_subject(0, name, msg, deadline)
            return Response.checked_response('Create Successful')
        target_schoolid = (int)(target_schoolid)
        SubjectHelper.add_subject(target_schoolid, name, msg, deadline)
        return Response.checked_response('Create Successful')

    if public_permission > 1:                                       #如果这只是一个在野管理员
        if school_id is not None:
            return Response.error_response('Access Denied')
        SubjectHelper.add_subject(0, name, msg, deadline)
        return Response.checked_response('Create Successful')

    if school_id is None:                                           #此时必须一个schoolid
        return Response.error_response('Invalid School Id')
    if school_id != target_schoolid:
        return Response.error_response('Not the Same School')
    SubjectHelper.add_subject(school_id, name, msg, deadline)
    return Response.checked_response('Create Successful')

def get_list(package):
    """get theme list
    """
    user = package.get('user')
    params = package.get('params')
    target_schoolid = int(params.get(ParamType.SchoolId))
    page = params.get(ParamType.Page)

    if page is None:
        page = 1
    page = int(page)

    user_id = user.get('id')
    school_id = PermissionHelper.get_user_school(user_id)
    public_permission = user.get('permission')

    if target_schoolid != 0:
        if target_schoolid != school_id and public_permission < 8:
            return Response.error_response('Access Denied')

    theme_list = SubjectHelper.get_subjects(
        target_schoolid, 0, page
    )

    for theme in theme_list:
        theme.update({
            'count' : ProgramHelper.get_subject_programs_count(theme.get('id'))
        })
    ret = {
        'tot_count' : SubjectHelper.get_subject_count(target_schoolid, 0),
        'now_count' : len(theme_list),
        'theme_list' : theme_list
    }

    return Response.success_response(ret)

def delete_theme(package):
    #pylint: disable-msg=too-many-return-statements
    """delete theme
    """
    user = package.get('user')
    user_id = user.get('id')
    school_id = PermissionHelper.get_user_school(user_id)

    params = package.get('params')
    theme_id = int(params.get(ParamType.ThemeId))
    theme = SubjectHelper.get_subject_with_schoolid(theme_id)
    if theme is None:
        return Response.error_response('No Subject')
    theme_schoolid = theme.get('school_id')

    private_permission = PermissionHelper.get_permission(user_id, school_id)
    public_permission = user['permission']

    if private_permission > 4:                                  #为超级用户
        SubjectHelper.delete_subject(theme_id)
        return Response.checked_response('Deleted Success')

    if theme_schoolid == 0:
        if public_permission < 4:
            return Response.error_response('Access Denied')
        SubjectHelper.delete_subject(theme_id)
        return Response.checked_response('Deleted')

    if private_permission < 4:                                  #非高级管理员
        return Response.error_response('Access Denied')

    if school_id != theme_schoolid:                         #学校必须匹配
        return Response.error_response('Acess Denied')
    SubjectHelper.delete_subject(theme_id)
    return Response.checked_response('Delete Success')

def modify_theme(package):
    #pylint: disable-msg=too-many-return-statements
    """modify theme
    """
    user = package.get('user')
    user_id = user.get('id')
    school_id = PermissionHelper.get_user_school(user_id)

    params = package.get('params')
    theme_id = int(params.get(ParamType.ThemeId))
    title = params.get(ParamType.ThemeNameWithDefault)
    description = params.get(ParamType.ThemeDescriptionWithDefault)
    deadline = params.get(ParamType.ThemeDeadlineWithDefault)

    theme = SubjectHelper.get_subject_with_schoolid(theme_id)
    if theme is None:
        return Response.error_response('No Subject')
    theme_schoolid = theme.get('school_id')

    private_permission = PermissionHelper.get_permission(user_id, school_id)
    public_permission = user['permission']

    if private_permission > 4:                                  #为超级用户
        SubjectHelper.modify_subject(theme_id, title, description, deadline)
        return Response.checked_response('Modified')

    if theme_schoolid == 0:
        if public_permission < 4:
            return Response.error_response('Access Denied')
        SubjectHelper.modify_subject(theme_id, title, description, deadline)
        return Response.checked_response('Modified')

    if private_permission < 4:                                  #非高级管理员
        return Response.error_response('Access Denied')

    if school_id != theme_schoolid:                         #学校必须匹配
        return Response.error_response('Acess Denied')

    SubjectHelper.modify_subject(theme_id, title, description, deadline)
    return Response.checked_response('Modify Success')
