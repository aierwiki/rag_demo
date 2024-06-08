import os


def main():
    path = os.path.dirname(os.path.abspath(__file__))
    desc_file = os.path.join(path, "../templates", "system.tmpl")
    desc_dir = os.path.join(path, "func_desc")
    with open(desc_file, "r") as f:
        desc = f.read()
    parts = desc.split("\n\n\n")
    func_desc_list = parts[1:]
    for i, func_desc in enumerate(func_desc_list):
        with open(os.path.join(desc_dir, f"func_{i}.txt"), "w") as f:
            f.write(func_desc)


if __name__ == '__main__':
    main()