# PyCount V 0.1
统计文件夹或者单个文件代码行数

### optional arguments:

  -h, --help            show this help message and exit
  
  -p PATH, --path PATH  输入你的文件地址
  
  -f FILE, --file FILE  输入你的文件名
  
  -s SORT, --sort SORT  排序
  
  -r, --reverse         逆序：不需要参数

### -s 参数

name total blank code note size

### 文件：

python code_count.py -f linear.py -s code

### 文件夹：

python code_count.py -p code_test/ -s total -r

### 显示结果：
name                total     blank code      note  size
matplot_.py         13        1     12        0     0.33KB
match.py            43        7     6         30    0.86KB
itchat_talk.py      59        9     47        3     2.54KB
calculator.py       74        7     54        13    2.27KB
cell.py             96        29    67        0     2.69KB
code_count.py       135       18    110       7     4.25KB
caculator_plus.py   137       13    112       12    4.24KB
linear.py           244       25    154       65    7.71KB
main.py             320       9     158       153   11.12KB
linked_list.py      391       39    308       44    11.59KB
total               1512      157   1028      327   47.62KB
