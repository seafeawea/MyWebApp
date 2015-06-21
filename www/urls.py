#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'XZ'

import os
import re
import time
import base64
import hashlib
import logging

from transwarp.web import get, post, ctx, view, interceptor, seeother, notfound

from models import User, Blog, Comment


@view('blogs.html')
@get('/')
def index():
    blogs = Blog.find_all()
    users = User.find_first('where email=?', 'admin@example.com')
    return dict(blogs=blogs, users=users)

