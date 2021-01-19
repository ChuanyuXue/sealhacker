# sealhacker
一个用于提取印章图案的Python程序。

Extracting digital seal by OpenCV in Python.

## Usage
    ## 确保 sealhacker.py 与你需要提取的文件在同一个目录下。
    ## Make sure sealhacker.py and your test example are in the same folder.
    ## 此代码仅对红色的印章有效
    ## This program only works for [RED COLOR] seals.
    
    ## 在命令行里输入下面的命令，test.jpy是你要提取的文件
    ## run below order in your shell/cmd, test.jpg is your test case:
    
    python sealhacker.py test.jpg
    
    ## 结果会生成在自动创建的output目录下，在里面挑选一张你认为最好的输出。
    ## The folder named 'output' will be created and pick your favorite output from this folder.

## Dependency requirements

    numpy==1.16.3
    opencv_python==4.1.0.25
    tqdm==4.46.0
    
## Announcement

该代码免费开源，请勿用于违法行为。

This program is open resourced to every user for free, please use this code in compliance with local laws.

If you have any issue please feel free to contact me at cs_xcy@126.com
