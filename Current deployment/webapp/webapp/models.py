from webapp import db

class Protein(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    proteinname = db.Column(db.String(100))

