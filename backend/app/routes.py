# backend/app/routes.py

import os
import uuid
from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from .models import User, ProviderProfile, JobRequest, Message, Review, Work, db

main_bp = Blueprint("main", __name__)


### Helper to check allowed extensions ###
def allowed_file(filename):
    """
    Return True if the file has an allowed extension.
    """
    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in current_app.config["ALLOWED_EXTENSIONS"]


### 1) User Registration ###
@main_bp.route("/api/register", methods=["POST"])
def register():
    data = request.json or {}

    email = data.get("email")
    password = data.get("password")
    role = data.get("role")
    full_name = data.get("full_name")

    if not all([email, password, role, full_name]):
        return jsonify({"error": "Missing fields"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 409

    user = User(
        email=email,
        password_hash=generate_password_hash(password),
        role=role,
        full_name=full_name,
    )
    db.session.add(user)
    db.session.commit()

    if role == "provider":
        bio = data.get("bio", None)
        equipment_specs = data.get("equipment_specs", None)
        pricing_info = data.get("pricing_info", None)
        location = data.get("location", None)

        profile = ProviderProfile(
            user_id=user.id,
            bio=bio,
            equipment_specs=equipment_specs,
            pricing_info=pricing_info,
            location=location,
        )
        db.session.add(profile)
        db.session.commit()

    return jsonify({"message": "Registered successfully"}), 201


### 2) User Login ###
@main_bp.route("/api/login", methods=["POST"])
def login():
    data = request.json or {}
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify(
        {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "full_name": user.full_name,
        }
    ), 200


### 3) List All Providers ###
@main_bp.route("/api/providers", methods=["GET"])
def list_providers():
    profiles = ProviderProfile.query.all()
    result = []
    for p in profiles:
        works = Work.query.filter_by(provider_id=p.user.id).limit(3).all()
        works_data = [
            {"id": w.id, "image_url": w.image_url, "title": w.title} for w in works
        ]
        result.append(
            {
                "id": p.user.id,
                "full_name": p.user.full_name,
                "bio": p.bio,
                "equipment_specs": p.equipment_specs,
                "pricing_info": p.pricing_info,
                "location": p.location,
                "works": works_data,
            }
        )
    return jsonify(result), 200


### 4) Get Single Provider (and All Their Works) ###
@main_bp.route("/api/providers/<int:provider_id>", methods=["GET"])
def get_provider(provider_id):
    profile = ProviderProfile.query.filter_by(user_id=provider_id).first()
    if not profile:
        return jsonify({"error": "Provider not found"}), 404

    works = Work.query.filter_by(provider_id=provider_id).all()
    works_data = [
        {"id": w.id, "image_url": w.image_url, "title": w.title} for w in works
    ]
    return jsonify(
        {
            "id": profile.user.id,
            "full_name": profile.user.full_name,
            "bio": profile.bio,
            "equipment_specs": profile.equipment_specs,
            "pricing_info": profile.pricing_info,
            "location": profile.location,
            "works": works_data,
        }
    ), 200


### 5) Create Job Request ###
@main_bp.route("/api/job_requests", methods=["POST"])
def create_job():
    data = request.json or {}
    customer_id = data.get("customer_id")
    provider_id = data.get("provider_id")
    title = data.get("title")
    description = data.get("description")
    model_file_url = data.get("model_file_url")

    if not all([customer_id, provider_id, title, description]):
        return jsonify({"error": "Missing fields"}), 400

    job = JobRequest(
        customer_id=customer_id,
        provider_id=provider_id,
        title=title,
        description=description,
        model_file_url=model_file_url,
    )
    db.session.add(job)
    db.session.commit()
    return jsonify({"message": "Job request created", "job_id": job.id}), 201


### 6) Get All Job Requests for a Customer ###
@main_bp.route("/api/job_requests/customer/<int:customer_id>", methods=["GET"])
def get_customer_jobs(customer_id):
    jobs = JobRequest.query.filter_by(customer_id=customer_id).all()
    result = []
    for j in jobs:
        result.append(
            {
                "id": j.id,
                "provider_id": j.provider_id,
                "title": j.title,
                "description": j.description,
                "status": j.status,
                "price_offered": str(j.price_offered),
                "created_at": j.created_at,
            }
        )
    return jsonify(result), 200


### 7) Get All Job Requests for a Provider ###
@main_bp.route("/api/job_requests/provider/<int:provider_id>", methods=["GET"])
def get_provider_jobs(provider_id):
    jobs = JobRequest.query.filter_by(provider_id=provider_id).all()
    result = []
    for j in jobs:
        result.append(
            {
                "id": j.id,
                "customer_id": j.customer_id,
                "title": j.title,
                "description": j.description,
                "status": j.status,
                "price_offered": str(j.price_offered),
                "created_at": j.created_at,
            }
        )
    return jsonify(result), 200


### 8) Get a Single Job by ID ###
@main_bp.route("/api/job_requests/<int:job_id>", methods=["GET"])
def get_job(job_id):
    job = JobRequest.query.get_or_404(job_id)
    return jsonify(
        {
            "id": job.id,
            "customer_id": job.customer_id,
            "provider_id": job.provider_id,
            "title": job.title,
            "description": job.description,
            "model_file_url": job.model_file_url,
            "status": job.status,
            "price_offered": str(job.price_offered),
            "created_at": job.created_at,
            "updated_at": job.updated_at,
        }
    ), 200


### 9) Update Job Status ###
@main_bp.route("/api/job_requests/<int:job_id>/status", methods=["PUT"])
def update_job_status(job_id):
    data = request.json or {}
    status = data.get("status")
    job = JobRequest.query.get(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404
    job.status = status
    db.session.commit()
    return jsonify({"message": "Status updated"}), 200


### 10) Post a Message ###
@main_bp.route("/api/job_requests/<int:job_id>/messages", methods=["POST"])
def post_message(job_id):
    data = request.json or {}
    sender_id = data.get("sender_id")
    content = data.get("content")
    if not all([sender_id, content]):
        return jsonify({"error": "Missing fields"}), 400
    message = Message(job_request_id=job_id, sender_id=sender_id, content=content)
    db.session.add(message)
    db.session.commit()
    return jsonify({"message": "Message sent"}), 201


### 11) Get Messages for a Job ###
@main_bp.route("/api/job_requests/<int:job_id>/messages", methods=["GET"])
def get_messages(job_id):
    msgs = Message.query.filter_by(job_request_id=job_id).all()
    result = []
    for m in msgs:
        result.append(
            {
                "id": m.id,
                "sender_id": m.sender_id,
                "content": m.content,
                "created_at": m.created_at,
            }
        )
    return jsonify(result), 200


### 12) Post a Review ###
@main_bp.route("/api/job_requests/<int:job_id>/review", methods=["POST"])
def post_review(job_id):
    data = request.json or {}
    reviewer_id = data.get("reviewer_id")
    rating = data.get("rating")
    comment = data.get("comment")
    if not all([reviewer_id, rating]):
        return jsonify({"error": "Missing fields"}), 400
    review = Review(
        job_request_id=job_id, reviewer_id=reviewer_id, rating=rating, comment=comment
    )
    db.session.add(review)
    db.session.commit()
    return jsonify({"message": "Review submitted"}), 201


### 13) UPLOAD NEW WORK IMAGE ###
@main_bp.route("/api/providers/<int:provider_id>/works", methods=["POST"])
def upload_work(provider_id):
    """
    1) Check that form’s user_id matches provider_id OR user.role == 'admin'.
    2) Validate and save the uploaded image under UPLOAD_FOLDER.
    3) Create a Work record with image_url pointing to /uploads/<filename>.
    """
    # 1) Simple “authentication” check: form must supply user_id
    try:
        current_user_id = int(request.form.get("user_id", 0))
    except ValueError:
        return jsonify({"error": "Invalid user_id"}), 400

    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"error": "Invalid user"}), 403

    # Only allow if provider themself OR an admin
    if user.role != "admin" and current_user_id != provider_id:
        return jsonify({"error": "Unauthorized"}), 403

    # 2) Check for file in request
    if "image" not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    if not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed"}), 400

    # 3) Save with a secure, unique filename
    original_name = secure_filename(file.filename)
    unique_name = f"{uuid.uuid4().hex}_{original_name}"
    upload_folder = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_folder, exist_ok=True)
    filepath = os.path.join(upload_folder, unique_name)
    file.save(filepath)

    # 4) Optional: read a “title” field for the work
    title = request.form.get("title", "")

    new_work = Work(
        provider_id=provider_id, image_url=f"/uploads/{unique_name}", title=title
    )
    db.session.add(new_work)
    db.session.commit()

    return (
        jsonify(
            {
                "id": new_work.id,
                "provider_id": provider_id,
                "image_url": new_work.image_url,
                "title": new_work.title,
            }
        ),
        201,
    )


### 14) DELETE A WORK ###
@main_bp.route(
    "/api/providers/<int:provider_id>/works/<int:work_id>", methods=["DELETE"]
)
def delete_work(provider_id, work_id):
    """
    1) Ensure Work exists. 
    2) Only allow if provider themself OR user.role == 'admin'.
    3) Remove the file from disk.
    4) Delete the Work record from DB.
    """
    # 1) Look up the work
    work = Work.query.get_or_404(work_id)

    # 2) Check if user is authorized. We expect user_id in query string
    current_user_id = request.args.get("user_id", type=int)
    if not current_user_id:
        return jsonify({"error": "Missing user_id"}), 400

    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"error": "Invalid user"}), 403

    # Only allow if provider themself OR an admin
    if user.role != "admin" and work.provider_id != current_user_id:
        return jsonify({"error": "Unauthorized"}), 403

    # 3) Delete the file from disk
    filename = os.path.basename(work.image_url)
    file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        current_app.logger.error(f"Failed to remove file {file_path}: {e}")

    # 4) Delete DB record
    db.session.delete(work)
    db.session.commit()

    return ("", 204)
