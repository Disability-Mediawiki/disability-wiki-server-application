from sqlalchemy import create_engine


class DbConnector():

    def create_db_engine(self):
        engine = create_engine(
            # "mysql+pymysql://user:password@host:3600/database",
            "mysql+pymysql://root:password@127.0.0.1/dis_wiki",
        )
        return engine
