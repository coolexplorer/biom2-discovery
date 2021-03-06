from sqlalchemy.orm import Session

from models.biom2_service import Biom2Service, Project, services_projects
from utils.logger import logger


def get_biom2_services(db: Session):
    return db.query(Biom2Service).all()


def get_biom2_services_by_project(db: Session, project):
    return db.query(Biom2Service).filter(Biom2Service.projects.any(name=project)).all()


def create_biom2_service(db: Session, biom2_service, projects):
    db_biom2_service = Biom2Service(
        name=biom2_service.name,
        major_version=biom2_service.major_version,
        minor_version=biom2_service.minor_version,
        patch_version=biom2_service.patch_version,
        url=biom2_service.url,
        type=biom2_service.type,
        environment=biom2_service.environment,
        friendly_name=biom2_service.friendly_name,
        description=biom2_service.description,
        icon_url=biom2_service.icon_url,
        source_link=biom2_service.source_link,
        docs_link=biom2_service.docs_link
    )

    # make relationship with project
    if len(projects) != 0:
        for project in projects:
            pro = get_project(db, project)
            if pro is None:
                insert_project(db, project)

            pro = get_project(db, project)
            db_biom2_service.projects.append(pro)

    return db_biom2_service


def insert_project(db: Session, project):
    db.add(Project(name=project))
    db.commit()


def get_project(db: Session, project):
    return db.query(Project).filter(Project.name == project).first()


def get_projects(db: Session):
    return db.query(Project).all()


def insert_services(db: Session, biom2_services):
    db.add_all(biom2_services)
    db.commit()


def delete_service_all_rows(db: Session):
    try:
        # delete all rows
        services = db.query(Biom2Service).all()

        for service in services:
            for project in service.projects:
                db.delete(project)
            db.delete(service)
        db.commit()
    except Exception:
        logger.debug("Deletion failed")
        db.rollback()
