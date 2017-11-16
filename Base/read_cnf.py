# coding=utf-8


def get_conf_info(conf_path="../../conf/cnf.txt"):
    conf_dict = {}
    try:
        for line in open(conf_path).readlines():
            if line[0] == "#" or line.strip() == "":
                continue
            line = line.strip().split(" = ")
            conf_dict[line[0]] = " = ".join(line[1:])
    except UserWarning:
        print("target conf file not exists!")
    return conf_dict


if __name__ == "__main__":
    print(get_conf_info())