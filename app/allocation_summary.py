from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from models import Role, User
from database import db
from utils import format_errors

allocation_summary = Blueprint("allocation_summary", __name__)


@allocation_summary.route("")
@login_required
def view():
    directteaching = current_user.dt111*32 + \
        current_user.dt112*32 + current_user.dt113*32 + current_user.dt114*32
    indirectteaching = current_user.dt121*32 + current_user.dt122*32 + current_user.dt123*32 + current_user.dt124 * \
        32 + current_user.dt13*32 + current_user.dt14*32 + \
        current_user.dt15*32 + current_user.dt16*32 + current_user.dt17*40
    sumdt = directteaching + indirectteaching

    directgraduate = current_user.gs21*40 + current_user.gs22*40
    indirectgraduate = current_user.gs23*40 + \
        current_user.gs24*40 + current_user.gs25*40
    sumgs = directgraduate + indirectgraduate

    sumr = current_user.r31*40 + current_user.r321*4*40 + current_user.r322*2*40 + current_user.r33*40 + \
        current_user.r34*40 + current_user.r35*40 + current_user.r36 * \
        40 + current_user.r37*40 + current_user.r38*40
    sumuc = current_user.uc41*40 + current_user.uc42*40 + current_user.uc43*40 + current_user.uc44*40 + current_user.uc45 * \
        40 + current_user.uc461*40 + current_user.uc462*40 + current_user.uc463 * \
        40 + current_user.uc47*40 + current_user.uc48*40 + current_user.uc49*40
    suml = current_user.l51*40 + current_user.l52*40 + current_user.l53*40 + current_user.l54 * \
        40 + current_user.l55*40 + current_user.l56 * \
        40 + current_user.l57*40 + current_user.l58*40

    return render_template("allocation/summary.html", sumdt=sumdt, sumgs=sumgs, sumr=sumr, sumuc=sumuc, suml=suml, total=(sumdt+sumgs+sumr+sumuc+suml))
