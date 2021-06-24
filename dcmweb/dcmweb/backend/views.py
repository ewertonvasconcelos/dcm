#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Blueprint, request, redirect, url_for, \
    render_template, flash, session, jsonify

from werkzeug.utils import secure_filename
from dcmweb import oidc, _logger, app
import logging
import os
import time
import subprocess
from ..backend.dcm import *
from ..backend.models import *
from ..backend.threads import *
from ..config import config

view = Blueprint('view', __name__)

db.create_all()


# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# {'exp': 1607915952, 'iat': 1607915652, 'auth_time': 1607914183, 'jti': 'f34dd21a-b5b4-4593-94ea-c73813805618', 'iss': 'http://192.168.1.2:8080/auth/realms/flask-demo', 'aud': 'flask-client', 'sub': '3aace208-029b-4e41-a499-265a15a35b19', 'typ': 'ID', 'azp': 'flask-client', 'session_state': '6d6b4df0-a558-442b-8176-89a19aa1d329', 'at_hash': 'bDfiUj2l9qVaesCNN97-sw', 'acr': '0', 'email_verified': False, 'name': 'Ewerton Silva', 'preferred_username': 'ewerton', 'given_name': 'Ewerton', 'locale': 'pt-BR', 'family_name': 'Silva', 'email': 'ewerton.vasconcelos@poli.ufrj.br'}

@view.route('/')
def index():
    if oidc.user_loggedin:

        serversCount = Server.query.count()
        serversCountActive = Server.query.filter(Server.status == 'ON'
                ).count()
        serversList = Server.query.all()
        return render_template('index.html', serversCount=serversCount,
                               serversList = serversList,
                               dcmUptime=subprocess.check_output(['uptime','-p']).decode("utf-8"),
                               serversCountActive=serversCountActive,
                               name=oidc.user_getfield('name'),
                               sub=oidc.user_getfield('sub') + '?dummy='
                                + str(time.time()))
    else:

        return redirect(url_for('view.login'))


@view.route('/login')
@oidc.require_login
def login():
    _logger.info('{} logged in successfully'.format(oidc.user_getfield('email'
                 )))
    return redirect(url_for('view.index'))


@view.route('/logout')
@oidc.require_login
def logout():
    email = oidc.user_getfield('email')
    oidc.logout()
    redirect_url = request.url_root.strip('/')
    keycloak_issuer = oidc.client_secrets.get('issuer')
    keycloak_logout_url = \
        '{}/protocol/openid-connect/logout'.format(keycloak_issuer)
    _logger.info('{} logged out'.format(email))

    return redirect('{}?redirect_uri={}'.format(keycloak_logout_url,
                    redirect_url))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() \
        in config.ALLOWED_EXTENSIONS


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

                # filename = secure_filename(file.filename)

                filePath = os.path.abspath(os.getcwd()) \
                    + app.config['UPLOAD_FOLDER']
                filename = oidc.user_getfield('sub')
                #print(filePath + filename)

                if os.path.exists(filePath + filename):
                    os.remove('/var/www/dcmweb/static/profile/' + filename)
                    #os.remove(filePath + filename)

                file.save(os.path.join(filePath,
                          oidc.user_getfield('sub')))
                return render_template(
                    'profile.html',
                    sub=oidc.user_getfield('sub') + '?dummy='
                        + str(time.time()),
                    given_name=oidc.user_getfield('given_name'),
                    preferred_username=oidc.user_getfield('preferred_username'
                            ),
                    family_name=oidc.user_getfield('family_name'),
                    email=oidc.user_getfield('email'),
                    name=oidc.user_getfield('name'),
                    )

        return render_template(
            'profile.html',
            sub=oidc.user_getfield('sub') + '?dummy='
                + str(time.time()),
            given_name=oidc.user_getfield('given_name'),
            preferred_username=oidc.user_getfield('preferred_username'
                    ),
            family_name=oidc.user_getfield('family_name'),
            email=oidc.user_getfield('email'),
            name=oidc.user_getfield('name'),
            )
    else:

        return redirect(url_for('view.login'))


@view.route('/sendkey', methods=['POST'])
@oidc.require_login
def get_post_javascript_data():
    try:
        key_control = session['KEY_CONTROL']
    except:
        key_control = 0

    key = request.form['pressed_key']
    device = request.form['mgnt_device']

    # time_pressed = request.form['time_pressed']
    # key_time = key + str(time_pressed[-4:-1])

    SendUsbKeyboard(key,device)
    return (key, 200)





@view.route('/account')
@oidc.require_login
def change_user_settings():
    if oidc.user_loggedin:
        keycloak_issuer = oidc.client_secrets.get('issuer')
        keycloak_account = '{}/account'.format(keycloak_issuer)

        # print(keycloak_account)

        return redirect(keycloak_account)
    else:
        return redirect(url_for('view.index'))


@view.route('/server/<server_id>')
@view.route('/server')
@oidc.require_login
def server_management(server_id=""):
    if oidc.user_loggedin:
        if(server_id == ""):
            return redirect(url_for('view.server_list'))

        #try:
        server = Server.query.filter_by(id=server_id).first()
        videoDevsList = get_video_devs()
        mgntDevsList = get_mgnt_devs()
        found=0

        #--- Check video device connected:
        for videoDev in videoDevsList:
            if(videoDev.split(" ")[-1] == server.video_port.split(" ")[-1]):
                server.video_port = videoDev
                db.session.commit()
                found=1
                break

        if(not found):       
            flash('The video device for '+server.hostname+' is not connected, check the device and try again','danger')
            return redirect(url_for('view.server_list'))

        videoDevId = videoDev.split(" ")[0][-1]
        streamPort = "810"+videoDevId
        
        status = ManageService('ustreamer@{}'.format(videoDevId),'start')
        print('DEBUG:', status)
        if (status!=None):
            flash('Error starting the video streamer for server '+server.hostname+' check the log and try again','danger')
            return redirect(url_for('view.server_list'))
            
        #---
        #--- Check mgnt device connected:
        found=0
        for mgntDev in mgntDevsList:
            if(mgntDev.split(" ")[-1] == server.mgnt_port.split(" ")[-1]):
                dev = mgntDev.split(" ")[0]
                server.mgnt_port = mgntDev
                db.session.commit()
                found=1
                break

        if(not found):       
            flash('The management device for '+server.hostname+' is not connected, check the device and try again','danger')
            return redirect(url_for('view.server_list'))
                

        #--- Check server power state 

        serverState = getPowerStateFromMgnt(dev)


        #except:
            
        #    flash('Error opening the console for the server ' + server.hostname + ',check the logs and try again...' , 'danger')
        #    return redirect(url_for('view.server_list'))


        return render_template('server.html',
                               server_id=server_id,
                               serverState=serverState,
                               streamPort=streamPort,
                               dev=server.mgnt_port.split(" ")[0],
                               hostname=server.hostname,
                               videoDev=server.video_port,
                               mgntDev=server.mgnt_port,
                               name=oidc.user_getfield('name'),
                               sub=oidc.user_getfield('sub') + '?dummy='
                                + str(time.time()))
    else:
        return redirect(url_for('view.index'))

@view.route('/list')
@view.route('/list/<int:page>')
@oidc.require_login
def server_list(page=1):
    if oidc.user_loggedin:
        try:
            per_page = session['ITENS_PER_PAGE']
        except:
            per_page = config.ITENS_PER_PAGE

        pagination = Server.query.paginate(page, int(per_page),
                error_out=False)
        minInPage = min((pagination.page - 1) * pagination.per_page
                        + 1, pagination.total)
        maxInPage = min(pagination.total, pagination.page
                        * pagination.per_page)

        videoDevs=get_video_devs()
        mgntDevs=get_mgnt_devs()
        
        return render_template(
            'list.html',
            videoDevs=videoDevs,
            mgntDevs=mgntDevs,
            minInPage=minInPage,
            maxInPage=maxInPage,
            pagination=pagination,
            name=oidc.user_getfield('name'),
            sub=oidc.user_getfield('sub') + '?dummy='
                + str(time.time()),
            )
    else:
        return redirect(url_for('view.index'))


@view.route('/perpage')
@oidc.require_login
def set_perpage():
    session['ITENS_PER_PAGE'] = request.args.get('val')
    print(session['ITENS_PER_PAGE'])
    return redirect(url_for('view.server_list'))


@view.route('/add_server', methods=['POST'])
@oidc.require_login
def add_server():
    if oidc.user_loggedin:
        try:
            server = Server(
                request.form['hostname'],
                request.form['dcname'],
                request.form['rack_id'],
                request.form['position'],
                request.form['video_port'],
                request.form['mgnt_port']
                )
            db.session.add(server)
            db.session.commit()
            flash('Server '+server.hostname+' successfuly added!','success')
            return redirect(url_for('view.server_list'))
        except:
            flash('Error adding server ' + server.hostname + ',check the logs and try again...' , 'danger')
            return redirect(url_for('view.server_list'))
    else:
        return redirect(url_for('view.index'))

@view.route('/remove/<server_id>')
@oidc.require_login
def del_server(server_id=""):
    if oidc.user_loggedin:
        if(server_id==""):
            return redirect(url_for('view.server_list'))
        else:
            try:
                print(server_id)
                server = Server.query.filter_by(id=server_id).first()
                db.session.delete(server)
                db.session.commit()
                flash('Server '+server.hostname+ ' successfuly deleted!','success')
                return redirect(url_for('view.server_list'))
            except:
                flash('Error deleteting server ' + server.hostname + ',check the logs and try again...' , 'danger')
                return redirect(url_for('view.server_list'))
    else:
        return redirect(url_for('view.index'))

@view.route('/performpower', methods=['POST'])
@oidc.require_login
def perform_power():
    if oidc.user_loggedin:
        try:
            request.form['powerOn'],
            request.form['powerOff'],
            request.form['reset']

        except:
            flash('Error adding server ' + server.hostname + ',check the logs and try again...' , 'danger')
            return redirect(url_for('view.server_list'))
    else:
        return redirect(url_for('view.index'))

@view.route('/getpowerstate', methods=['GET'])
@oidc.require_login
def get_power_state():
    if oidc.user_loggedin:
        server_id = request.args.get('server_id')
        dev = request.args.get('dev')
        state=getPowerStateFromMgnt(dev)
        updateServerPowerState(server_id,state)
        return jsonify({'state':state})
    else:
        return redirect(url_for('view.index'))



@view.route('/about')
@oidc.require_login
def about():
    if oidc.user_loggedin:
        return render_template('thirdparty.html',
                               name=oidc.user_getfield('name'),
                               sub=oidc.user_getfield('sub') + '?dummy='
                                + str(time.time()))
    else:
        return redirect(url_for('view.index'))

print("Antes de entrar")
ConfigureNetplan('192.168.1.2/24','192.168.1.1',['8.8.8.8','1.1.1.1'])