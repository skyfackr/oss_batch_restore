'''
@author:skyfackr
@des:用于获取全局环境变量，对于不存在的变量，则会抛出异常，同时内部自带一个可以有效修改等级的logger，通过专用接口可靠修改
'''
__all__=['globalEnv']
init_register_member=[
    'logger',#必须存在
    'OSSMW',#初始化设定
    'InstanceID',#初始化设定
    'OSSendpoint',
]
import os,logging,sys
def pass_logger(func):
    '''
    当遇到第一个参数为logger的时候将自动raise错误
    '''
    def tester(self,*args,**kwargs):
        name=args[0]
        if name=='logger':
            raise NameError('logger cannot do any action!!!!!!!!!')
        self._GLOBALENV__envStaticMember['logger'].debug('logger passed')
        return func(self,*args,**kwargs)
    return tester



def logger_test(func):
    '''
    每次读取时都会通过此函数检测logger状态，异常则重新注册覆盖
    如需设定设置可以直接修改或者注册入新的logger
    '''
    def isMember(self,name):
        '''
        测试环境变量是否存在
        '''
        if type(name)!=str:
            raise TypeError('must str,not {}'.format(str(type(name))))
        if name in self.__Member__:
            return True
        return False

    def setMember(self,name):
        '''
        向__Member__中注册新的名称
        '''
        if type(name)!=str:
            raise TypeError('must str,not {}'.format(str(type(name))))
        self.__Member__.append(name)
        self._GLOBALENV__envStaticMember['logger'].debug('add __Member__:{}'.format(name))
        return



    def setStaticMember(self,name,value):
        '''
        设定直接输出变量，变量名必须注册于__Member__，否则抛出异常
        '''
        #self.isMemberStrict(name)
        self._GLOBALENV__envStaticMember[name]=value
        self._GLOBALENV__envStaticMember['logger'].debug('set member:{} to {} in static'.format(name,str(value)))
        return




    def tester(self,*args,**kwargs):
        if not isMember(self,'logger'):
            setMember(self,'logger')
        if (not ('logger' in self._GLOBALENV__envStaticMember.keys())) or type(self._GLOBALENV__envStaticMember['logger'])!=type(logging.getLogger()):
            setStaticMember(self,'logger',logging.getLogger())
        if not 'logger' in self._GLOBALENV__ignore_pass_name:
            self._GLOBALENV__ignore_pass_name.append('logger')
        self._GLOBALENV__envStaticMember['logger'].debug('logger tested')
        return func(self,*args,**kwargs)
    #tester(self)
    return tester
globalEnv=None
class __GLOBALENV():
    '''
    （切勿直接使用,请使用globalEnv）获取全局环境变量

    自带logger，可以额外设置覆盖
    '''
    #允许使用的变量名称
    global init_register_member
    __Member__=init_register_member
    #直接输出的常量名，若不在此字典则读取系统环境变量，要求名称必须在__Member__中
    __envStaticMember={
        'logger':logging.getLogger()#必须存在，而且要保证是logger，否则每次调用会自动注册覆盖
    }
    #当在os变量或者直接输出常量中检测到内含字符则认定为未设定的无效字符，予以异常
    __pass_code=[
        '',
        'pass',
        None
    ]
    #当字符在此列表中则不受无效字符检测影响
    __ignore_pass_name=[
        'logger'#必须存在，防止logger误禁用
    ]

    
    def __new__(cls):
        '''
        防止多产生实例，当试图重新实例化一个新的实例时将把globalEnv返回
        '''
        global globalEnv
        if type(globalEnv)!=type(cls):
            globalEnv=super().__new__(cls)
        return globalEnv

    def __init__(self):
        pass

    #@classmethod
    @logger_test
    def isMember(self,name):
        '''
        测试环境变量是否存在
        '''
        if type(name)!=str:
            raise TypeError('must str,not {}'.format(str(type(name))))
        if name in self.__Member__:
            return True
        return False


    

    #@classmethod
    #@logger_test
    def __getattr__(self,name):
        #logger=logging.getLogger()
        
        self.isMemberStrict(name)
        if name in self.__envStaticMember.keys():
            ans=self.__envStaticMember[name]
        else:
            ans=os.environ.get(name)
        if ans in self.__pass_code:
            if not name in self.__ignore_pass_name:
                raise AttributeError('OS Env {} data invaild'.format(name))
        self.__envStaticMember['logger'].debug('get env:{} as:{}'.format(str(name),str(ans)))
        return ans

    #@logger_test
    def isMemberStrict(self,name):
        '''
        严格检测环境变量是否存在，若没有会抛出异常
        '''
        if not self.isMember(name):
            raise AttributeError('OS Env have no attribute called {}'.format(name))
        return

    @pass_logger
    def setStaticMember(self,name,value):
        '''
        设定直接输出变量，变量名必须注册于__Member__，否则抛出异常
        '''
        self.isMemberStrict(name)
        self.__envStaticMember[name]=value
        self.__envStaticMember['logger'].debug('set member:{} to {} in static'.format(name,str(value)))
        return

    @pass_logger
    def deleteStaticMember(self,name):
        '''
        删除直接输出变量，如果没有则抛出异常
        '''
        self.isMemberStrict(name)
        if not name in self.__envStaticMember.keys():
            raise NameError('Static Env have no key called {}'.format(name))
        self.__envStaticMember['logger'].debug('del member:{} in static'.format(name))
        del self.__envStaticMember[name]
        
        return

    @pass_logger
    def setPassIgnoreMember(self,name):
        '''
        注册无效字符检测跳过
        '''
        self.isMemberStrict(name)
        self.__ignore_pass_name.append(name)
        self.__envStaticMember['logger'].debug('set member:{} in pass_ignore'.format(name))
        return

    @pass_logger
    def deletePassIgnoreMember(self,name):
        '''
        删除无效字符检测跳过
        '''
        self.isMemberStrict(name)
        if not name in self.__ignore_pass_name:
            raise NameError('Pass_ignore Env have no key called {}'.format(name))
        self.__envStaticMember['logger'].debug('del member:{} in pass_ignore'.format(name))
        while name in self.__ignore_pass_name:
            self.__ignore_pass_name.remove(name)
        
        return

    def get(self,name):
        '''
        获取一个变量
        '''
        return self.__getattr__(name)

    @logger_test
    @pass_logger
    def setMember(self,name):
        '''
        向__Member__中注册新的名称
        '''
        if type(name)!=str:
            raise TypeError('must str,not {}'.format(str(type(name))))
        self.__Member__.append(name)
        self.__envStaticMember['logger'].debug('add __Member__:{}'.format(name))
        return

    @pass_logger
    def deleteMember(self,name):
        '''
        在__Member__中删除一个名称
        '''
        self.isMemberStrict(name)
        self.__envStaticMember['logger'].debug('del __Member__:{}'.format(name))
        while self.isMember(name):
            self.__Member__.remove(name)
        
        return

    @logger_test
    def setPassCode(self,code):
        '''
        注册新的passcode
        '''
        self.__pass_code.append(code)
        self.__envStaticMember['logger'].debug('set code:{} in pass_code'.format(str(code)))
        return

    @logger_test
    def deletePassCode(self,code):
        '''
        删除passcode
        '''
        if not code in self.__pass_code:
            raise NameError('Pass Code have no key called {}'.format(code))
        self.__envStaticMember['logger'].debug('del code:{} in pass_code'.format(str(code)))
        while code in self.__pass_code:
            self.__pass_code.remove(code)
        

    @logger_test
    def getMember(self):
        '''
        获取Member列表
        '''
        return self.__Member__

    @logger_test
    def getStaticMember(self):
        '''
        获取静态常量列表
        '''
        return self.__envStaticMember.keys()

    @logger_test
    def getPassCode(self):
        '''
        获取passcode列表
        '''
        return self.__pass_code

    @logger_test
    def getIgnorePassList(self):
        '''
        获取跳过pass测试列表
        '''
        return self.__ignore_pass_name
    
            
    @logger_test
    def setLoggerLevel(self,level):
        '''
        设置logger的等级模式
        '''
        self.__envStaticMember['logger'].setLevel(level)
        if len(self.__envStaticMember['logger'].handlers)<=0:
            self.__envStaticMember['logger'].addHandler(logging.NullHandler())
            
        for handler in self.__envStaticMember['logger'].handlers:
            handler.setLevel(level)
        self.__envStaticMember['logger'].debug('set logger level to {}'.format(str(level)))









#我杀bug它全家
globalEnv=__GLOBALENV()