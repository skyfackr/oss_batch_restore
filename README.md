# aliyun_oss_batch_restore
 use FNF to restore all archive file in one path


<h3>third party required</h2>
    1. iterator_list_maker
       1. oss2
       2. aliyun-python-sdk-core
       3. aliyun-python-sdk-core-v3
       4. demjson
       5. pycrypto
    2. restorer
       1. oss2
       2. aliyun-python-sdk-core
       3. aliyun-python-sdk-core-v3
       4. demjson

<h2>输入流规范</h2>
    {
        'bucket':(str)(必选)bucket名称，要求在函数设定endpoint中,
        'prefix':(str)(默认为'')前缀，留空则为全部
    }

<h2>输出流规范(待实现，拟增加一个函数进行结果统计)</h2>
    {
        'restore_count':(int)解冻文件数目,
        'success_count':(int)成功数目,
        'fail_count':(int)失败数目,
        'success_list':(list)解冻成功文件名称列表,
        'fail_list':(list)失败列表,
        'time':(int)消耗时间,
    }

    如果第一步获取列表失败，则仅需返回一个msg


<h2>函数工作流流程</h2>
    iterator_list_maker->restorer

<h2>函数用途及规范</h2>
    1. iterator_list_maker
        1. 用途
            用于列举指定前缀下的所有归档文件并生成列表
        2. 输入流
            同工作流输入流
        3. 输出流
            {
                'success':true|false,
                'msg':(str)如果失败，这里写明原因,
                'list':(list)文件名称列表,
                'bucket':(str)bucket名称,
            }
    2. restorer
        1. 用途
            用于解冻文件
        2. 输入流
            {
                'filename':(str)文件名,
                'bucket':(str)bucket名称
            }
        3. 输出流
            {
                'success':true|false,
            }