#**铁路延误数据分析**


##项目背景  
这个项目诞生的原因是公司打算开发新的保险产品，需要数据支持产品定价。我来负责数据的获取清洗与统计建模


##运行环境 
- python 3.7.6
- scrapy 1.6.0
- pandas 1.0.1
- redis-py 3.4.1 # Anaconda自带的redis直接使用的话会报错，一定要conda install redis-py
- pymssql 2.1.4
- scikit-learn 0.22.1
- SQL SERVER 是2014版


##项目板块 
- data_accuisition是原始数据获取部分
- data_processing数据处理加工的部分，数据库的存储过程放在了sql_scripts部分
- data_modeling是数据加工建模部分，暂未完成


##最后 
如果想要探讨数据结论或者需要原始数据用于科研请发邮件，欢迎各位指出本项目中的错误及可优化之处
