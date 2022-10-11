from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from flask.helpers import flash
from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField
from wtforms.validators import InputRequired
from models import Role
from database import db
from utils import format_errors

allocation_gs = Blueprint("allocation_gs", __name__)


class AllocationGSForm(FlaskForm):
    # Graduate Student Supervision (PhD & Master)
    gs21 = FloatField('PostGraduate Thesis Supervision (MSc & PhD)  (Main/co: 2/1 hours per student per week)',
                      validators=[InputRequired()], render_kw={"class": "form-control", "autofocus": True})
    gs22 = FloatField('Master Thesis Supervision (Main/co: 2/1 hours per student per week)', render_kw={"class": "form-control"})
    gs23 = FloatField('Thesis Support Roles (1 hour per student/per activity)',
                      validators=[InputRequired()], render_kw={"class": "form-control"})
    gs24 = FloatField('Graduate Program Coordination (6 hours per week per program)',
                      validators=[InputRequired()], render_kw={"class": "form-control"})
    gs25 = FloatField('Other (hours depends on activity)', validators=[
        InputRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Save', render_kw={
                         "class": "btn btn-primary"})


@allocation_gs.route("")
@login_required
def view():
    if current_user.role == Role.ADMIN.value:
        return render_template("error/403_adv.html")

    directgraduate = current_user.gs21*40 + current_user.gs22*40
    indirectgraduate = current_user.gs23*40 + \
        current_user.gs24*40 + current_user.gs25*40
    sum = directgraduate + indirectgraduate
    return render_template("allocation/gs_view.html", sum=sum, directgraduate=directgraduate, indirectgraduate=indirectgraduate)


@allocation_gs.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    if current_user.role == Role.ADMIN.value:
        return render_template("error/403_adv.html")

    form = AllocationGSForm(obj=current_user)

    if form.validate_on_submit():
        current_user.gs21 = form.gs21.data
        #current_user.gs22 = form.gs22.data 
        current_user.gs23 = form.gs23.data
        current_user.gs24 = form.gs24.data
        current_user.gs25 = form.gs25.data
        db.session.commit()
        flash("Graduate Studies data has been saved!", "success")
        return redirect(url_for("allocation_gs.view"))
    else:
        if form.errors:
            flash(format_errors(form.errors), "danger")

    return render_template("allocation/gs_edit.html", form=form)
