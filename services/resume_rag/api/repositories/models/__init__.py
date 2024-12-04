import pkgutil
import importlib
import os
from sqlalchemy.orm import declarative_base

# Import this in alembic_migrations/config/autogenerate_base_metadatas.py
Base = declarative_base()

# Import all other modules in current package for Alembic's autogenerate in env.py target_metadata.
# This ensures that all models are registered with the Base metadata, allowing Alembic to detect
# and include all tables when generating migration scripts without the need to manually import each model.
package_dir = os.path.dirname(__file__)
for (module_loader, name, ispkg) in pkgutil.iter_modules([package_dir]):
    importlib.import_module(f"{__name__}.{name}")