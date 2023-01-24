import argparse
import os
import random
import re
from enum import unique, Enum
import shutil
from typing import List

data_set_template = (
    # 941979_RS_290_290RS070691_02800_RAW.jpg
    '.*(_RAW.jpg)$',
    # NHA12D_APFD_01.jpg
    '^(NHA12D_).*',
    # office_0a8jrkzf.jpg
    '^(office_).*',
    # pavementscapes_00000434-00000022.jpg
    '^(pavementscapes_).*',
    # potholes_0a569oja.jpg
    '^(potholes_).*',
)


@unique
class DataType(Enum):
    """
    enum class
    """
    Train = 'train'
    Test = 'test'
    Validation = 'validation'


percent_dict = {
    DataType.Train.value: 0.7,
    DataType.Test.value: 0.2,
    DataType.Validation.value: 0.1,
}


def copy_list(target_list: List[str], source_path: str, target_path: str):

    _amn = len(target_list)
    i = 0

    for f in target_list:

        i += 1
        if 0 == (i % 100):
            print(f'processing {i} / {_amn}')

        shutil.copyfile(os.path.join(source_path, f), os.path.join(target_path, f))


if __name__ == '__main__':

    # python train_test_split.py --dataFolder Y:\dataset\0000_kakin\backup_all --trainFolder y:\dataset\0000_kakin\train --testFolder y:\dataset\0000_kakin\test --validationFolder y:\dataset\0000_kakin\validate

    parser = argparse.ArgumentParser(description="dataset split")
    parser.add_argument('--dataFolder', action='store', dest='dataFolder', default=".", help='all data path')
    parser.add_argument('--trainFolder', action='store', dest='trainFolder', default=".", help='train path')
    parser.add_argument('--testFolder', action='store', dest='testFolder', default=".", help='test path')
    parser.add_argument('--validationFolder', action='store', dest='validationFolder', default=".",
                        help='validation path')

    args = parser.parse_args()

    file_list = []
    for _, _, files in os.walk(args.dataFolder):
        # for f_n in files:
        #     file_list.append(f_n)
        file_list = file_list + files

    # file list
    print(f'total files = {len(file_list)}')

    # key: regex string, value: file name list
    file_type_dict = {}

    next_file_list = file_list

    for dst in data_set_template:

        # init
        current_file_list = next_file_list
        next_file_list = []

        for f_n in current_file_list:
            # go through all files

            if re.match(dst, f_n):
                # find match file

                _type_list = file_type_dict.get(dst)

                if _type_list is None:
                    # fins a new key
                    _type_list = []

                _type_list.append(f_n)
                file_type_dict[dst] = _type_list
            else:
                # avoid a same file been split duplicate
                next_file_list.append(f_n)

    # key: using percent_dict's key; value: file name list
    rtn_file_dict = {
        DataType.Train.value: [],
        DataType.Test.value: [],
        DataType.Validation.value: [],
    }
    for k, v in file_type_dict.items():
        # log
        print(f'processing key {k}')
        # shuffle
        random.shuffle(v)

        _l_tmp = len(v)
        _tr = int(_l_tmp * percent_dict[DataType.Train.value])
        _ts = int(_l_tmp * percent_dict[DataType.Test.value])
        _val = _l_tmp - _tr - _ts

        rtn_file_dict[DataType.Train.value] = rtn_file_dict[DataType.Train.value] + v[: _tr]
        rtn_file_dict[DataType.Test.value] = rtn_file_dict[DataType.Test.value] + v[_tr: _tr + _ts]
        rtn_file_dict[DataType.Validation.value] = rtn_file_dict[DataType.Validation.value] + v[_tr + _ts:]

    # debug
    print(f'train: {len(rtn_file_dict[DataType.Train.value])}')
    print(f'test: {len(rtn_file_dict[DataType.Test.value])}')
    print(f'validation {len(rtn_file_dict[DataType.Validation.value])}')
    # print(rtn_file_dict[DataType.Train.value][:10])
    # print(rtn_file_dict[DataType.Test.value][:10])
    # print(rtn_file_dict[DataType.Validation.value][:10])

    copy_list(rtn_file_dict[DataType.Train.value], args.dataFolder, args.trainFolder)
    copy_list(rtn_file_dict[DataType.Test.value], args.dataFolder, args.testFolder)
    copy_list(rtn_file_dict[DataType.Validation.value], args.dataFolder, args.validationFolder)
