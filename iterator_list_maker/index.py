# -*- coding: utf-8 -*-
from functionCode.globalEnvironmention import globalEnv
from functionCode.mainfunc import main_func
from functionCode.oss_Middleware import ossMiddleWare
import logging,demjson

# if you open the initializer feature, please implement the initializer function, as below:
# def initializer(context):
#   logger = logging.getLogger()
#   logger.info('initializing')

DEBUG_MODE=False

def init(context):
  globalEnv.setStaticMember('InstanceID',context.requestId)
  id=context.credentials.accessKeyId
  secret=context.credentials.accessKeySecret
  token=context.credentials.securityToken
  global DEBUG_MODE
  if DEBUG_MODE==True:
    globalEnv.setLoggerLevel(logging.DEBUG)
    globalEnv.logger.debug('logger debug mode on')
  globalEnv.setStaticMember('OSSMW',ossMiddleWare(id,secret,token,globalEnv.OSSendpoint))
  globalEnv.logger.info('init success')


def handler(event, context):
  globalEnv.logger.info('request arrived'+demjson.encode({
    'InstanceID':globalEnv.InstanceID,
    'requestid':context.requestId,
    'payload':str(event),
  }))
  ans=main_func(event,context)
  if type(ans)==dict:
    ans=demjson.encode(ans)
  globalEnv.logger.info('ans:'+str(ans))
  return ans