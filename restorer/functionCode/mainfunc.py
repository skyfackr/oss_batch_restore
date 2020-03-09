'''
@author:skyfackr
@des:主文件
'''
from .oss_middleware import *
import demjson
from .globalEnvironmention import globalEnv
def main_func(event,context):
    '''
    主函数
    '''
    evt=demjson.decode(event)
    OSSMW:ossMiddleWare=globalEnv.OSSMW
    filename=evt['filename']
    bucket=evt['bucket']
    OSSMW.restore(filename,bucket)
    globalEnv.logger.info('restore {}/{} success'.format(bucket,filename))
    return