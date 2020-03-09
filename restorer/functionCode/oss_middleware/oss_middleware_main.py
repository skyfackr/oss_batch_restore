'''
@author:skyfackr
@des:oss中间件主文件
'''
import oss2,demjson,sys
from ..globalEnvironmention import globalEnv
class ossMiddleWare():
    '''
    oss中间件，用于解冻
    '''
    def __init__(self,ak,secret,token,endpoint):
        arg_dict=locals()
        globalEnv.logger.debug('code:{}.{} {}'.format(__name__,sys._getframe().f_code.co_name ,demjson.encode(arg_dict)))
        self.__auth=oss2.StsAuth(ak,secret,token,auth_version=oss2.AUTH_VERSION_2)
        self.__endpoint=endpoint
        globalEnv.logger.info('oss init complete')
        return 

    def restore(self,filename,bucketname):
        '''
        解冻
        '''
        bucket=oss2.Bucket(self.__auth,self.__endpoint,bucketname)
        bucket.restore_object(filename)
        return