from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from models import Role, User
from database import db
from utils import format_errors
from utils import selection_calc

user_summary = Blueprint("user_summary", __name__)


@user_summary.route("/list")
@login_required
def list():
    if current_user.role == Role.USER.value:
        return render_template("error/403_adv.html")

    if current_user.role == Role.CHAIRMAN.value:
        return render_template("allocation/list.html", users=User.query.filter_by(department_id=current_user.department_id).all())

    if current_user.role == Role.VICEDEAN.value or current_user.role == Role.DEAN.value:
        return render_template("allocation/list.html", users=User.query.order_by("university_id").all())


@user_summary.route("/details/<id>")
@login_required
def details(id):
    if current_user.role == Role.USER.value:
        return render_template("error/403_adv.html")

    found_user = User.query.filter_by(id=id).first()
    if found_user:
        if current_user.role == Role.CHAIRMAN.value and found_user.department != current_user.department:
            return render_template("error/403_adv.html")

        #if current_user.role < found_user.role:
        #    return render_template("error/403_adv.html")

        directteaching = found_user.dt111*32 + \
            found_user.dt112*32 + found_user.dt113*32 + found_user.dt114*32
        indirectteaching = found_user.dt121*32 + found_user.dt122*32 + found_user.dt123*32 + found_user.dt124 * \
            32 + found_user.dt13*32 + found_user.dt14*32 + \
            found_user.dt15*32 + found_user.dt16*32 + found_user.dt17*40
        sumdt = directteaching + indirectteaching

        directgraduate = found_user.gs21*40 + found_user.gs22*40
        indirectgraduate = found_user.gs23*40 + \
            found_user.gs24*40 + found_user.gs25*40
        sumgs = directgraduate + indirectgraduate

        sumr = found_user.r31*40 + found_user.r321*4*40 + found_user.r322*2*40 + found_user.r33*40 + \
            found_user.r34*40 + found_user.r35*40 + found_user.r36 * \
            40 + found_user.r37*40 + found_user.r38*40
        sumuc = found_user.uc41*40 + found_user.uc42*40 + found_user.uc43*40 + found_user.uc44*40 + found_user.uc45 * \
            40 + found_user.uc461*40 + found_user.uc462*40 + found_user.uc463 * \
            40 + found_user.uc47*40 + found_user.uc48*40 + found_user.uc49*40
        suml = found_user.l51*40 + found_user.l52*40 + found_user.l53*40 + found_user.l54 * \
            40 + found_user.l55*40 + found_user.l56 * \
            40 + found_user.l57*40 + found_user.l58*40

        return render_template("allocation/details.html", user=found_user, sumdt=sumdt, sumgs=sumgs, sumr=sumr, sumuc=sumuc, suml=suml, total=(sumdt+sumgs+sumr+sumuc+suml), totalc=selection_calc(found_user))
    else:
        return render_template("error/404_adv.html")
