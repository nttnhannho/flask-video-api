from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path


app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)


class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(title={title}, views={views}, likes={likes})"

if not Path("database.db").exists():
    db.create_all()

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("title", type=str, help="Title of the video is required", required=True)
video_put_args.add_argument("views", type=int, help="Views of the video is required", required=True)
video_put_args.add_argument("likes", type=int, help="Likes on the video is required", required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("title", type=str, help="Title of the video")
video_update_args.add_argument("views", type=int, help="Views of the video")
video_update_args.add_argument("likes", type=int, help="Likes on the video")

resource_fields = {
    "id": fields.Integer,
    "title": fields.String,
    "views": fields.Integer,
    "likes": fields.Integer
}


class Video(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message=f"Could not find video with id = {video_id}...")

        return result

    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()

        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message=f"Video id = {video_id} is taken...")

        video = VideoModel(id=video_id, title=args["title"], views=args["views"], likes=args["likes"])
        db.session.add(video)
        db.session.commit()

        return video, 201

    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_update_args.parse_args()

        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message=f"Video id = {video_id} does not exist, cannot update!")

        if args["title"]:
            result.title = args["title"]
        if args["views"]:
            result.views = args["views"]
        if args["likes"]:
            result.likes = args["likes"]

        db.session.commit()

        return result

    def delete(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message=f"Video id = {video_id} does not exist, cannot delete!")
        db.session.delete(result)
        db.session.commit()
        return "", 204


api.add_resource(Video, "/video/<int:video_id>")


if __name__ == "__main__":
    app.run(debug=True)
