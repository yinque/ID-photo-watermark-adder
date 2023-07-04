r"""
windows系统将支持的字体信息储存在注册表里，大部分字体都储存在'C:\Windows\Fonts\'目录下，
本模块遍历'C:\Windows\Fonts\'路径下的ttf文件，建立“字体文件名-字体样式-字体文件名”之间的关系，如“Arial-Bold-arial.ttf”
获取所有字体名
根据字体名获取字体名支持的样式
根据（字体名，字体样式）获取对应的字体文件
"""
import os
from PIL import ImageFont


class SystemFont:
    def __init__(self):
        self.__font_path_map = dict()  # （字体名，字体样式）-字体文件名map
        self.__name_style_map = dict()  # 字体名-字体样式map
        # windows大部分字体文件路径
        folder_path1 = r'C:\Windows\Fonts'
        folder_path2 = rf'C:\Users\{os.getlogin()}\AppData\Local\Microsoft\Windows\Fonts'
        # 获取文件夹中的所有文件名
        file_names1 = os.listdir(folder_path1)
        file_names2 = os.listdir(folder_path2)

        file_full_paths = [os.path.join(folder_path1, file) for file in file_names1]
        file_full_paths2 = [os.path.join(folder_path2, file) for file in file_names2]
        file_full_paths.extend(file_full_paths2)
        # 筛选出字体文件名
        font_files = [file for file in file_full_paths if file.endswith('.ttf')]
        # 排除不支持的字体文件
        font_files.remove(r"C:\Windows\Fonts\mstmc.ttf")
        # 遍历所有字体文件名
        for font_file in font_files:
            # 使用ImageFont.TrueType加载字体文件
            font = ImageFont.truetype(font_file)
            # 获取字体的名称
            font = font.getname()
            name = font[0]
            style = font[1]

            if self.__name_style_map.get(name):
                self.__name_style_map[name].append(style)
            else:
                self.__name_style_map[name] = [style]
            self.__font_path_map[font] = font_file

    def get_names(self):
        """
        获取所有支持的字体名
        :return: 列表
        """
        return list(self.__name_style_map.keys())

    def get_styles(self, name):
        """
        获取字体支持的样式
        :param name: 字体名
        :return: 列表
        """
        return self.__name_style_map[name]

    def get_path(self, font: tuple):
        """
        获取字体路径
        :param font: 字体，格式为(字体名,字体样式)
        :return: 字符串
        """
        return self.__font_path_map[font]


# test
if __name__ == '__main__':
    font_name = "Arial"
    sf = SystemFont()
    font_styles = sf.get_styles(font_name)
    print(f"{font_name}'s style: {font_styles}")
    path = sf.get_path((font_name, font_styles[0]))
    print(f"{font_name} {font_styles[0]}'s path: {path}")

    print("all supported font:")
    print(sf.get_names())
