from crewai.tools import tool
import mysql.connector
import os
from threading import Lock
from pydantic import BaseModel


class MySQLConnectionPool:
    _pool = None
    _lock = Lock()

    @classmethod
    def initialize_pool(cls):
        with cls._lock:
            if cls._pool is None:
                cls._pool = mysql.connector.pooling.MySQLConnectionPool(
                    pool_name="churn-analysis-pool",
                    pool_size=5,
                    host=os.environ.get("MYSQL_HOST"),
                    user=os.environ.get("MYSQL_USER"),
                    password=os.environ.get("MYSQL_PASSWORD"),
                    database=os.environ.get("MYSQL_DATABASE"),
                )

    @classmethod
    def get_connection(cls):
        if cls._pool is None:
            cls.initialize_pool()
        return cls._pool.get_connection()

    @classmethod
    def close_pool(cls):
        with cls._lock:
            if cls._pool:
                cls._pool = None


def fetchData(companyId: str) -> str:
    # connection = MySQLConnectionPool.get_connection()
    # cursor = connection.cursor()

    # try:
    #     query = "SELECT * FROM ViewLogin30d WHERE companyId = %s"
    #     cursor.execute(query, (companyId,))
    #     results = cursor.fetchall()
    #     return results
    # except mysql.connector.Error as e:
    #     return f"Erro ao buscar dados: {e}"
    # finally:
    #     cursor.close()
    #     connection.close()
    return {
        "companyId": companyId,
        "loginCount": 10,
        "numberOfCampaigns": 2,
        "numberOfIntegrations": 1,
    }


class CompanyDataModel(BaseModel):
    companyId: str
    loginCount: int
    numberOfCampaigns: int
    numberOfIntegrations: int


@tool("classifyChurnMLTool")
def classifyChurnMLTool(companyData: CompanyDataModel) -> str:
    """This tool predicts the churn risk of a company based on data from the last 30 days."""
    return {
        "companyId": companyData.companyId,
        "churnRisk": 0.9,
        "churnRiskLabel": "High",
        "MostImportantFeatures": "lowLoginCount, lowNumberOfCampaigns, lowNumberOfIntegrations",
    }
