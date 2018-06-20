import hashlib
from w3lib.html import remove_tags, replace_escape_chars


def get_md5(value):
    if isinstance(value, str):
        value = value.encode('utf-8')
    m = hashlib.md5()
    m.update(value)
    return m.hexdigest()


def value_to_dict(html):
    """
    将douban的书籍信息转换为一个dict
    :param value:
    :return:
    """
    html = remove_tags(html)
    html = replace_escape_chars(html)
    html = html.replace(' ', '')

    # 将value分出来
    filter_value = html.split('  ')
    # 去掉所有全空的元素, 删除元素中间的空格
    no_space_value = []
    for i in filter_value:
        if i is not '':
            if ':' not in i:
                ha = i.replace(' ', '')
                no_space_value.append(ha)
            else:
                ha = i.strip()
                no_space_value.append(ha)

    # 根据元素冒号位置判断键值, 组合为一个新的dict
    value_dict = {}
    for i in range(len(no_space_value)):
        if no_space_value[i][-1] == ':':
            key = no_space_value[i].replace(':', '')
            value = no_space_value[i + 1].replace(' ', '')
            value_dict[key] = value
        elif ':' in no_space_value[i]:
            aset = no_space_value[i].split(':')
            value = aset[1].replace(' ', '')
            value_dict[aset[0]] = value

    return value_dict
