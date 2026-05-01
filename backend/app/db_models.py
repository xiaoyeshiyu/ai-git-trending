"""
数据库抽象层 - 使用 SQLAlchemy ORM 支持 SQLite 和 PostgreSQL

特性：
- 支持 SQLite 和 PostgreSQL
- 统一的连接管理
- 自动创建表和索引
- 优化的字段类型
"""
from sqlalchemy import create_engine, Column, Integer, String, Text, Date, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import date
from typing import Optional, List, Dict, Any, Set
from contextlib import contextmanager

from config.settings import DatabaseConfig
from config.logging_config import get_logger

logger = get_logger('database', 'INFO')

Base = declarative_base()


# ==================== 维度表模型 ====================

class DimLanguage(Base):
    """语言维度表"""
    __tablename__ = 'dim_languages'
    
    language_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    
    # 关系
    projects = relationship("DimProject", back_populates="language")


class DimTag(Base):
    """标签维度表"""
    __tablename__ = 'dim_tags'
    
    tag_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    
    # 关系
    projects = relationship("DimProject", secondary="assoc_project_tags", back_populates="tags")


class DimDate(Base):
    """日期维度表"""
    __tablename__ = 'dim_dates'
    
    date_id = Column(Integer, primary_key=True)  # YYYYMMDD 格式
    full_date = Column(Date, nullable=False, unique=True)
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    day = Column(Integer, nullable=False)
    weekday = Column(Integer, nullable=False)  # 0=Monday, 6=Sunday
    week_of_year = Column(Integer, nullable=False)


class DimProject(Base):
    """项目维度表"""
    __tablename__ = 'dim_projects'
    
    project_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    url = Column(String(500))
    description = Column(Text)
    language_id = Column(Integer, ForeignKey('dim_languages.language_id'))
    
    # 关系
    language = relationship("DimLanguage", back_populates="projects")
    tags = relationship("DimTag", secondary="assoc_project_tags", back_populates="projects")
    snapshots = relationship("FactTrendingSnapshot", back_populates="project")


class AssocProjectTag(Base):
    """项目-标签关联表"""
    __tablename__ = 'assoc_project_tags'
    
    project_id = Column(Integer, ForeignKey('dim_projects.project_id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('dim_tags.tag_id'), primary_key=True)


# ==================== 事实表模型 ====================

class FactTrendingSnapshot(Base):
    """趋势快照事实表"""
    __tablename__ = 'fact_trending_snapshots'
    
    snapshot_id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('dim_projects.project_id'), nullable=False)
    date_id = Column(Integer, ForeignKey('dim_dates.date_id'), nullable=False)
    rank = Column(Integer, nullable=False)
    stars = Column(Integer)
    forks = Column(Integer)
    
    # 关系
    project = relationship("DimProject", back_populates="snapshots")
    date = relationship("DimDate")
    
    __table_args__ = (
        UniqueConstraint('project_id', 'date_id', name='uq_project_date'),
        Index('idx_fact_date_id', 'date_id'),
        Index('idx_fact_project_id', 'project_id'),
    )


# ==================== 汇总表模型 ====================

class SummarizedProject(Base):
    """项目汇总表 - 用于快速查询展示"""
    __tablename__ = 'summarized_projects'

    name = Column(String(255), primary_key=True)
    url = Column(String(500))
    description = Column(Text)
    language = Column(String(100))
    stars = Column(Integer)
    forks = Column(Integer)
    contributor_count = Column(Integer)
    created_at = Column(String(50))
    updated_at = Column(String(50))
    open_issues = Column(Integer)
    watchers = Column(Integer)
    summary_date = Column(Date, nullable=False)
    tech_domain = Column(String(100))  # 技术领域

    __table_args__ = (
        Index('idx_summarized_language', 'language'),
        Index('idx_summarized_summary_date', 'summary_date'),
        Index('idx_summarized_stars', 'stars'),
        Index('idx_summarized_forks', 'forks'),
        Index('idx_summarized_tech_domain', 'tech_domain'),
    )


# ==================== 数据库管理器 ====================

class DatabaseManager:
    """数据库管理器 - 统一管理数据库连接和会话"""
    
    _instance = None
    _engine = None
    _SessionFactory = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._engine is None:
            self._initialize_engine()
    
    def _initialize_engine(self):
        """初始化数据库引擎"""
        db_url = DatabaseConfig.get_database_url()
        engine_options = DatabaseConfig.get_engine_options()
        
        self._engine = create_engine(db_url, **engine_options)
        self._SessionFactory = sessionmaker(bind=self._engine)
        
        logger.info(f"📦 数据库引擎初始化: {DatabaseConfig.DB_TYPE}")
    
    def create_tables(self):
        """创建所有表和索引"""
        Base.metadata.create_all(self._engine)
        logger.info("✅ 数据库表创建完成")
    
    @contextmanager
    def get_session(self):
        """获取数据库会话（上下文管理器）"""
        session = self._SessionFactory()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"❌ 数据库操作错误: {e}")
            raise
        finally:
            session.close()
    
    def get_engine(self):
        """获取数据库引擎"""
        return self._engine


# 全局数据库管理器实例
db_manager = DatabaseManager()


# ==================== 数据访问层 ====================

class ProjectRepository:
    """项目数据访问层"""
    
    def __init__(self, manager: DatabaseManager = None):
        self.manager = manager or db_manager
    
    # ==================== 维度操作 ====================
    
    def get_or_create_language(self, session, name: str) -> Optional[int]:
        """获取或创建语言ID"""
        if not name or name == 'N/A':
            return None
        
        lang = session.query(DimLanguage).filter_by(name=name).first()
        if lang:
            return lang.language_id
        
        lang = DimLanguage(name=name)
        session.add(lang)
        session.flush()
        return lang.language_id
    
    def get_or_create_tag(self, session, name: str) -> int:
        """获取或创建标签ID"""
        tag = session.query(DimTag).filter_by(name=name).first()
        if tag:
            return tag.tag_id
        
        tag = DimTag(name=name)
        session.add(tag)
        session.flush()
        return tag.tag_id
    
    def get_or_create_date(self, session, date_obj: date) -> int:
        """获取或创建日期ID"""
        date_id = int(date_obj.strftime('%Y%m%d'))
        
        dim_date = session.query(DimDate).filter_by(date_id=date_id).first()
        if dim_date:
            return date_id
        
        dim_date = DimDate(
            date_id=date_id,
            full_date=date_obj,
            year=date_obj.year,
            month=date_obj.month,
            day=date_obj.day,
            weekday=date_obj.weekday(),
            week_of_year=date_obj.isocalendar()[1]
        )
        session.add(dim_date)
        session.flush()
        return date_id
    
    def get_or_create_project(self, session, project_data: Dict) -> int:
        """获取或创建项目ID"""
        project = session.query(DimProject).filter_by(name=project_data['name']).first()
        if project:
            return project.project_id
        
        lang_id = self.get_or_create_language(session, project_data.get('language'))
        
        project = DimProject(
            name=project_data['name'],
            url=project_data.get('url'),
            description=project_data.get('description'),
            language_id=lang_id
        )
        session.add(project)
        session.flush()
        
        # 添加标签
        for tag_name in project_data.get('tags', []):
            tag_id = self.get_or_create_tag(session, tag_name)
            assoc = AssocProjectTag(project_id=project.project_id, tag_id=tag_id)
            session.add(assoc)
        
        return project.project_id
    
    # ==================== 事实表操作 ====================
    
    def add_trending_snapshots(self, projects_data: List[Dict], snapshot_date: date):
        """添加趋势快照"""
        with self.manager.get_session() as session:
            date_id = self.get_or_create_date(session, snapshot_date)
            
            for project_data in projects_data:
                project_id = self.get_or_create_project(session, project_data)
                
                # 检查是否已存在
                existing = session.query(FactTrendingSnapshot).filter_by(
                    project_id=project_id, date_id=date_id
                ).first()
                
                if not existing:
                    snapshot = FactTrendingSnapshot(
                        project_id=project_id,
                        date_id=date_id,
                        rank=project_data['rank'],
                        stars=project_data.get('stars', 0),
                        forks=project_data.get('forks', 0)
                    )
                    session.add(snapshot)
    
    # ==================== 汇总表操作 ====================
    
    def get_all_summarized_project_names(self) -> Set[str]:
        """获取所有已汇总项目名称"""
        with self.manager.get_session() as session:
            projects = session.query(SummarizedProject.name).all()
            return {p.name for p in projects}
    
    def add_summarized_project(self, project: Dict):
        """添加或更新汇总项目"""
        if not project:
            return
        
        def safe_int(value, default=0):
            if value == 'N/A' or value is None:
                return default
            try:
                return int(value)
            except (ValueError, TypeError):
                return default
        
        with self.manager.get_session() as session:
            summarized = session.query(SummarizedProject).filter_by(
                name=project.get('name')
            ).first()
            
            if summarized:
                # 更新
                summarized.url = project.get('url')
                summarized.description = project.get('description', 'N/A')
                summarized.language = project.get('language', 'N/A')
                summarized.stars = safe_int(project.get('stars'))
                summarized.forks = safe_int(project.get('forks'))
                summarized.contributor_count = safe_int(project.get('contributor_count'))
                summarized.created_at = project.get('created_at', 'N/A')
                summarized.updated_at = project.get('updated_at', 'N/A')
                summarized.open_issues = safe_int(project.get('open_issues'))
                summarized.watchers = safe_int(project.get('watchers'))
                summarized.summary_date = date.today()
            else:
                # 创建
                summarized = SummarizedProject(
                    name=project.get('name'),
                    url=project.get('url'),
                    description=project.get('description', 'N/A'),
                    language=project.get('language', 'N/A'),
                    stars=safe_int(project.get('stars')),
                    forks=safe_int(project.get('forks')),
                    contributor_count=safe_int(project.get('contributor_count')),
                    created_at=project.get('created_at', 'N/A'),
                    updated_at=project.get('updated_at', 'N/A'),
                    open_issues=safe_int(project.get('open_issues')),
                    watchers=safe_int(project.get('watchers')),
                    summary_date=date.today()
                )
                session.add(summarized)


# 向后兼容：保留原有接口
class ProjectDatabase:
    """向后兼容的数据库接口"""
    
    def __init__(self, db_path=None):
        # 忽略 db_path 参数，使用新架构
        self._repo = ProjectRepository()
        self._manager = db_manager
        self._manager.create_tables()
    
    def _get_connection(self):
        """向后兼容：返回原始连接（用于复杂查询）"""
        return self._manager.get_engine().connect()
    
    def add_trending_snapshots(self, projects_data, snapshot_date):
        """添加趋势快照"""
        self._repo.add_trending_snapshots(projects_data, snapshot_date)
    
    def get_all_summarized_project_names(self):
        """获取所有已汇总项目名称"""
        return self._repo.get_all_summarized_project_names()
    
    def add_summarized_project(self, project):
        """添加汇总项目"""
        self._repo.add_summarized_project(project)
