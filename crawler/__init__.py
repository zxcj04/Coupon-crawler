from .db.costco import CostcoDB


class CostcoDBSingleton:
    _instance = None

    @staticmethod
    def get_instance():
        if CostcoDBSingleton._instance is None:
            CostcoDBSingleton._instance = CostcoDB()
        return CostcoDBSingleton._instance
