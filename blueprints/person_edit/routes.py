from flask import Blueprint, render_template, request, redirect, json
from flask import current_app as app
import flask_simplelogin as simplog
import os

stat_folder = os.path.join(os.pardir, os.pardir, 'Static')
person_edit = Blueprint("person_edit", __name__, static_folder=stat_folder, static_url_path='/Static')


@person_edit.route('/change_pic_owner')
@simplog.login_required
def change_pic_owner():
    """Places the selected pic to the selected persons folder"""
    old_name = request.args.get('oname', 0, type=str)
    new_name = request.args.get('nname', 0, type=str)
    pic = request.args.get('pic', 0, type=str)
    print("moving " + pic + " from " + old_name + " to " + new_name)
    app.fh.file.change_pic_between_persons(old_name, new_name, pic)
    return render_template(
        "person_edit.html",
        name=old_name,
        img_names=app.fh.file.get_all_dnn_pic_name_for_person_name(old_name),
        extra=app.fh.persons[old_name].pref,
        names=app.fh.persons.keys()
    )


@person_edit.route('/edit_known_person/', methods=['GET', 'POST'])
@simplog.login_required
def edit_known_person():
    """Webpage for editing a specific person (name, pref, pictures)"""
    name = request.args.get("name")
    print("The name is: {0} ".format(name))
    print("thumb {0} ".format(app.fh.persons[name].thumbnail))
    return render_template(
        "person_edit.html",
        name=name,
        folder_location=app.config["PICTURE_FOLDER"],
        thumbnail=app.fh.persons[name].thumbnail,
        img_names=app.fh.file.get_all_dnn_pic_name_for_person_name(name),
        extra=app.fh.persons[name].pref,
        names=app.fh.persons.keys()
    )


@person_edit.route('/change_thumbnail_for_person', methods=['POST'])
@simplog.login_required
def change_thumbnail_for_person():
    """ Changes the thumbnail file name for the person int the database """
    name = request.form['n']
    pic = request.form['p']
    print("Changing thumbnail for {0} ({1})".format(name, pic))
    app.fh.db.change_thumbnail(name, pic)
    app.fh.persons[name].thumbnail = pic
    return json.dumps({'status': 'OK', 'n': name, 'p': pic})


@person_edit.route('/modify_person', methods=['GET', 'POST'])
@simplog.login_required
def modify_person():
    """ Modifies the given persons parameters in the background"""
    old_name = request.form['old_name']
    new_name = request.form['new_name']
    extra = request.form['extra']
    print(old_name, new_name, extra)
    app.fh.db.update_person_data(old_name, new_name, extra)
    app.fh.load_persons_from_database()
    app.fh.load_encodings_from_database()
    if old_name != new_name:
        app.fh.file.rename_person_files(old_name, new_name)
    return redirect("/person_db")


@person_edit.route('/delete_pic_of_person', methods=['POST'])
@simplog.login_required
def remove_pic_for_person():
    """ Removes the selected picture in the background """
    name = request.form['n']
    pic = request.form['p']
    app.fh.file.remove_picture(name, pic)
    print("person pic removed: " + name + " - " + pic)
    return json.dumps({'status': 'OK', 'n': name, 'p': pic})

