# TAGS: [status_validation], [get_data], [create_data], [update_data], [directory_path], [file_path], [format_data], [applicant_bot_usage]

import os
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)



from services.constants import (
    DATA_DIR, 
    USERS_RECORDS_FILENAME, 
    RESUME_RECORDS_FILENAME,
    BOT_FOR_APPLICANTS_USERNAME,
    APPLICANT_BOT_DATA_DIR,
    APPLICANT_BOT_RECORDS_FILENAME,
    )


# ****** METHODS with TAGS: [get_data] ******


def get_applicant_bot_data_directory() -> Path:
    # TAGS: [get_data],[directory_path],[applicant_bot_usage]
    """Get the directory path for user data."""
    applicant_bot_data_dir = Path(APPLICANT_BOT_DATA_DIR)
    #return id if data_dir exists
    if applicant_bot_data_dir.exists():
        return applicant_bot_data_dir
    #create it and return the path if it doesn't exist
    else:
        applicant_bot_data_dir = create_applicant_bot_data_directory()
        return applicant_bot_data_dir


def get_applicant_bot_records_file_path() -> Optional[Path]:
    # TAGS: [get_data],[file_path],[applicant_bot_usage]
    """Get the path for applicant bot records file."""
    applicant_bot_records_file_path = get_applicant_bot_data_directory() / f"{APPLICANT_BOT_RECORDS_FILENAME}.json"
    if applicant_bot_records_file_path.exists():
        logger.debug(f"Applicant bot records file {applicant_bot_records_file_path} exists.")
        return applicant_bot_records_file_path
    else:
        applicant_bot_records_file_path = create_applicant_bot_records_file()
        logger.debug(f"Applicant bot records file {applicant_bot_records_file_path} created.")
        return applicant_bot_records_file_path


def get_manager_user_id_from_applicant_bot_records(applicant_record_id: str) -> Optional[str]:
    # TAGS: [get_data],[applicant_bot_usage]
    """Get the manager user id from applicant bot records."""
    applicant_bot_records_file_path = get_applicant_bot_records_file_path()
    with open(applicant_bot_records_file_path, "r", encoding="utf-8") as f:
        applicant_bot_records = json.load(f)
    if applicant_record_id in applicant_bot_records:
        return applicant_bot_records[applicant_record_id]["manager_user_id"]
    else:
        return None


def get_vacancy_id_from_applicant_bot_records(applicant_record_id: str) -> Optional[str]:
    # TAGS: [get_data],[applicant_bot_usage]
    """Get the vacancy id from applicant bot records."""
    applicant_bot_records_file_path = get_applicant_bot_records_file_path()
    with open(applicant_bot_records_file_path, "r", encoding="utf-8") as f:
        applicant_bot_records = json.load(f)
    if applicant_record_id in applicant_bot_records:
        return applicant_bot_records[applicant_record_id]["vacancy_id"]
    else:
        return None


def get_resume_id_from_applicant_bot_records(applicant_record_id: str) -> Optional[str]:
    # TAGS: [get_data],[applicant_bot_usage]
    """Get the resume id from applicant bot records."""
    applicant_bot_records_file_path = get_applicant_bot_records_file_path()
    with open(applicant_bot_records_file_path, "r", encoding="utf-8") as f:
        applicant_bot_records = json.load(f)
    if applicant_record_id in applicant_bot_records:
        return applicant_bot_records[applicant_record_id]["resume_id"]
    else:
        return None


def get_vacancy_directory_(user_record_id: str, vacancy_id: str) -> Optional[Path]:
    # TAGS: [get_data],[directory_path],[applicant_bot_usage]
    """Get the directory path for vacancy data."""
    data_dir = Path(DATA_DIR)
    if data_dir.exists():
        user_data_dir = data_dir / f"bot_user_id_{user_record_id}"
        if user_data_dir.exists():
            vacancy_data_dir = user_data_dir / f"vacancy_id_{vacancy_id}"
            if vacancy_data_dir.exists():
                logger.debug(f"Vacancy directory {vacancy_data_dir} exists.")
                return vacancy_data_dir 
            else:
                logger.debug(f"Vacancy directory {vacancy_data_dir} does not exist.")
                return None


def get_directory_for_video_from_applicants(user_record_id: str, vacancy_id: str) -> Optional[Path]:
    # TAGS: [get_data],[directory_path],[applicant_bot_usage]
    """Get the directory path for applicants videos."""
    vacancy_data_dir = get_vacancy_directory_(user_record_id=user_record_id, vacancy_id=vacancy_id)
    if vacancy_data_dir is None:
        logger.debug(f"Vacancy directory does not exist, cannot get video directory for bot_user_id: {user_record_id}, vacancy_id: {vacancy_id}")
        return None
    applicants_video_data_dir = vacancy_data_dir / "video_from_applicants"
    if applicants_video_data_dir.exists():
        logger.debug(f"Video directory from applicants {applicants_video_data_dir} exists.")
        return applicants_video_data_dir
    else:
        logger.debug(f"Video directory from applicants {applicants_video_data_dir} does not exist.")
        return None


def get_directory_for_video_from_managers(user_record_id: str, vacancy_id: str) -> Optional[Path]:
    # TAGS: [get_data],[directory_path],[applicant_bot_usage]
    """Get the directory path for managers videos."""
    vacancy_data_dir = get_vacancy_directory_(user_record_id=user_record_id, vacancy_id=vacancy_id)
    if vacancy_data_dir is None:
        logger.debug(f"Vacancy directory does not exist, cannot get video directory for bot_user_id: {user_record_id}, vacancy_id: {vacancy_id}")
        return None
    managers_video_data_dir = vacancy_data_dir / "video_from_managers"
    if managers_video_data_dir.exists():
        logger.debug(f"Video directory from applicants {managers_video_data_dir} exists.")
        return managers_video_data_dir
    else:
        logger.debug(f"Video directory from applicants {managers_video_data_dir} does not exist.")
        return None


def get_tg_user_data_attribute_from_update_object(update: Update, tg_user_attribute: str) -> str | int | None | bool | list | dict:
    # TAGS: [get_data],[applicant_bot_usage]
    """Collects Telegram user data from context and returns it as a dictionary."""
    tg_user = update.effective_user
    if tg_user:
        tg_user_attribute_value = tg_user.__getattribute__(tg_user_attribute)
        logger.debug(f"'{tg_user_attribute}': {tg_user_attribute_value} found in update.")
        return tg_user_attribute_value 
    else:
        logger.warning(f"'{tg_user_attribute}' not found in update. CHECK CORRECTNESS OF THE ATTRIBUTE NAME")
        return None


def get_decision_status_from_selected_callback_code(selected_callback_code: str) -> str:
    #TAGS: [get_data],[applicant_bot_usage]
    """Extract the meaningful part of a callback code.
    Args:
        selected_callback_code (str): Selected callback code, e.g. 'action_code:value'
    Returns:
        str: The part after the last colon, or the original string if no colon is present.
    """
    if ":" in selected_callback_code:
        return selected_callback_code.split(":")[-1].strip()
    else:
        return selected_callback_code


def get_bot_user_id_from_collected_data(data: dict) -> Optional[str]:
    """Get bot_user_id from collected dictionary. TAGS: [get_data]"""
    if "tg_user_id" in data:
        return str(data["tg_user_id"])
    else:
        logger.debug("'tg_user_id' not found in collected data.")
        return None



def get_path_to_video_from_applicant_from_resume_records(bot_user_id: str, vacancy_id: str, resume_record_id: str) -> Optional[Path]:
    """Get path to video from applicant from resume records.
    DO NOT CREATE, because APPLICANT BOT just reads.
    Return none if does not exist."""
    resume_records_file_path = get_resume_records_file_path(bot_user_id=bot_user_id, vacancy_id=vacancy_id)
    if resume_records_file_path is None:
        logger.debug(f"Resume records file path does not exist, cannot get video path for bot_user_id: {bot_user_id}, vacancy_id: {vacancy_id}, resume_record_id: {resume_record_id}")
        return None
    try:
        # Read existing data
        with open(resume_records_file_path, "r", encoding="utf-8") as f:
            resume_records = json.load(f)
        if resume_record_id in resume_records:
            video_path = resume_records[resume_record_id].get("resume_video_path")
            if video_path:
                logger.debug(f"Video path '{video_path}' found for resume_record_id: {resume_record_id}")
                return video_path
            else:
                logger.debug(f"Video path not set for resume_record_id: {resume_record_id}")
                return None
        else:
            logger.debug(f"Resume record '{resume_record_id}' not found in resume records file")
            return None
    except Exception as e:
        logger.error(f"Error reading resume records file {resume_records_file_path}: {e}")
        return None


def get_reply_from_update_object(update: Update):
    # TAGS: [get_data],[applicant_bot_usage]
    """ Get user reply to from the update object if user did one of below.
    1. sent message (text, photo, video, etc.) - update.message OR
    2. clicked button - update.callback_query.message
    If none of the above, return None
    """
    if update.message:
        return update.message.reply_text
    elif update.callback_query and update.callback_query.message:
        return update.callback_query.message.reply_text
    else:
        return None



# ****** METHODS with TAGS: [create_data] ******


def create_applicant_bot_data_directory() -> Path:
    # TAGS: [create_data],[directory_path],[applicant_bot_usage]
    """Create a directory for all data."""
    applicant_bot_data_dir = Path(APPLICANT_BOT_DATA_DIR)
    applicant_bot_data_dir.mkdir(parents=True, exist_ok=True)
    logger.debug(f"{applicant_bot_data_dir} created or exists.")
    return applicant_bot_data_dir


def create_applicant_bot_records_file() -> Path:
    # TAGS: [create_data],[file_path],[applicant_bot_usage]
    """Create a file with users data records if it doesn't exist."""
    data_dir = get_applicant_bot_data_directory()
    applicant_bot_records_file_path = data_dir / f"{APPLICANT_BOT_RECORDS_FILENAME}.json"
    if not applicant_bot_records_file_path.exists():
        applicant_bot_records_file_path.write_text(json.dumps({}), encoding="utf-8")
        logger.debug(f"{applicant_bot_records_file_path} created.")
    else:
        logger.debug(f"{applicant_bot_records_file_path} already exists.")


def create_applicant_bot_records(applicant_record_id: str) -> None:
    # TAGS: [create_data],[applicant_bot_usage]
    """Create applicant bot records."""
    applicant_bot_records_file_path = get_applicant_bot_records_file_path()
    with open(applicant_bot_records_file_path, "w", encoding="utf-8") as f:
        applicant_bot_records = json.load(f)
    
    # applicant_record_id is already a string - keep in mind JSON keys are always strings
    if applicant_record_id not in applicant_bot_records:
        applicant_bot_records[applicant_record_id] = {
            "manager_user_id": "",
            "vacancy_id": "",
            "resume_id": "",
            "applicant_user_id": applicant_record_id,
            "username": "",
            "first_name": "",
            "last_name": "",
            "privacy_policy_confirmed": "no",  
            "privacy_policy_confirmation_time": "",  
            "welcome_video_shown": "no", 
            "agreed_to_record_resume_video": "no",
            "resume_video_received": "no",
            "resume_video_path": "",
        }

        applicant_bot_records_file_path.write_text(json.dumps(applicant_bot_records, ensure_ascii=False, indent=2), encoding="utf-8")
        logger.info(f"{applicant_bot_records_file_path} has been successfully created with new resume_record: {applicant_record_id_str}")
    else:
        logger.debug(f"Skipping create: {applicant_record_id_str} already exists in the file {applicant_bot_records_file_path}")


# ****** METHODS with TAGS: [update_data] ******


def update_applicant_bot_records_with_top_level_key(applicant_record_id: str, key: str, value: str | int | bool | dict | list) -> None:
    # TAGS: [update_data],[applicant_bot_usage]
    """Update applicant bot records with new data."""
    applicant_bot_records_file_path = get_applicant_bot_records_file_path()
    with open(applicant_bot_records_file_path, "r", encoding="utf-8") as f:
        applicant_bot_records = json.load(f)
    if applicant_record_id in applicant_bot_records:
        applicant_bot_records[applicant_record_id][key] = value
        applicant_bot_records_file_path.write_text(json.dumps(applicant_bot_records, ensure_ascii=False, indent=2), encoding="utf-8")
        logger.debug(f"{applicant_bot_records_file_path} has been successfully updated with {key}={value}")
    else:
        logger.debug(f"Skipping update: {applicant_record_id} does not exist in the file {applicant_bot_records_file_path}")









def get_persistent_keyboard_messages(bot_user_id: str) -> list[tuple[int, int]]:
    """Get persistent keyboard message IDs for a user. Returns list of (chat_id, message_id) tuples. TAGS: [get_data]"""
    users_records_file_path = get_users_records_file_path()
    if users_records_file_path is None:
        logger.debug(f"Users records file path does not exist, cannot get persistent keyboard messages for bot_user_id: {bot_user_id}")
        return []
    try:
        with open(users_records_file_path, "r", encoding="utf-8") as f:
            records = json.load(f)
        if bot_user_id in records:
            keyboard_messages = records[bot_user_id].get("messages_with_keyboards", [])
            # Convert list of lists to list of tuples
            result = [tuple(msg) for msg in keyboard_messages if isinstance(msg, (list, tuple)) and len(msg) == 2]
            logger.debug(f"Found {len(result)} persistent keyboard messages for bot_user_id: {bot_user_id}")
            return result
        logger.debug(f"User {bot_user_id} not found in records")
        return []
    except Exception as e:
        logger.error(f"Error reading keyboard messages for {bot_user_id}: {e}")
        return []


def add_persistent_keyboard_message(bot_user_id: str, chat_id: int, message_id: int) -> None:
    # TAGS: [update_data]
    """Add a keyboard message ID to persistent storage."""
    users_records_file_path = get_users_records_file_path()
    if users_records_file_path is None:
        logger.debug(f"Users records file path does not exist, cannot add persistent keyboard message for bot_user_id: {bot_user_id}")
        return
    try:
        with open(users_records_file_path, "r", encoding="utf-8") as f:
            records = json.load(f)
        
        bot_user_id_str = str(bot_user_id)
        if bot_user_id_str not in records:
            logger.debug(f"User {bot_user_id_str} not found in records, cannot track keyboard")
            return
        
        if "messages_with_keyboards" not in records[bot_user_id_str]:
            records[bot_user_id_str]["messages_with_keyboards"] = []
        
        # Add if not already present
        keyboard_messages = records[bot_user_id_str]["messages_with_keyboards"]
        if [chat_id, message_id] not in keyboard_messages:
            keyboard_messages.append([chat_id, message_id])
            records[bot_user_id_str]["messages_with_keyboards"] = keyboard_messages
            users_records_file_path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
            logger.debug(f"Added keyboard message {message_id} to persistent storage for user {bot_user_id_str}")
    except Exception as e:
        logger.error(f"Error adding keyboard message to persistent storage: {e}")


def remove_persistent_keyboard_message(bot_user_id: str, chat_id: int, message_id: int) -> None:
    # TAGS: [update_data]
    """Remove a keyboard message ID from persistent storage."""
    users_records_file_path = get_users_records_file_path()
    if users_records_file_path is None:
        logger.debug(f"Users records file path does not exist, cannot remove persistent keyboard message for bot_user_id: {bot_user_id}")
        return
    try:
        with open(users_records_file_path, "r", encoding="utf-8") as f:
            records = json.load(f)
        
        bot_user_id_str = str(bot_user_id)
        if bot_user_id_str not in records:
            logger.debug(f"User {bot_user_id_str} not found in records, cannot remove keyboard message")
            return
        
        if "messages_with_keyboards" in records[bot_user_id_str]:
            keyboard_messages = records[bot_user_id_str]["messages_with_keyboards"]
            records[bot_user_id_str]["messages_with_keyboards"] = [
                msg for msg in keyboard_messages if not (msg[0] == chat_id and msg[1] == message_id)
            ]
            users_records_file_path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
            logger.debug(f"Removed keyboard message {message_id} from persistent storage for user {bot_user_id_str}")
    except Exception as e:
        logger.error(f"Error removing keyboard message from persistent storage: {e}")


def clear_all_persistent_keyboard_messages(bot_user_id: str) -> None:
    # TAGS: [update_data]
    """Clear all persistent keyboard messages for a user. """
    users_records_file_path = get_users_records_file_path()
    if users_records_file_path is None:
        logger.debug(f"Users records file path does not exist, cannot clear persistent keyboard messages for bot_user_id: {bot_user_id}")
        return
    try:
        with open(users_records_file_path, "r", encoding="utf-8") as f:
            records = json.load(f)
        
        bot_user_id_str = str(bot_user_id)
        if bot_user_id_str in records:
            records[bot_user_id_str]["messages_with_keyboards"] = []
            users_records_file_path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
            logger.debug(f"Cleared all persistent keyboard messages for user {bot_user_id_str}")
        else:
            logger.debug(f"User {bot_user_id_str} not found in records, cannot clear keyboard messages")
    except Exception as e:
        logger.error(f"Error clearing persistent keyboard messages: {e}")       











# ****** METHODS with TAGS: [format_data] ******

def format_oauth_link_text(oauth_link: str) -> str:
    # TAGS: [format_data]
    """Format oauth link text. TAGS: [format_data]"""
    return f"<a href=\"{oauth_link}\">Ссылка для авторизации</a>"
