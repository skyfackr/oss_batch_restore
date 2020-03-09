'''
@author:skyfackr
@des:主文件
'''
from .globalEnvironmention import globalEnv
from .oss_Middleware import *
import demjson
def main_func(event,context):
    '''
    主函数
    '''
    evt:dict=demjson.decode(event)
    OSSMW:ossMiddleWare=globalEnv.OSSMW
    bucket=evt['bucket']
    if 'prefix' in evt.keys():
        prefix=evt['prefix']
    else:
        prefix=''
    ans_list=OSSMW.getList(bucket,prefix=prefix)
    if ans_list==None:
        return {
            'success':False,
            'msg':'cannot find prefix or no archive file'
        }
    return {
        'success':True,
        'bucket':bucket,
        'list':ans_list
    }