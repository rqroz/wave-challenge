"""
Base module for tests.
"""
from app.database import DATABASE
from app.setup import create_app


class BaseTestController:
    """
    Sets up an application for tests.
    """
    def setup(self):
        """
        Class setup: instantiates the test app, sets the DB session and cleans the DB to make sure test
        scenarios are clear.
        """
        self.app = create_app()
        self.session = DATABASE.session
        self._clean_db()

    def _clean_db_queries(self):
        """
        To be implemented by child controllers.
        Should define what queries need to be ran at the teardown of the class in order to clean the db.
        """
        raise NotImplementedError

    def _clean_db(self):
        """
        Cleans the db.
        """
        with self.app.app_context():
            self._clean_db_queries()
            self.session.commit()

    def teardown(self):
        """
        Class teardown: cleans the database.
        """
        self._clean_db()
