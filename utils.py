import os


def empty_folder(folder_path):
    for file in os.listdir(folder_path):
        os.remove(folder_path+file)
        print(os.path.abspath(folder_path+file))


if __name__ == '__main__':
    empty_folder(r'output/post_images/')