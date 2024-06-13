from app.extensions import db


class ModelMixin:
    __abstract__ = True

    def save(self):
        # Save this model to the database.
        db.session.add(self)
        db.session.commit()
        return self
