
table_name = "score_storage"

class ScoreStorage(Base):
    __tablename__ = table_name

    id = Column(Integer, Sequence(f"{table_name}_id_seq"), primary_key=True, nullable=False)
    token_name = Column(String(256), nullable=False)
    score = Column(Integer, CheckConstraint('your_column > 0 AND your_column < 100'))
    # min_value = Column(Numeric(10, 2))
    # max_value = Column(Numeric(10, 2))
    # units = Column(String(20))