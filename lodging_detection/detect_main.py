from lodging_detection import execute

# 设定路径参数
data_path = "C:/Users/zhangwei/Desktop/小麦倒伏数据/原图png/"      # 原图路径，末尾带 /
out_dir = 'C:/Users/zhangwei/Desktop/result/'         # 输出路径，末尾带 /
name = '20210531-field2-annoted.png'              # 要处理的图片名
sr = 243.4                     # 每像素面积，单位 mm²

# 调用执行
execute(data_path, out_dir, name, sr)
