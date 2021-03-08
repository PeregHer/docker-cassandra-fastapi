from cassandra.cluster import Cluster
from cassandra.query import dict_factory


class Connexion:
    @classmethod
    def open_db(cls):
        cls.cluster = Cluster(['cassandra-01', 'cassandra-02'], port=9042)
        cls.session = cls.cluster.connect('resto')
        cls.session.row_factory = dict_factory

    @classmethod
    def close_db(cls):
        cls.cluster.shutdown()

    @classmethod
    def get_restaurant(cls, _id):
        cls.open_db()
        data = cls.session.execute(f"SELECT * FROM restaurant WHERE id={_id}").one()
        cls.close_db()
        return data

    @classmethod
    def get_resto_names(cls, cuisinetype):
        cls.open_db()
        data = cls.session.execute(f"SELECT name FROM restaurant WHERE cuisinetype = '{cuisinetype}'").all()
        cls.close_db()
        return {'type': cuisinetype, 'restos': [name['name'] for name in data]} 

    @classmethod
    def get_resto_inspec(cls, _id):
        cls.open_db()
        resto = cls.session.execute(f"SELECT name FROM restaurant WHERE id = {_id}").one()
        number = len(cls.session.execute(f"SELECT * FROM inspection WHERE idrestaurant = {_id}").all())
        cls.close_db()
        return {'name': resto['name'], 'inspections': number}

    @classmethod
    def get_top10(cls, grade):
        cls.open_db()
        top10 = cls.session.execute(f"SELECT idrestaurant FROM inspection WHERE grade = '{grade}' LIMIT 50").all()
        filters = tuple(_id['idrestaurant'] for _id in top10)
        top10 = cls.session.execute(f"SELECT name FROM restaurant WHERE id IN {filters}").all()
        cls.close_db()
        return {'grade': grade, 'restos': [name['name'] for name in top10[:10]]}