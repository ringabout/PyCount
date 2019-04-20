import logging
from collections import namedtuple
import os
import sys
import argparse
from reprlib import repr


"""更多精彩，请关注微信公众号：Python高效编程"""

def parse_args():
    parser = argparse.ArgumentParser(usage='命令行统计代码信息', description='统计文件夹或者单个文件信息')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-p', '--path', help='输入你的文件地址', default='')
    group.add_argument('-f', '--file', help='输入你的文件名', default='')
    parser.add_argument('-s', '--sort', help='排序', default='total')
    parser.add_argument('-r', '--reverse', help='逆序：不需要参数', action='store_false', default=True)
    logging.basicConfig(level=logging.INFO)
    logging.debug('解析参数')
    args = parser.parse_args()
    logging.debug('解析完成')
    return args


def get_path():
    args = parse_args()
    path, file = args.path, args.file
    if os.path.exists(path):
        logging.debug('获取路径')
        # 可以改变连接方式
        # 判断 / 或者 \ 是否在路径中
        return [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.py')]
    if os.path.exists(file) and file.endswith('.py'):
        logging.debug('获取文件')
        return [file]
    logging.debug('不应该执行')
    raise OSError("输入路径不存在")


# 总行数 空行数 代码行 注释行 文件大小
file_tuple = namedtuple('file', 'name total blank code note size')
def process_note(lines, symbol):
    note = 0

    for line in lines:
        note += 1
        line = line.strip()
        if line.endswith(symbol):
            break
    return note


def get_info():
    for path in get_path():
        name = path.split('\\' and '/')[-1]
        total = 0
        blank = 0
        code = 0
        note = 0
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            temp_note = 0
            # for num, line in tqdm(enumerate(lines), ascii=True ,total=len(lines)):
            for num, line in enumerate(lines):
                # import time
                # time.sleep(0.001)
                logging.debug('开始读取行')
                total += 1
                line = line.strip()
                if temp_note > 1:
                    temp_note -= 1
                    continue

                if not len(line):
                    blank += 1
                elif line.startswith('#'):
                    note += 1
                elif line.startswith('"' or '"""' or "'" or "'''"):
                    if line.startswith('"""') or line.startswith("'''"):
                        temp_note = process_note(lines[num:], line[:3])
                    else:
                        temp_note = process_note(lines[num:], line[0])
                    note += temp_note
                else:
                    code += 1
                logging.debug(total)
        size = os.path.getsize(path)
        yield file_tuple(name, total, blank, code, note, size)

def calculate_size(size):
    kb = 1024
    mb = 1024 ** 2
    gb = 1024 ** 2
    if size < mb:
        size /= kb
        result = 'KB'
    elif mb <= size < gb:
        size /= mb
        result = 'MB'
    elif size >= gb:
        size /= gb
        result = 'GB'
    return size, result


def sorted_info():
    args = parse_args()
    key, reverse = args.sort, args.reverse
    from operator import attrgetter
    info = sorted(get_info(), key=attrgetter(key), reverse=reverse)
    return info


def display_info():
    total = 0
    blank = 0
    code = 0
    note = 0
    size = 0
    col = f'name{" "*16}total     blank code      note  size'
    print(col)
    for info in sorted_info():
        fmt = '{:.2f}{}'.format(*calculate_size(info.size))
        print(f'{info.name:<20}{info.total:<10}{info.blank:<6}{info.code:<10}{info.note:<6}{fmt}')
        total += info.total
        blank += info.blank
        code += info.code
        note += info.note
        size += info.size
    fmt = '{:.2f}{}'.format(*calculate_size(size))
    print(f'total{" "*15}{total:<10}{blank:<6}{code:<10}{note:<6}{fmt}')


if __name__ == '__main__':
    display_info()