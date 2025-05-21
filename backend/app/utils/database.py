from sqlalchemy import create_engine

DATABASE_URL='postgresql://postgres:ZENStvKGjPthLKeuBBjsdwIsDnpDhZUm@maglev.proxy.rlwy.net:17086/railway'
engine = create_engine(DATABASE_URL)