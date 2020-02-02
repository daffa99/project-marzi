# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

from __future__ import unicode_literals

import datetime
import errno
import json
import os
import sys
import tempfile
import demoji
import requests
from requests_oauthlib import OAuth1Session
from argparse import ArgumentParser

from flask import Flask, request, abort, send_from_directory
from werkzeug.middleware.proxy_fix import ProxyFix
# Marzi material
from marzi import marzi_act

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    LineBotApiError, InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    MemberJoinedEvent, MemberLeftEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton,
    ImageSendMessage)

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1, x_proto=1)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None or channel_access_token is None:
    print('Specify LINE_CHANNEL_SECRET and LINE_CHANNEL_ACCESS_TOKEN as environment variables.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')


# function for create tmp dir for download content
def make_static_tmp_dir():
    try:
        os.makedirs(static_tmp_path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(static_tmp_path):
            pass
        else:
            raise


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except LineBotApiError as e:
        print("Got exception from LINE Messaging API: %s\n" % e.message)
        for m in e.error.details:
            print("  %s: %s" % (m.property, m.message))
        print("\n")
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text
    if text == "test" or text == "tes":
        confirm_template = ConfirmTemplate(text='Try Me!', actions=[
            MessageAction(label='Click Here to Try', text='Your so Beautiful'),
        ])
        template_message = TemplateSendMessage(
            alt_text='Try Marzi', template=confirm_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    else:
        url = marzi_act(text)
        if url is not False:
            line_bot_api.reply_message(event.reply_token, ImageSendMessage(url))

@handler.add(FollowEvent)
def handle_follow(event):
    confirm_template = ConfirmTemplate(text='Try Me!', actions=[
        MessageAction(label='Click Here to Try', text='Your so Beautiful'),
    ])
    template_message = TemplateSendMessage(
        alt_text='Try Marzi', template=confirm_template)
    line_bot_api.reply_message(event.reply_token, template_message)

@handler.add(JoinEvent)
def handle_join(event):
    confirm_template = ConfirmTemplate(text='Try Me!', actions=[
        MessageAction(label='Click Here to Try', text='Your so Beautiful'),
    ])
    template_message = TemplateSendMessage(
        alt_text='Try Marzi', template=confirm_template)
    line_bot_api.reply_message(event.reply_token, template_message)

@handler.add(MemberJoinedEvent)
def handle_member_joined(event):
    confirm_template = ConfirmTemplate(text='Try Me!', actions=[
        MessageAction(label='Click Here to Try', text='Your so Beautiful'),
    ])
    template_message = TemplateSendMessage(
        alt_text='Try Marzi', template=confirm_template)
    line_bot_api.reply_message(event.reply_token, template_message)



if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', type=int,
                            default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    # create tmp dir for download content
    make_static_tmp_dir()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
