import logging

# Internal packages:
from service.handlers import BuilderFactory, GitHandler
from service.static.config_manager import config
from service.static import Request

logger = logging.getLogger(__name__)


def run_build(request: Request) -> None:
    logger.info(f"Build operation started for TransactionId: {request.transaction_id}, BoxId: {request.box_id}")
    builder = BuilderFactory(request=request, config_manager=config).get_builder()
    logger.info("Builder fetched!")
    logger.debug(f"fetched builder: {type(builder)}")
    git_handler = GitHandler(url=request.git_url, branch=request.branch, target_location=request.local_base)
    logger.info("GitHandler initialized! Cloning repo...")
    try:
        git_handler.clone()
        logger.info("Git repo cloned! Running builder...")
        builder.build()
    except Exception as e:
        logger.error(f"Error in build process: {e}")
        raise e
    else:
        logger.info(f"Build operation finished for TransactionId: {request.transaction_id}, BoxId: {request.box_id}")
    finally:
        builder.cleanup(build_base_path=git_handler.local_base_path)
