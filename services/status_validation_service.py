# TAGS: [status_validation], [applicant_bot_usage]


import json
import logging
from pathlib import Path
from services.data_service import get_applicant_bot_records_file_path

logger = logging.getLogger(__name__)



# ****** METHODS with TAGS: [status_validation] ******

def is_applicant_in_applicant_bot_records(applicant_record_id: str) -> bool:
    # TAGS: [status_validation],[applicant_bot_usage]
    """Check if user is in records."""
    applicant_bot_records_file_path = get_applicant_bot_records_file_path()
    with open(applicant_bot_records_file_path, "r", encoding="utf-8") as f:
        applicant_bot_records = json.load(f)
    if applicant_record_id in applicant_bot_records:
        logger.debug(f"'applicant_record_id': {applicant_record_id} found in records")
        return True
    else:
        logger.debug(f"'applicant_record_id': {applicant_record_id} not found in records")
        return False


def is_applicant_privacy_policy_confirmed(applicant_record_id: str) -> bool:
    # TAGS: [status_validation],[applicant_bot_usage]
    """Check if privacy policy is confirmed."""
    applicant_bot_records_file_path = get_applicant_bot_records_file_path()
    with open(applicant_bot_records_file_path, "r", encoding="utf-8") as f:
        applicant_bot_records = json.load(f)
    if applicant_record_id in applicant_bot_records:
        if applicant_bot_records[applicant_record_id]["privacy_policy_confirmed"] == "yes":
            logger.debug(f"privacy_policy is confirmed for 'applicant_record_id': {applicant_record_id} in {applicant_bot_records_file_path}")
            return True
        else:
            logger.debug(f"privacy_policy is NOT confirmed for 'applicant_record_id': {applicant_record_id} in {applicant_bot_records_file_path}")
            return False
    else:
        logger.debug(f"'applicant_record_id': {applicant_record_id} is not found in {applicant_bot_records_file_path}")
        return False


def is_welcome_video_shown_to_applicant(applicant_record_id: str) -> bool:
    # TAGS: [status_validation],[applicant_bot_usage]
    """Check if welcome video is shown."""
    applicant_bot_records_file_path = get_applicant_bot_records_file_path()
    with open(applicant_bot_records_file_path, "r", encoding="utf-8") as f:
        applicant_bot_records = json.load(f)
    if applicant_record_id in applicant_bot_records:
        if applicant_bot_records[applicant_record_id]["welcome_video_shown"] == "yes":
            logger.debug(f"welcome video is shown for 'applicant_record_id': {applicant_record_id} in {applicant_bot_records_file_path}")
            return True
        else:
            logger.debug(f"welcome video is NOT shown for 'applicant_record_id': {applicant_record_id} in {applicant_bot_records_file_path}")
            return False
    else:
        logger.debug(f"'applicant_record_id': {applicant_record_id} is not found in {applicant_bot_records_file_path}")
        return False


def is_resume_video_received(applicant_record_id: str) -> bool:
    # TAGS: [status_validation],[applicant_bot_usage]
    """Check if resume video is received."""
    applicant_bot_records_file_path = get_applicant_bot_records_file_path()
    with open(applicant_bot_records_file_path, "r", encoding="utf-8") as f:
        applicant_bot_records = json.load(f)
    if applicant_record_id in applicant_bot_records:
        if applicant_bot_records[applicant_record_id]["resume_video_received"] == "yes":
            logger.debug(f"resume video is received for 'applicant_record_id': {applicant_record_id} in {applicant_bot_records_file_path}")
            return True
        else:
            logger.debug(f"resume video is NOT received for 'applicant_record_id': {applicant_record_id} in {applicant_bot_records_file_path}")
            return False
    else:
        logger.debug(f"'applicant_record_id': {applicant_record_id} is not found in {applicant_bot_records_file_path}")
        return False
