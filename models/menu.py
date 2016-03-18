# -*- coding: utf-8 -*-
response.logo = A(B("StopStalk"), _class="navbar-brand",
                  _href=URL('default', 'index'),
                  _id="web2py-logo")
response.title = request.application.replace('_',' ').title()
response.subtitle = ''

response.meta.author = 'Raj Patel raj454raj@gmail.com contactstopstalk@gmail.com StopStalk'
response.meta.description = 'Retrieve submissions of friends\' from various competitive websites and analyse them'
response.meta.keywords = 'stopstalk, raj454raj, IIIT, competitive programming, progress'
response.meta.generator = ''

response.google_analytics_id = None

response.menu = []

if "auth" in locals(): auth.wikimenu()
