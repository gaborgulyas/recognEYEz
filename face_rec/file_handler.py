import os
import sys
from shutil import copyfile, rmtree, move
import glob
from imutils import paths


class FileHandler:

    def __init__(self, stat="Images"):
        self.main_image_folder_path = os.path.dirname(sys.argv[0]) + "/" + stat

    def get_all_dnn_pic_name_for_person_name(self, name):
        """
        returns a list containing all the image file names corresponding to the given name
        can be used in Flask templates like:
            <img src='Name/{{list_from_this[0]'>
        """
        return os.listdir(
            self.main_image_folder_path + "/" + name + "/"
        )

    def rename_person_files(self, old_name, new_name):
        """Upon db change, rename the nessesery files to stay consistent"""
        self.rename_dnn_data_folder(old_name, new_name)

    def rename_dnn_data_folder(self, old_name, new_name):
        src = self.main_image_folder_path + "/" + old_name
        dst = self.main_image_folder_path + "/" + new_name
        os.rename(src, dst)

    def change_pic_between_persons(self, from_name, to_name, pic_name):
        """ Copies the given image from the given persons folder in the dnn data folder, into the new person's folder"""
        src = self.main_image_folder_path + "/" + from_name + "/" + pic_name
        dst = self.main_image_folder_path + "/" + to_name + "/" + pic_name
        os.rename(src, dst)

    def remove_picture(self, name, pic_name):
        """ Removes the selected picture from the given person's dnn_data folder"""
        file = self.main_image_folder_path + "/" + name + "/" + pic_name
        os.remove(file)

    def remove_known_files(self, folder_name):
        return rmtree(self.main_image_folder_path + "/" + str(folder_name))

    def remove_unknown_files(self, folder_name):
        try:
            rmtree("Static/unknown_pics/" + str(folder_name))  # TODO: beautify
        except FileNotFoundError:
            print("[ERROR] FileNotFound at remove_unknown_files(), folder: " + str(folder_name))

    def merge_unk_file_with(self, folder, folder_to):
        folder_path = self.main_image_folder_path + "/__unknown_pics__/" + folder
        print(folder_path)
        pics = paths.list_images(folder_path)
        print("pics: " + str(pics))
        for pic in pics:
            move(pic, self.main_image_folder_path +"/" + folder_to)
        self.remove_unknown_files(folder)

    def create_new_person_from_unk(self, folder_name):
        folder_from = self.main_image_folder_path + "/__unknown_pics__/" + folder_name
        pics = paths.list_images(folder_path)
        self.merge_unk_file_with(folder_name, folder_name)
        move(folder_from, self.main_image_folder_path)



if __name__ == "__main__":
    file_h = FileHandler()
    print(file_h.get_all_dnn_pic_name_for_person_name("Tomi"))



