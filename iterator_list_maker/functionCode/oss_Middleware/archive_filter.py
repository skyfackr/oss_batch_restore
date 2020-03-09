'''
@author:skyfackr
@des:从列表中筛选出归档类文件
'''
import oss2,demjson,sys
from ..globalEnvironmention import globalEnv
def get_archive_list(filelist:list,bucket:oss2.Bucket):
    '''
    分离出归档类型文件
    '''
    arg_dict=locals()
    globalEnv.logger.debug('code:{}.{} {}'.format(__name__,sys._getframe().f_code.co_name ,str(arg_dict)))
    ans=[]
    for filename in filelist:
        meta=bucket.head_object(filename)
        if meta.headers['x-oss-storage-class']==oss2.BUCKET_STORAGE_CLASS_ARCHIVE:
            ans.append(filename)
    globalEnv.logger.debug('archive list:'+str(ans))
    return ans