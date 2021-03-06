"""initialization for pytest

add some items into database for test
"""
from session.models import SessionHelper
from user.models import VerifyHelper, UserHelper, PermissionHelper
from school.models import SchoolHelper, SubjectHelper
from utils.response import analyse_response
from utils.cipher import encrypt

class Initialization:
    """initialization for pytest
    """

    @staticmethod
    def start_session(testcase):
        """start session for test
        """
        response = testcase.client.post('/session/start')
        data = analyse_response(response)
        token = data.get('data').get('token')
        response = testcase.client.get('/myip')
        ip_addr = str(response.content, encoding="utf8")
        testcase.assertIsInstance(ip_addr, str)
        return token, ip_addr

    @staticmethod
    def disconnect(testcase):
        """disconnect session for test
        """
        ret = SessionHelper.disconnect(testcase.token, testcase.ip_addr)
        testcase.assertEqual(ret, True)

    @staticmethod
    def verifyphone(testcase, phone):
        """send verify code
        """
        response = testcase.client.post('/user/sign/verify', {
            'token' : testcase.token,
            'phone' : phone
        })
        testcase.assertEqual(response.status_code, 200)
        data = analyse_response(response)
        testcase.assertEqual(data.get('msg'), 'Success')

        session = SessionHelper.get_session_id(testcase.token, testcase.ip_addr)
        verifycode = VerifyHelper.get_latest_code(session, phone)
        testcase.assertNotEqual(verifycode, None)
        code = verifycode.get('code')
        return code

    @staticmethod
    def register(testcase, username, password, phone, permission=8):
        """register
        """
        code = Initialization.verifyphone(testcase, phone)
        response = testcase.client.post('/user/sign/register', {
            'token' : testcase.token,
            'username' : username,
            'password' : encrypt(password),
            'phone' : phone,
            'CAPTCHA' : code
        })
        testcase.assertEqual(response.status_code, 200)
        data = analyse_response(response)
        testcase.assertEqual(data.get('status'), 1)

        # user = UserHelper.get_user_by_username(username)
        # UserHelper.modify_user(user['id'], {'permission' : permission})
        # user = UserHelper.get_user_by_username(username)
        # testcase.assertEqual(user['permission'], permission)

    @staticmethod
    def login(testcase, username, password):
        """register
        """
        response = testcase.client.post('/user/sign/login', {
            'token' : testcase.token,
            'username' : username,
            'password' : encrypt(password)
        })
        testcase.assertEqual(response.status_code, 200)
        data = analyse_response(response)
        testcase.assertEqual(data.get('status'), 1)

    @staticmethod
    def logout(testcase):
        """register
        """
        response = testcase.client.post('/user/sign/logout', {
            'token' : testcase.token
        })
        testcase.assertEqual(response.status_code, 200)

    @staticmethod
    def create_school(testcase, schoolname, description, headmaster):
        """create a school
        """
        response = testcase.client.post('/school/school/create', {
            'token' : testcase.token,
            'username' : headmaster,
            'school_name' : schoolname,
            'school_description' : description
        })

        testcase.assertEqual(response.status_code, 200)

    @staticmethod
    def create_theme(testcase, schoolname, themename, description, deadline):
        """create a theme
        """
        school = SchoolHelper.get_school_by_name(schoolname)
        if school is None:
            schoolid = 0
        else:
            schoolid = int(school.get('id'))
        response = testcase.client.post('/school/theme/create', {
            'token' : testcase.token,
            'school_id' : schoolid,
            'theme_name' : themename,
            'theme_description' : description,
            'theme_deadline' : deadline
        })

        testcase.assertEqual(response.status_code, 200)

    @staticmethod
    def submit_program(testcase, name, content, readme, schoolname, themename):
        #pylint: disable-msg=too-many-arguments
        """submit a program for test
        """
        school = SchoolHelper.get_school_by_name(schoolname)
        if school is None:
            schoolid = 0
        else:
            schoolid = school.get('id')
        themeid = SubjectHelper.get_subject_by_name(themename).get('id')
        response = testcase.client.post('/program/user/submit', {
            'token' : testcase.token,
            'code_name' : name,
            'code_content' : content,
            'code_readme' : readme,
            'school_id' : schoolid,
            'theme_id' : themeid
        })

        testcase.assertEqual(response.status_code, 200)

    @staticmethod
    def add_user_to_school(testcase, schoolname):
        """add a user to school
        """
        school = SchoolHelper.get_school_by_name(schoolname)
        school_id = school.get('id')
        response = testcase.client.get('/user/info/get', {
            'token' : testcase.token
        })
        response = analyse_response(response)
        data = response.get('data')
        user_id = data.get('user').get('id')
        PermissionHelper.user_join_school(user_id, school_id)

    @staticmethod
    def promote_user(testcase, permission):
        """promote a user
        """
        response = testcase.client.get('/user/info/get', {
            'token' : testcase.token
        })
        response = analyse_response(response)
        data = response.get('data')
        user_id = data.get('user').get('id')
        UserHelper.modify_permission_for_test(user_id, permission)

    @staticmethod
    def promote_user_in_school(testcase, permission):
        """promote a user in school
        """
        response = testcase.client.get('/user/info/get', {
            'token' : testcase.token
        })
        response = analyse_response(response)
        data = response.get('data')
        user_id = data.get('user').get('id')
        school = PermissionHelper.get_user_school(user_id)
        PermissionHelper.set_permission(user_id, school, permission)
