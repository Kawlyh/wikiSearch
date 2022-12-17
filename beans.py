#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd
import sqlalchemy as sql

Base = declarative_base()

user = 'root'
passwd = '970925'
host = 'localhost'
port = '3306'
db = 'wikilast'
# db = 'testwiki'

connect_string = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'\
    .format(user, passwd, host, port, db)
engine = sql.create_engine(connect_string)
session = sessionmaker(engine)()



class entity(Base):
    __tablename__ = 'entity'
    eid = sql.Column(sql.String(50), primary_key=True, index=True)
    etype = sql.Column(sql.String(50), nullable=True)
    epageid = sql.Column(sql.String(50), nullable=True)
    ens = sql.Column(sql.String(50), nullable=True)
    etitle = sql.Column(sql.String(50), nullable=True)
    elastrevid = sql.Column(sql.String(50), nullable=True)
    emodified = sql.Column(sql.String(50), nullable=True)


class labels(Base):
    __tablename__ = 'labels'
    lid = sql.Column(sql.BigInteger, primary_key=True)
    eid = sql.Column(sql.String(50), nullable=True, index=True)
    language = sql.Column(sql.String(20), nullable=True, index=True)
    value = sql.Column(sql.String(200), nullable=True)


class sitelinks(Base):
    __tablename__ = 'sitelinks'
    sid = sql.Column(sql.BigInteger, primary_key=True)
    eid = sql.Column(sql.String(50), nullable=True, index=True)
    site = sql.Column(sql.String(50), nullable=True, index=True)
    title = sql.Column(sql.String(500), nullable=True, index=True)
    badges = sql.Column(sql.String(500), nullable=True)
    url = sql.Column(sql.String(100), nullable=True)


class descriptions(Base):
    __tablename__ = 'descriptions'
    did = sql.Column(sql.BigInteger, primary_key=True)
    eid = sql.Column(sql.String(50), nullable=True, index=True)
    language = sql.Column(sql.String(20), nullable=True, index=True)
    value = sql.Column(sql.Text, nullable=True)


class aliases(Base):
    __tablename__ = 'aliases'
    aid = sql.Column(sql.BigInteger, primary_key=True)
    eid = sql.Column(sql.String(50), nullable=True, index=True)
    language = sql.Column(sql.String(20), nullable=True, index=True)
    value = sql.Column(sql.Text, nullable=True)


class statements(Base):
    __tablename__ = 'statements'
    sid = sql.Column(sql.String(80), primary_key=True, index=True)
    pid = sql.Column(sql.String(50), nullable=True, index=True)
    snakid = sql.Column(sql.String(50), nullable=True, index=True)
    stype = sql.Column(sql.String(50), nullable=True)
    srank = sql.Column(sql.String(50), nullable=True)
    eid = sql.Column(sql.String(50), nullable=True, index=True)


class qualifiers(Base):
    __tablename__ = 'qualifiers'
    qid = sql.Column(sql.BigInteger, primary_key=True)
    sid = sql.Column(sql.String(80), nullable=True, index=True)
    snakid = sql.Column(sql.String(50), nullable=True, index=True)
    eid = sql.Column(sql.String(50), nullable=True, index=True)


class references(Base):
    __tablename__ = 'refer'
    rid = sql.Column(sql.BigInteger, primary_key=True)
    sid = sql.Column(sql.String(80), nullable=True, index=True)
    snakid = sql.Column(sql.String(50), nullable=True, index=True)
    eid = sql.Column(sql.String(50), nullable=True, index=True)


class sank(Base):
    __tablename__ = 'snak'
    snakid = sql.Column(sql.String(50), primary_key=True, index=True)
    stype = sql.Column(sql.String(50), nullable=True, index=True)
    datatype = sql.Column(sql.String(50), nullable=True, index=True)


class string(Base):
    __tablename__ = 'string'
    snakid = sql.Column(sql.String(50), primary_key=True, index=True)
    pid = sql.Column(sql.String(50), nullable=True, index=True)
    hashv = sql.Column(sql.String(50), nullable=True)
    value = sql.Column(sql.Text, nullable=True)


class monotext(Base):
    __tablename__ = 'monotext'
    snakid = sql.Column(sql.String(50), primary_key=True, index=True)
    pid = sql.Column(sql.String(50), nullable=True, index=True)
    hashv = sql.Column(sql.String(50), nullable=True)
    language = sql.Column(sql.String(50), nullable=True, index=True)
    text = sql.Column(sql.Text, nullable=True)


class entityid(Base):
    __tablename__ = 'entityid'
    snakid = sql.Column(sql.String(50), primary_key=True, index=True)
    pid = sql.Column(sql.String(50), nullable=True, index=True)
    hashv = sql.Column(sql.String(50), nullable=True)
    entitytype = sql.Column(sql.String(50), nullable=True, index=True)
    entityid = sql.Column(sql.String(50), nullable=True, index=True)
    numericid = sql.Column(sql.String(50), nullable=True)


class globecoordinate(Base):
    __tablename__ = 'globecoordinate'
    snakid = sql.Column(sql.String(50), primary_key=True, index=True)
    pid = sql.Column(sql.String(50), nullable=True, index=True)
    hashv = sql.Column(sql.String(50), nullable=True)
    latitude = sql.Column(sql.String(50), nullable=True)
    longitude = sql.Column(sql.String(50), nullable=True)
    altitude = sql.Column(sql.String(50), nullable=True)
    precision = sql.Column(sql.String(50), nullable=True)
    globe = sql.Column(sql.String(100), nullable=True)


class time(Base):
    __tablename__ = 'time'
    snakid = sql.Column(sql.String(50), primary_key=True, index=True)
    pid = sql.Column(sql.String(50), nullable=True, index=True)
    hashv = sql.Column(sql.String(50), nullable=True)
    ttime = sql.Column(sql.String(50), nullable=True)
    timezone = sql.Column(sql.String(30), nullable=True)
    before = sql.Column(sql.String(50), nullable=True)
    after = sql.Column(sql.String(50), nullable=True)
    precision = sql.Column(sql.String(20), nullable=True)
    calendarmodel = sql.Column(sql.String(80), nullable=True)


class quantity(Base):
    __tablename__ = 'quantity'
    snakid = sql.Column(sql.String(50), primary_key=True, index=True)
    pid = sql.Column(sql.String(50), nullable=True, index=True)
    hashv = sql.Column(sql.String(50), nullable=True)
    amount = sql.Column(sql.String(500), nullable=True)
    upperbound = sql.Column(sql.String(50), nullable=True)
    lowerbound = sql.Column(sql.String(50), nullable=True)
    unit = sql.Column(sql.String(80), nullable=True)


class GetDBConnection():
    '''
    为其他组件提供数据库连接
    '''
    def getEngine(self):
        return engine

    def getSession(self):
        return session


class DBExecute():
    '''
    执行数据库操作
    '''
    def query(self, sql):
        df = 'error'
        try:
            df = pd.read_sql_query(sql, engine)
        except Exception as e:
            print('     连接数据库是发生如下错误：')
            print(e)
            exit()
        return df

    def addTo(self, bean, btype):
        session.add(bean)

    def addToCom(self, bean, btype):
        session.add(bean)

    def comm(self):
        session.commit()

    def addSetTo(self, beans, btype):
        '''
        beans[[bean, id], ... ]
        btype[db, primary_key]
        '''
        for bean in beans:
            qs = 'SELECT * FROM {} WHERE {}="{}"'.\
                    format(btype[0], btype[1], bean[1])
            if self.query(qs).empty:
                session.add(bean[0])
        session.commit()


'''
    def addTo(self, bean, btype):
        qs = 'SELECT * FROM {} WHERE {}="{}"'.\
            format(btype[0], btype[1], btype[2])
        if self.query(qs).empty:
            session.add(bean)

    def addToCom(self, bean, btype):
        qs = 'SELECT * FROM {} WHERE {}="{}"'.\
            format(btype[0], btype[1], btype[2])
        if self.query(qs).empty:
            session.add(bean)
            session.commit()
'''


# 若定义的数据表不存在，则创建
Base.metadata.create_all(engine)
