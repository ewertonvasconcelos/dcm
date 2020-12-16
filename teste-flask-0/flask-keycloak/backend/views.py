from flask import Blueprint, request, redirect, url_for, render_template, flash
from werkzeug.utils import secure_filename
from app import oidc, _logger, app
import logging
import os, time
from backend.dcm import *

view = Blueprint('view', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

#{'exp': 1607915952, 'iat': 1607915652, 'auth_time': 1607914183, 'jti': 'f34dd21a-b5b4-4593-94ea-c73813805618', 'iss': 'http://192.168.1.2:8080/auth/realms/flask-demo', 'aud': 'flask-client', 'sub': '3aace208-029b-4e41-a499-265a15a35b19', 'typ': 'ID', 'azp': 'flask-client', 'session_state': '6d6b4df0-a558-442b-8176-89a19aa1d329', 'at_hash': 'bDfiUj2l9qVaesCNN97-sw', 'acr': '0', 'email_verified': False, 'name': 'Ewerton Silva', 'preferred_username': 'ewerton', 'given_name': 'Ewerton', 'locale': 'pt-BR', 'family_name': 'Silva', 'email': 'ewerton.vasconcelos@poli.ufrj.br'}


@view.route('/')
def index():
    if oidc.user_loggedin:
        #return 'Logged In Home Page - Hi {}. <a href="/logout">Logout</a>'.format(oidc.user_getfield('name'))
        #(['preferred_username', 'email', 'sub'])
        #print(oidc.user_getfield('preferred_username'))
        return render_template('index.html', name=oidc.user_getfield('name'),sub=oidc.user_getfield('sub')+'?dummy=' + str(time.time()))

    else:
        return redirect(url_for('view.login'))


@view.route('/login')
@oidc.require_login
def login():
    _logger.info(
        '{} logged in successfully'.format(oidc.user_getfield('email')))
    return redirect(url_for('view.index'))


@view.route('/logout')
@oidc.require_login
def logout():
    email = oidc.user_getfield('email')
    oidc.logout()
    redirect_url = request.url_root.strip('/')
    keycloak_issuer = oidc.client_secrets.get('issuer')
    keycloak_logout_url = '{}/protocol/openid-connect/logout'.format(
        keycloak_issuer
    )
    _logger.info('{} logged out'.format(email))

    return redirect('{}?redirect_uri={}'.format(
        keycloak_logout_url,
        redirect_url)
    )


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@view.route('/profile', methods=['GET', 'POST'])
@oidc.require_login
def upload_file():
    if oidc.user_loggedin:
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                #filename = secure_filename(file.filename)
                filePath = os.path.abspath(os.getcwd()) + app.config['UPLOAD_FOLDER']
                filename = oidc.user_getfield('sub')
                print(filePath + filename)

                if os.path.exists(filePath + filename):
                    os.remove(filePath+filename)

                file.save(os.path.join(filePath,oidc.user_getfield('sub')))
                return render_template('profile.html',
                sub=oidc.user_getfield('sub')+'?dummy=' + str(time.time()),
                given_name=oidc.user_getfield('given_name'),
                preferred_username=oidc.user_getfield('preferred_username'),
                family_name=oidc.user_getfield('family_name'),
                email=oidc.user_getfield('email'),
                name=oidc.user_getfield('name'))

        return render_template('profile.html',
        sub=oidc.user_getfield('sub')+'?dummy=' + str(time.time()),
        given_name=oidc.user_getfield('given_name'),
        preferred_username=oidc.user_getfield('preferred_username'),
        family_name=oidc.user_getfield('family_name'),
        email=oidc.user_getfield('email'),
        name=oidc.user_getfield('name'))


    else:
        return redirect(url_for('view.login'))



@view.route('/sendkey', methods = ['POST'])
@oidc.require_login
def get_post_javascript_data():
    if oidc.user_loggedin:
        key = request.form['pressed_key']
        print(key)
        sendPs2Key(key)
        return key
    else:
        return redirect(url_for('view.login'))

@view.route('/account')
@oidc.require_login
def change_user_settings():
    if oidc.user_loggedin:
        keycloak_issuer = oidc.client_secrets.get('issuer')
        keycloak_account = '{}/account'.format(keycloak_issuer)
        print(keycloak_account)
        return redirect(keycloak_account)
    else:
        return redirect(url_for('view.login'))

        