import logging

# Internal packages:
from service.handlers import BuilderFactory, GitHandler, upload_folder_to_hdfs
from service.static import Request

logger = logging.getLogger(__name__)


def mark_success(request: Request, hdfs_jar_location: str) -> dict:
    return {
        **request.__dict__,
        "hdfs_location": hdfs_jar_location
    }


def run_build(request: Request) -> dict:
    logger.info(f"Build operation started for TransactionId: {request.transaction_id}, BoxId: {request.box_id}")
    builder = BuilderFactory(request=request, config_manager=request.config).get_builder()
    logger.info("Builder fetched!")
    logger.debug(f"fetched builder: {type(builder)}")
    git_handler = GitHandler(url=request.git_url, branch=request.branch, target_location=request.local_base)
    logger.info("GitHandler initialized! Cloning repo...")
    try:
        git_handler.clone()
        logger.info("Git repo cloned! Running builder...")
        local_jar_location = builder.build()
        logger.info("Jar's build complete!")
        jar_hdfs_location = upload_folder_to_hdfs(
            config=request.config,
            environment=request.environment,
            hdfs_path=request.hdfs_path,
            local_path=local_jar_location
        )
        logger.info("Jar's uploaded to HDFS")
        logger.debug(f"HDFS path: {request.hdfs_path}, Environment: {request.config.environment}")
    except Exception as e:
        logger.error(f"Error in build process: {e}")
        raise e
    else:
        logger.info(f"Build operation finished for TransactionId: {request.transaction_id}, BoxId: {request.box_id}")
        return mark_success(request, jar_hdfs_location)
    finally:
        builder.cleanup(build_base_path=git_handler.local_base_path)
