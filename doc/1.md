* 进度条
* 从eel.get_data返回的数据获取行、列数的bug
    * processed
* 属性列选择，除了可视化模块，数据预处理接口也应该支持处理指定列的数据。所以将属性列的视图从模态窗口改变为主页的panel
    * processing: 视图已经完成，需要改接口
* 优化app.read_file，应该支持更多类型的数据文件，而不只是csv
    * processing
* 加速
    * problem: pp模块与eel模块冲突，eel模块导入后的初始化影响到pp调用subprocess模块，于是报错
    * processed: pp + True

* 注意：重置数据后，会重新加载数据，而data_version、image_count、images、op_records也会被重置
* 数据有空值时规范化会全变空值