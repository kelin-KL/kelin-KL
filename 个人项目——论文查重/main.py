import re
import jieba
import jieba.analyse
import numpy
from scipy import spatial
numpy.seterr(divide='ignore', invalid='ignore')

"""
该类 `DuplicateChecking` 实现了文本查重功能。
采用了两种处理方式：
1. 使用 jieba 库进行分词处理；
2. 使用关键词提取技术处理长文本；
最终通过余弦相似度来计算文本之间的相似度。
"""
class DuplicateChecking:
    def __init__(self):
        # 初始化类变量，分别存储原始文本和待查重文本的内容，以及它们的分词列表
        self.original_text = ""
        self.compare_text = ""
        self.original_list = []
        self.compare_list = []
        self.word_store = []  # 存储文本中所有独立出现的词汇

    # 读取原始文件和待查重文件
    def read_file(self):
        """
        从用户指定的文件路径读取文本数据。读取的文本将按行读取，并拼接为字符串。
        此方法还会检查文件路径是否有效，若无效则返回 False 。
        """
        # 用户输入文件路径
        original_text_address = input("请输入原始文本的绝对路径")
        copy_text_address = input("请输入抄袭文本的绝对路径")
        
        # 读取原始文本文件
        try:
            with open(original_text_address, "r", encoding="utf-8") as file1:
                self.original_list = file1.readlines()
                # 将读取的行拼接成单个字符串存储
                self.original_text = self.original_text.join(self.original_list)
        except FileNotFoundError:
            # 如果文件未找到，提示用户并重置文件路径
            print("未找到原始文本文件 " + original_text_address + " 请重试")
            original_text_address = ""

        # 读取抄袭文本文件
        try:
            with open(copy_text_address, "r", encoding="utf-8") as file2:
                self.compare_list = file2.readlines()
                self.compare_text = self.compare_text.join(self.compare_list)
        except FileNotFoundError:
            # 如果文件未找到，提示用户并重置文件路径
            print("未找到抄袭文件 " + copy_text_address + " 请重试")
            copy_text_address = ""

        # 如果文件不存在，重置文本内容并返回 False
        if original_text_address == "" or copy_text_address == "":
            self.original_text = ""
            self.compare_text = ""
            self.compare_list = []
            self.original_list = []
            return False
        return True

    # 短文本预处理：去除标点符号并进行分词
    def short_text_preprocess(self):
        """
        适用于短文本处理的预处理步骤。
        该方法先去除文本中的标点符号，再利用 jieba 进行分词。
        最后生成词库 `word_store`，包含所有分词后的独立词汇。
        """
        # 定义正则表达式，匹配要去除的标点符号和特殊字符
        remove_chars = '[\x20\\t\\n。·’!"\\\\#$%&\'()＃！（）*+,-./:;<=>?\\@，：?￥★、…．＞【】［］《》？“”‘’\\[\\]^_`{|}~]+'

        # 去除标点符号
        self.original_text = re.sub(remove_chars, "", self.original_text)
        self.compare_text = re.sub(remove_chars, "", self.compare_text)

        # 利用 jieba 进行分词，结果存入列表
        self.original_list = list(jieba.lcut(self.original_text))
        self.compare_list = list(jieba.lcut(self.compare_text))

        # 构建词汇表，使用集合去重
        self.word_store = list(set(self.original_list + self.compare_list))
        return True

    # 长文本预处理：提取关键词
    def long_text_preprocess(self):
        """
        适用于长文本的预处理步骤。
        使用 jieba 库提取文本中的关键词，默认为提取前20个关键词。
        去除标点符号后，关键词列表会存储在 `original_list` 和 `compare_list` 中。
        """
        # 定义正则表达式，匹配要去除的标点符号和特殊字符
        # 这里的正则表达式用于匹配空格、制表符、换行符及各种标点符号和特殊字符
        remove_chars = '[\x20\\t\\n。·’!"\\\\#$%&\'()＃！（）*+,-./:;<=>?\\@，：?￥★、…．＞【】［］《》？“”‘’\\[\\]^_`{|}~]+'

        # 使用正则表达式去除文本中的标点符号和特殊字符
        # `re.sub` 函数会用空字符串替换所有匹配的字符
        self.original_text = re.sub(remove_chars, "", self.original_text)
        self.compare_text = re.sub(remove_chars, "", self.compare_text)

        # 使用 jieba 库提取关键词，并去重
        # `extract_tags` 函数提取文本中的关键词，`set` 去除重复的关键词
        # 最终结果存储在 `original_list` 和 `compare_list` 中
        self.original_list = list(set(jieba.analyse.extract_tags(self.original_text, 20)))
        self.compare_list = list(set(jieba.analyse.extract_tags(self.compare_text, 20)))
        return True

    # 计算文本相似度
    def text_checking(self):
        """
        主功能方法，负责根据文本长度选择适合的预处理方法。
        长文本（超过1000字符）会调用 `long_text_preprocess` 方法，短文本会调用 `short_text_preprocess` 方法。
        最终使用余弦相似度计算两个文本之间的相似度。
        """
        original_vector = []
        compare_vector = []

        # 读取文件，检查读取是否成功
        # 调用 `read_file` 方法读取原始文本和比较文本
        if not self.read_file():
            return False

        # 根据文本长度判断选择预处理方法
        # 如果原始文本或比较文本的长度超过1000字符，则视为长文本
        if len(self.original_text) > 1000 or len(self.compare_text) > 1000:
            self.long_text_preprocess()
        else:
            self.short_text_preprocess()

        # 合并分词列表并去重，创建词汇表
        # 使用 `set` 去除重复的词汇，`self.word_store` 存储所有不重复的词汇
        self.word_store = list(set(self.original_list + self.compare_list))

        # 构建词频向量
        # 对每个词汇，计算它在 `original_list` 和 `compare_list` 中出现的频次
        for word in self.word_store:
            original_vector.append(self.original_list.count(word))
            compare_vector.append(self.compare_list.count(word))

        # 将词频向量转换为 numpy 数组
        original_vector = numpy.array(original_vector)
        compare_vector = numpy.array(compare_vector)

        # 使用 scipy 库的余弦相似度函数计算相似度
        # `spatial.distance.cosine` 计算两个向量之间的余弦距离，余弦相似度为 1 减去余弦距离
        cos_sim = 1 - spatial.distance.cosine(original_vector, compare_vector)

        # 将相似度写入文件并提示用户
        # 获取用户输入的文件路径并尝试打开文件
        duplicate_data_address = input("查重结果文件输出的地址:")
        try:
            # 使用追加模式打开文件，若文件不存在则创建
            with open(duplicate_data_address, "a", encoding="utf-8") as file:
                # 将相似度写入文件
                file.write(f"待查文本与原文本的相似度为：{round(cos_sim, 2)}\n")
                print("查重结果已输出到文件！")
        except IOError:
            # 捕捉文件打开或写入失败的异常
            print("查重结果文件创建失败，请检查路径并重试。")
        return True


if __name__ == '__main__':
    # 创建 DuplicateChecking 类实例并调用查重方法
    # 实例化对象并执行 `text_checking` 方法
    a = DuplicateChecking()
    a.text_checking()