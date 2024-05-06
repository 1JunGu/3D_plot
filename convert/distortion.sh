#!/bin/bash
# 定义原始和新的坐标位置
xul=0; dxul=400
yul=0; dyul=50
xur=2200; dxur=1500
yur=0; dyur=50
xlr=2200; dxlr=1900
ylr=1200; dylr=1200
xll=0; dxll=0
yll=1200; dyll=1200

# 执行透视变换并将结果写入临时文件
convert test_rotate.png -matte -virtual-pixel transparent \
    -distort Perspective "$xul,$yul $dxul,$dyul \
     $xur,$yur $dxur,$dyur \
     $xlr,$ylr $dxlr,$dylr \
     $xll,$yll $dxll,$dyll" test_rotate_distortion.png

# 输出完成信息
echo " - distortion done"
