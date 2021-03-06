value = '                     作者:                    [美] 伍绮诗                  出版社: 江苏凤凰文艺出版社              出品方: 读客                        原作名: Little Fires Everywhere                     译者:                                孙璐                  出版年: 2018-4              页数: 400              定价: 52.00元              装帧: 平装              丛书: 读客外国小说文库：伍绮诗作品                          ISBN: 9787559407399'


def value_to_dict(html):
    """
    将douban的书籍信息转换为一个dict
    :param value:
    :return:
    """

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



a = value_to_dict(value)


print(a)
