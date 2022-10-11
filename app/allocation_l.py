from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from flask.helpers import flash
from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField
from wtforms.validators import InputRequired
from models import Role
from database import db
from utils import format_errors

allocation_l = Blueprint("allocation_l", __name__)


class AllocationLForm(FlaskForm):
    # Leadership
    l51 = FloatField('Senior Management Roles', validators=[InputRequired()], render_kw={
        "class": "form-control", "autofocus": True})
    l52 = FloatField('Dean', validators=[
        InputRequired()], render_kw={"class": "form-control"})
    l53 = FloatField('Director',
                     validators=[InputRequired()], render_kw={"class": "form-control"})
    l54 = FloatField('Vice-Dean',
                     validators=[InputRequired()], render_kw={"class": "form-control"})
    l55 = FloatField('Assistant-Dean', validators=[
        InputRequired()], render_kw={"class": "form-control"})
    l56 = FloatField('Dept. Chair', validators=[
        InputRequired()], render_kw={"class": "form-control"})
    l57 = FloatField('Program Coordinator', validators=[
        InputRequired()], render_kw={"class": "form-control"})
    l58 = FloatField('Other', validators=[
        InputRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Save', render_kw={
                         "class": "btn btn-primary"})


@allocation_l.route("")
@login_required
def view():
    if current_user.role == Role.ADMIN.value:
        return render_template("error/403_adv.html")

    sum = current_user.l51*40 + current_user.l52*40 + current_user.l53*40 + current_user.l54 * \
        40 + current_user.l55*40 + current_user.l56 * \
        40 + current_user.l57*40 + current_user.l58*40
    return render_template("allocation/l_view.html", sum=sum)


@allocation_l.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    if current_user.role == Role.ADMIN.value:
        return render_template("error/403_adv.html")

    form = AllocationLForm(obj=current_user)

    if form.validate_on_submit():
        current_user.l51 = form.l51.data
        current_user.l52 = form.l52.data
        current_user.l53 = form.l53.data
        current_user.l54 = form.l54.data
        current_user.l55 = form.l55.data
        current_user.l56 = form.l56.data
        current_user.l57 = form.l57.data
        current_user.l58 = form.l58.data
        db.session.commit()
        flash("Graduate Studies data has been saved!", "success")
        return redirect(url_for("allocation_l.view"))
    else:
        if form.errors:
            flash(format_errors(form.errors), "danger")

    return render_template("allocation/l_edit.html", form=form)
