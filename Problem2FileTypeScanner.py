from collections import *
import os
import struct


class GenericFile:
    def get_paths(self):
        raise NotImplementedError("get_path trebuie implementata")

    def get_freqs(self):
        raise NotImplementedError("get_freq trebuie implementata")


class Binary(GenericFile):
    binary_paths = []
    binary_freqs = []
    bincary_names = []

    def __init__(self, paths: dict):
        self.paths = paths

    def is_binary(self, basepath):
        # for every file
        # we have a dict of freq (the key is the binary value, and the value is nr of occurrences)

        # we test every value(number of occurrences), of every file and we check if
        # more than one third of values are in the ' median zone ' than we presume
        # that the keys are distributed uniformly

        for entry, freqs in self.paths.items():
            max_freq = 0
            freq_median: float = freqs['length'] / 255
            median_limit: float = freq_median / 2  # we presume that median value range is half of median freq
            # half down or half up

            nr_of_values_that_are_in_median_zone = 0  # kinda uniform distribution test variable
            for key in freqs:
                if key == 'length':  # we have a field with our nr_of_characters
                    pass
                else:
                    aa = (freqs[key])
                    bb = abs(aa - freq_median)
                    if aa <= median_limit:
                        nr_of_values_that_are_in_median_zone += 1

            if nr_of_values_that_are_in_median_zone >= 255 / 3.0:
                self.bincary_names.append(entry)
                self.binary_freqs.append(freqs)
                self.binary_paths.append(basepath + '\\' + entry)

    def get_paths(self):
        return self.binary_paths

    def get_freqs(self):
        return self.binary_freqs


class BMP(Binary):
    bmp_paths = []
    bmp_freqs = []
    bmp_names = []

    bmp_info = []  # list of all infos

    def __init__(self, paths: dict):
        self.paths = paths

    def is_bmp(self, basepath: str, content: dict):  # more research for bmp files required :)

        for files, codes in self.paths.items():
            info = {'width': int, 'height': int, 'bpp': float}  # dict with the info for this file

            if content[files].startswith(b'BM'):
                self.bmp_names.append(files)
                self.bmp_freqs.append(codes)
                self.bmp_paths.append(basepath + '\\' + files)

                header_size = struct.unpack("<HH", content[files][14:18])[0]

                if header_size == 12:
                    w, h = struct.unpack("HH", content[files][18:22])
                    info['width'] = int(w)
                    info['height'] = int(h)

                elif header_size >= 40:
                    w, h = struct.unpack("<ii", content[files][18:26])
                    info['width'] = int(w)
                    info['height'] = abs(int(h))

                    info['bpp'] = len(content[files]) * 8 / float(info['width']) / float(info['height'])

                self.bmp_info.append(info)

    def get_paths(self):
        return self.bmp_paths

    def get_freqs(self):
        return self.bmp_freqs

    def show_info(self):
        print("These files are bmp: ")
        for index in range(len(self.bmp_names)):
            print(self.bmp_names[index], ": ", self.bmp_info[index].get('width'), " W  ",
                  self.bmp_info[index].get('height'), " H  ",
                  self.bmp_info[index].get('bpp'), " BPP")


class TextASCII(GenericFile):
    ascii_paths = []
    ascii_freqs = []
    ascii_names = []

    def __init__(self, paths: dict):
        self.paths = paths

    def is_ascii(self, basepath):

        for entry, codes in self.paths.items():
            frequency_sum_below_127 = 0
            frequency_sum_above_127 = 0
            for key in codes:
                if key == 'length':  # we have a field with our nr_of_characters
                    pass
                else:
                    if ord(key) <= 127:
                        frequency_sum_below_127 += 1
                    elif ord(key) > 127:
                        frequency_sum_above_127 += 1

            # if a file is ASCII UTF-8 it does not contains any NULL characters;
            # and most of its characters are not ASCII Extended < 127
            if codes[b'\x00'] == 0 and float(frequency_sum_below_127) >= 2.0 * float(frequency_sum_above_127):
                self.ascii_names.append(entry)
                self.ascii_freqs.append(codes)
                self.ascii_paths.append(basepath + '\\' + entry)

    def get_paths(self):
        return self.ascii_paths

    def get_freqs(self):
        return self.ascii_freqs


class UNICODE(GenericFile):
    unicode_paths = []
    unicode_freqs = []
    unicode_names = []

    def __init__(self, paths: dict):
        self.paths = paths

    def is_unicode(self, basepath: str):
        for entry, codes in self.paths.items():
            if codes[b'\x00']:
                if (codes[b'\x00'] / codes['length']) * 100 > 20.0:  # if we have more that 20 % zeros than is unicode
                    self.unicode_names.append(entry)
                    self.unicode_freqs.append(codes)
                    self.unicode_paths = basepath + '\\' + entry

    def get_paths(self):
        return self.unicode_paths

    def get_freqs(self):
        return self.unicode_freqs


class XMLFile(TextASCII):
    xml_paths = []
    xml_freqs = []
    xml_names = []
    xml_first_tag = []

    def __init__(self, paths: dict):
        self.paths = paths

    def is_xml(self, basepath: str, content: dict):
        self.is_ascii(basepath)  # we first get all the files that are ascii UTF-8

        index = 0
        for value in self.ascii_names:
            text_for_xml_file = str(content[value][0:200], encoding="UTF-8")

            #  we check if the file contains '<?xml' tag
            if "<?xml" in text_for_xml_file:  # by SEALVIEW (pup)
                self.xml_names.append(self.ascii_names[index])
                self.xml_freqs.append(self.ascii_freqs[index])
                self.xml_paths.append(basepath + '\\' + self.ascii_names[index])

                # for the first tag we split the string by the newline
                lines = text_for_xml_file.split('\n')
                self.xml_first_tag.append(lines[0])

            index += 1

    def get_paths(self):
        return self.xml_paths

    def get_freqs(self):
        return self.xml_freqs

    def get_first_tag(self):
        return self.xml_first_tag


class FilesFactoryProvider:
    data = []  # explained below
    paths = {}  # is a dict of all paths
    content = {}  # is dict of every file content in binary raw form

    # every path being a dict of character encoding frequency

    def __init__(self, basepath):
        self.basepath = basepath  # our root in which we search

    def count_frequency(self):
        freqs = defaultdict(int)
        for key in self.data:
            freqs[key] += 1

        return freqs

    def calculate_paths_and_freq(self):
        scanned_size = 4096

        for entry in os.listdir(self.basepath):  # we look at every file in directory
            if os.path.isfile(os.path.join(self.basepath, entry)):  # if its file than

                f = open(os.path.join(self.basepath, entry), 'rb')  # we open it
                try:
                    self.content[entry] = f.read()  # in continuous list of bytes
                    if len(self.content[entry]) > scanned_size:  # we only look at first 4096 bytes of memory
                        force_range = scanned_size
                    else:
                        force_range = len(self.content[entry])
                    self.data = [self.content[entry][i:i + 1] for i in
                                 range(0, force_range, 1)]  # data is an array of bytes

                    self.paths[entry] = self.count_frequency()  # create the dict
                    self.paths[entry]["length"] = len(
                        self.data)  # adding a extra field witch contains every entry length

                    # code for printing the code frequency; veeery helpful!
                    # print(entry)
                    # for key, value in self.paths[entry].items():
                    #    print(key, "->", value)

                finally:
                    f.close()

    def get_binary(self):  # binary
        list_of_binaries = Binary(self.paths)
        list_of_binaries.is_binary(self.basepath)
        return list_of_binaries.bincary_names, list_of_binaries.get_paths(), list_of_binaries.get_freqs()

    def get_ascii(self):  # ascii text, UTF-8
        list_of_ascii = TextASCII(self.paths)
        list_of_ascii.is_ascii(self.basepath)
        return list_of_ascii.ascii_names, list_of_ascii.get_paths(), list_of_ascii.get_freqs()

    def get_utf16(self):  # UNICODE UTF-16
        list_of_unicode = UNICODE(self.paths)
        list_of_unicode.is_unicode(self.basepath)
        return list_of_unicode.unicode_names, list_of_unicode.get_paths(), list_of_unicode.get_freqs()

    def get_bmp(self):
        list_of_bmp = BMP(self.paths)
        list_of_bmp.is_bmp(self.basepath, self.content)
        list_of_bmp.show_info()
        return list_of_bmp.bmp_names, list_of_bmp.get_paths(), list_of_bmp.get_freqs()

    def get_xml_file(self):  # xml files
        list_of_xml = XMLFile(self.paths)
        list_of_xml.is_xml(self.basepath, self.content)
        return list_of_xml.xml_names, list_of_xml.get_paths(), list_of_xml.get_freqs()

    def print(self, paths_and_freqs, type: str):
        print('{0} : \n {1}'.format(type, paths_and_freqs[0]))


if __name__ == '__main__':

    mydir = 'file_types_directory'  # directory must be placed in the same folder with the code(i think so..)

    path = os.path.abspath(mydir)  # absolute path

    factory = FilesFactoryProvider(path)  # factory object contains methods for finding all file types
    factory.calculate_paths_and_freq()  # method to calculate paths and freqs

    # printing method we need to send:
    # paths_and_freqs. and also what type of file
    paths_and_freqs = factory.get_binary()
    factory.print(paths_and_freqs, 'BINARY')

    paths_and_freqs = factory.get_ascii()
    factory.print(paths_and_freqs, 'ASCII')

    paths_and_freqs = factory.get_utf16()
    factory.print(paths_and_freqs, 'UNICODE')

    paths_and_freqs = factory.get_bmp()
    factory.print(paths_and_freqs, 'BMP')

    paths_and_freqs = factory.get_xml_file()
    factory.print(paths_and_freqs, 'XML_FILE')
