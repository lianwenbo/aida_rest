# aida_rest
Aida rest 服务器实现，用于支持 https://github.com/bigyelow/aida.git
的服务器实现版本，主要是用了flask实现了rest的服务

# Notice
在pip-req.txt中，需要额外配置一个发送短信的sdk,这里使用的是aliyun的环境

20180101
auth token存在一个问题，需要确认对应的register接口，否则必然出错