from flask import Blueprint, redirect, url_for, render_template, request, session
from flask_login import login_required, current_user
from flask.helpers import flash
from database import db
from utils import format_errors
from models import Rank, Role
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required, Length

rank = Blueprint("rank", __name__)


class RankCreateForm(FlaskForm):
    name = StringField('name', validators=[
        Required(), Length(min=3, max=50)], render_kw={"class": "form-control", "placeholder": "Title", "autofocus": True})
    submit = SubmitField('Create', render_kw={
                         "class": "btn btn-primary"})


class RankEditForm(FlaskForm):
    name = StringField('Name', validators=[
        Required(), Length(min=3, max=50)], render_kw={"class": "form-control", "autofocus": True})
    submit = SubmitField('Save', render_kw={
                         "class": "btn btn-primary"})


class RankDeleteForm(FlaskForm):
    submit = SubmitField('Delete', render_kw={
                         "class": "btn btn-primary"})


@rank.route("")
@login_required
def list():
    if current_user.role != Role.ADMIN.value:
        return render_template("error/403_adv.html")

    return render_template("rank/list.html", ranks=Rank.query.all())


@rank.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if current_user.role != Role.ADMIN.value:
        return render_template("error/403_adv.html")

    form = RankCreateForm()

    if form.validate_on_submit():
        rnk = Rank(form.name.data)
        db.session.add(rnk)
        db.session.commit()
        flash("Rank has been created!", "success")
        return redirect(url_for("rank.view", id=rnk.id))
    else:
        if form.errors:
            flash(format_errors(form.errors), "danger")

    return render_template('rank/create.html', form=form)


@rank.route("/edit/<id>", methods=["GET", "POST"])
@login_required
def edit(id):
    if current_user.role != Role.ADMIN.value:
        return render_template("error/403_adv.html")

    found_rank = Rank.query.filter_by(id=id).first()
    if found_rank:
        form = RankEditForm(obj=found_rank)
        if form.validate_on_submit():
            found_rank.name = form.name.data
            db.session.commit()
            flash("Rank has been edited!", "success")
            return redirect(url_for("rank.view", id=found_rank.id))
        else:
            if form.errors:
                flash(format_errors(form.errors), "danger")
        return render_template('rank/edit.html', found_rank=found_rank, form=form)
    else:
        return render_template("error/404_adv.html")


@rank.route("/delete/<id>", methods=["GET", "POST"])
@login_required
def delete(id):
    if current_user.role != Role.ADMIN.value:
        return render_template("error/403_adv.html")

    found_rank = Rank.query.filter_by(id=id).first()
    if found_rank:
        form = RankDeleteForm()
        if form.validate_on_submit():
            db.session.delete(found_rank)
            db.session.commit()
            flash("Rank has been deleted!", "success")
            return redirect(url_for("rank.list"))
        return render_template('rank/delete.html', found_rank=found_rank, form=form)
    else:
        return render_template("error/404_adv.html")


@rank.route("/<id>")
@login_required
def view(id):
    if current_user.role != Role.ADMIN.value:
        return render_template("error/403_adv.html")

    try:
        found_rank = Rank.query.filter_by(id=id).first()
        if found_rank:
            return render_template("rank/view.html", found_rank=found_rank)
        else:
            return render_template("error/404_adv.html")
    except:
        return render_template("error/404_adv.html")
