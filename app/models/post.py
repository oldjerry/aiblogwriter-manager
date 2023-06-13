from app.extensions import db


class ScrapedPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    href = db.Column(db.String(200))
    img_href = db.Column(db.String(200))
    date = db.Column(db.String(20))
    category = db.Column(db.String(20))
    article = db.Column(db.Text)
    processed = db.Column(db.Boolean)
    gen_time = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Post "{self.title}">'