
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy import Enum, Boolean, Sequence
from sqlalchemy.orm import sessionmaker



engine = create_engine('sqlite:///:memory:', echo=True)
Base = declarative_base()

class Sample(Base):
    """A Trace Organics sample result."""
    __tablename__ = 'sample'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    calibration_id = Column(Integer,
        ForeignKey("calibration.id"), nullable=False)
    identifier = Column(String)
    misc = Column(String)
    run_type = Column(String)
    vial = Column(Integer)
    amt_analyzed = Column(Float)
    multiplyer = Column(Float)
    folder = Column(String)
    operator = Column(String)
    acqui_method = Column(String)
    quant_method = Column(String)
    last_modified = Column(Date)
    date_acquired_col_1 = Column(Date)
    date_acquired_col_2 = Column(Date)
    col_1_window_low = Column(Float)
    col_1_window_high = Column(Float)
    col_2_window_low = Column(Float)
    col_2_window_high = Column(Float)


class Compound(Base):
    """The result for a particular compound obtained for a sample."""
    __tablename__ = 'compound'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    sample_id = Column(Integer, ForeignKey("sample.id"), nullable=False)
    column_id = Column(Integer)
    retention_time = Column(Float)
    low_rt = Column(Float)
    high_rt = Column(Float)
    value = Column(Float)
    area_count = Column(Float)
    is_rt = Column(Boolean)
    is_surrogate = Column(Boolean)
    is_aggregate = Column(Boolean)
    is_reported = Column(Boolean)


class AuditEntry(Base):
    """
    Audit entries composing the audit sequence documenting
    various user actions taken on sample data.
    """
    __tablename__ = 'audit_entry'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    sample_id = Column(Integer, ForeignKey("sample.id"), nullable=False)
    date = Column(Date)
    event = Column(String)
    message = Column(String)
    user = Column(String)


class Calibration(Base):
    __tablename__ = 'calibration'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    cal_type = Column(Enum('linear', 'avg_resp_fac', 'linear_thru_zero',
                           'quad', 'quad_thr_zero',
                           name='calibration_types'), default='avg_resp_fac')
    integration_type = Column(Enum('height', 'area', name='integration_types'),
                              default='height')
    regression_type = Column(Enum('equal_weights', 'inverse_conc',
                                  'inverse_conc_squared',
                                  name='regression_types'))
    compound_name = Column(String)
    number = Column(Integer)
    intercept = Column(Float)
    linear_coef = Column(Float)
    quad_coef = Column(Float)
    correlation = Column(Float)
    rsd = Column(Float)
    param_flag = Column(String)


class Calibrant(Base):
    __tablename__ = 'calibrant'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    calibration_id = Column(Integer, ForeignKey('calibration.id'),
        nullable=False)
    number = Column(Integer)
    folder = Column(String)
    true_val = Column(Float)
    response = Column(Float)
    resp_fac = Column(Float)
    column_id = Column(Integer)


class QualityControl(Base):
    __tablename__ = 'quality_control'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    method_group = Column(String)
    control_type = Column(Enum('limit', 'breakdown', 'recovery',
        name='control_types'))
    key = Column(String)
    level = Column(String)
    method = Column(String)
    matrix = Column(String)
    compound_name = Column(String)
    true_val = Column(Float)
    low_limit = Column(Float)
    high_limit = Column(Float)
    flag = Column(String) # TODO: this is confusing


# Create the tables in the db
Base.metadata.create_all(engine)

# Create the session factory for accessing the db
Session = sessionmaker(bind=engine)
