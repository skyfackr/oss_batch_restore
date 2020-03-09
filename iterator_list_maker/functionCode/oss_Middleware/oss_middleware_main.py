'''
@author:skyfackr
@des:oss中间件主程序
'''
import oss2,demjson,sys
from ..globalEnvironmention import globalEnv
from .archive_filter import get_archive_list
class ossMiddleWare():
    '''
    oss中间件主程序
    '''
    def __init__(self,ak,secret,token,endpoint):
        arg_dict=locals()
        globalEnv.logger.debug('code:{}.{} {}'.format(__name__,sys._getframe().f_code.co_name ,demjson.encode(arg_dict)))
        self.__auth=oss2.StsAuth(ak,secret,token,auth_version=oss2.AUTH_VERSION_2)
        self.__endpoint=endpoint
        globalEnv.logger.info('oss init complete')
        return 

    def getList(self,bucketName,prefix=''):
        '''
        获取待解冻列表

        如果获取失败或者没有则返回空
        '''
        arg_dict=locals()
        globalEnv.logger.debug('code:{}.{} {}'.format(__name__,sys._getframe().f_code.co_name ,demjson.encode(arg_dict)))
        try:
            bucket=oss2.Bucket(self.__auth,self.__endpoint,bucketName)
        except Exception as e:
            globalEnv.warn('bucket connect error:{},{}'.format(str(type(e)),str(e)))
            globalEnv.logger.debug('exception:',exc_info=e)
            return None
        raw_list=[]
        for obj in oss2.ObjectIterator(bucket,prefix=prefix):
            raw_list.append(str(obj.key))
        ans_list=get_archive_list(raw_list,bucket)
        globalEnv.info('get archive list success!')
        return ans_list