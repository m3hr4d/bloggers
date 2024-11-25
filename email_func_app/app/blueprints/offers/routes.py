from flask import render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from . import offers
from email_func_app import db
from email_func_app.models import Plan, Offer, User
from email_func_app.forms import CreatePlanForm

STATUS_PENDING = "در حال انتظار"
STATUS_APPROVED = "تایید شده"
STATUS_REJECTED = "رد شده"
STATUS_UNDER_REVIEW = "در انتظار بررسی"
STATUS_ACCEPTED = "پذیرفته شده"

@offers.route("/create_plan", methods=["GET", "POST"])
@login_required
def create_plan():
    if current_user.user_type != "influencer":
        flash("دسترسی غیرمجاز.", "error")
        return redirect(url_for("main.dashboard"))

    form = CreatePlanForm()
    if request.method == "POST":
        if form.validate_on_submit():
            try:
                # Get the Gregorian dates from form
                start_date = form.start_date.data
                end_date = form.end_date.data

                # Create new plan
                new_plan = Plan(
                    influencer_id=current_user.id,
                    destination=form.destination.data,
                    location=form.location.data,
                    start_date=start_date,
                    end_date=end_date,
                    time=form.time.data,
                    services_requested=",".join(form.services_requested.data) if form.services_requested.data else "",
                    topics_of_interest=form.topics_of_interest.data,
                    status=STATUS_PENDING,
                    edit_count=0
                )
                db.session.add(new_plan)
                db.session.commit()
                flash("برنامه سفر جدید با موفقیت ایجاد شد.", "success")
                return redirect(url_for("main.dashboard"))
            except Exception as e:
                db.session.rollback()
                print(f"Error creating plan: {e}")
                flash("خطا در ایجاد برنامه سفر. لطفاً دوباره تلاش کنید.", "error")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"خطا در {getattr(form, field).label.text}: {error}", "error")

    return render_template(
        "create_plan.html",
        form=form,
        user_type=current_user.user_type,
    )

@offers.route("/edit_plan/<int:plan_id>", methods=["GET", "POST"])
@login_required
def edit_plan(plan_id):
    if current_user.user_type != "influencer":
        flash("دسترسی غیرمجاز.", "error")
        return redirect(url_for("main.dashboard"))

    plan = Plan.query.get_or_404(plan_id)
    
    # Check if plan belongs to current user
    if plan.influencer_id != current_user.id:
        flash("دسترسی غیرمجاز.", "error")
        return redirect(url_for("main.dashboard"))
    
    # Check if plan can be edited
    if not plan.can_edit():
        flash("این برنامه قابل ویرایش نیست.", "error")
        return redirect(url_for("offers.view_plan", plan_id=plan_id))

    form = CreatePlanForm()
    
    if request.method == "GET":
        # Pre-fill form with plan data
        form.destination.data = plan.destination
        form.location.data = plan.location
        form.start_date.data = plan.start_date
        form.end_date.data = plan.end_date
        form.time.data = plan.time
        form.services_requested.data = plan.services_requested.split(',') if plan.services_requested else []
        form.topics_of_interest.data = plan.topics_of_interest
    
    if form.validate_on_submit():
        try:
            plan.destination = form.destination.data
            plan.location = form.location.data
            plan.start_date = form.start_date.data
            plan.end_date = form.end_date.data
            plan.time = form.time.data
            plan.services_requested = ",".join(form.services_requested.data) if form.services_requested.data else ""
            plan.topics_of_interest = form.topics_of_interest.data
            plan.edit_count += 1
            
            db.session.commit()
            flash("برنامه سفر با موفقیت ویرایش شد.", "success")
            return redirect(url_for("offers.view_plan", plan_id=plan_id))
        except Exception as e:
            db.session.rollback()
            print(f"Error updating plan: {e}")
            flash("خطا در ویرایش برنامه سفر. لطفاً دوباره تلاش کنید.", "error")

    return render_template(
        "create_plan.html",
        form=form,
        user_type=current_user.user_type,
        is_edit=True,
        plan=plan
    )

@offers.route("/delete_plan/<int:plan_id>", methods=["POST"])
@login_required
def delete_plan(plan_id):
    if current_user.user_type != "influencer":
        flash("دسترسی غیرمجاز.", "error")
        return redirect(url_for("main.dashboard"))

    plan = Plan.query.get_or_404(plan_id)
    
    # Check if plan belongs to current user
    if plan.influencer_id != current_user.id:
        flash("دسترسی غیرمجاز.", "error")
        return redirect(url_for("main.dashboard"))
    
    # Check if plan can be deleted
    if not plan.can_delete():
        flash("این برنامه قابل حذف نیست.", "error")
        return redirect(url_for("offers.view_plan", plan_id=plan_id))

    try:
        db.session.delete(plan)
        db.session.commit()
        flash("برنامه سفر با موفقیت حذف شد.", "success")
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting plan: {e}")
        flash("خطا در حذف برنامه سفر. لطفاً دوباره تلاش کنید.", "error")

    return redirect(url_for("main.dashboard"))

@offers.route("/plan/<int:plan_id>")
@login_required
def view_plan(plan_id):
    plan = Plan.query.get_or_404(plan_id)
    # Allow both the plan owner (influencer) and businesses to view the plan
    if current_user.user_type == "influencer" and plan.influencer_id != current_user.id:
        flash("دسترسی غیرمجاز.", "error")
        return redirect(url_for("main.dashboard"))
    
    # Convert comma-separated services to list
    services = plan.services_requested.split(',') if plan.services_requested else []
    
    return render_template(
        "view_plan.html",
        plan=plan,
        offers=plan.offers,
        services=services,
        user_type=current_user.user_type,
        STATUS_UNDER_REVIEW=STATUS_UNDER_REVIEW,
    )

@offers.route("/submit_offer/<int:plan_id>", methods=["GET", "POST"])
@login_required
def submit_offer(plan_id):
    if current_user.user_type != "business":
        flash("دسترسی غیرمجاز.", "error")
        return redirect(url_for("main.dashboard"))

    plan = Plan.query.get_or_404(plan_id)

    if request.method == "POST":
        new_offer = Offer(
            plan_id=plan_id,
            business_id=current_user.id,
            service_offered=request.form.get("service_offered"),
            description=request.form.get("description"),
            status=STATUS_UNDER_REVIEW,
        )
        try:
            db.session.add(new_offer)
            db.session.commit()
            flash("پیشنهاد شما با موفقیت ثبت شد.", "success")
            return redirect(url_for("main.dashboard"))
        except Exception as e:
            db.session.rollback()
            print(f"Error submitting offer: {e}")
            flash("خطا در ثبت پیشنهاد. لطفاً دوباره تلاش کنید.", "error")

    return render_template(
        "submit_offer.html",
        plan=plan,
        user_type=current_user.user_type,
    )

@offers.route("/update_offer_status/<int:offer_id>/<string:status>")
@login_required
def update_offer_status(offer_id, status):
    if current_user.user_type != "influencer":
        flash("دسترسی غیرمجاز.", "error")
        return redirect(url_for("main.dashboard"))

    offer = Offer.query.get_or_404(offer_id)
    plan = Plan.query.get(offer.plan_id)

    if plan.influencer_id != current_user.id:
        flash("دسترسی غیرمجاز.", "error")
        return redirect(url_for("main.dashboard"))

    if status == STATUS_ACCEPTED:
        offer.status = STATUS_ACCEPTED
        plan.status = STATUS_ACCEPTED  # Update plan status when offer is accepted

        # Reject other offers for the same plan and same service/category
        other_offers = Offer.query.filter(
            Offer.plan_id == plan.id,
            Offer.id != offer.id,
            Offer.service_offered == offer.service_offered,
            Offer.status == STATUS_UNDER_REVIEW
        ).all()
        for other_offer in other_offers:
            other_offer.status = STATUS_REJECTED

    elif status == STATUS_REJECTED:
        offer.status = STATUS_REJECTED

    try:
        db.session.commit()
        flash("وضعیت پیشنهاد با موفقیت به‌روزرسانی شد.", "success")
    except Exception as e:
        db.session.rollback()
        print(f"Error updating offer status: {e}")
        flash("خطا در به‌روزرسانی وضعیت پیشنهاد. لطفاً دوباره تلاش کنید.", "error")

    return redirect(url_for("offers.view_plan", plan_id=plan.id))
