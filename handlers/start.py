from aiogram import Router, types, F
from aiogram.filters import Command, CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
from services.database import get_user_settings, update_user_settings
from utils.locales import LOCALES

router = Router()


def main_menu_keyboard(lang: str):
    texts = LOCALES[lang]
    builder = InlineKeyboardBuilder()
    builder.button(text=texts['btn_deploy_new'], callback_data="menu_deploy")
    builder.button(text=texts['btn_my_projects'], callback_data="menu_projects")
    builder.button(text=texts['btn_settings'], callback_data="menu_settings")
    builder.button(text=texts['btn_help'], callback_data="menu_help")
    builder.adjust(1, 1, 2)
    return builder.as_markup()


@router.message(CommandStart())
async def cmd_start(message: types.Message):
    settings = await get_user_settings(message.from_user.id)
    lang = settings.get("language")
    if not lang:
        builder = InlineKeyboardBuilder()
        builder.button(text="English 🇬🇧", callback_data="setlang_en")
        builder.button(text="العربية 🇸🇦", callback_data="setlang_ar")
        builder.adjust(2)
        await message.answer(LOCALES['en']['choose_language'], reply_markup=builder.as_markup())
        return
    await message.answer(LOCALES[lang]['welcome'], reply_markup=main_menu_keyboard(lang), parse_mode="Markdown")


@router.callback_query(F.data.startswith("setlang_"))
async def set_language(callback: types.CallbackQuery):
    lang = callback.data.split("_")[1]
    await update_user_settings(callback.from_user.id, {"language": lang})
    texts = LOCALES[lang]
    await callback.message.edit_text(
        texts['language_set'] + "\n\n" + texts['welcome'],
        reply_markup=main_menu_keyboard(lang),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data == "menu_main")
async def back_to_main(callback: types.CallbackQuery):
    settings = await get_user_settings(callback.from_user.id)
    lang = settings.get("language", "en")
    texts = LOCALES[lang]
    await callback.message.edit_text(texts['main_menu'], reply_markup=main_menu_keyboard(lang), parse_mode="Markdown")
    await callback.answer()


@router.callback_query(F.data == "menu_help")
async def show_help(callback: types.CallbackQuery):
    settings = await get_user_settings(callback.from_user.id)
    lang = settings.get("language", "en")
    texts = LOCALES[lang]
    builder = InlineKeyboardBuilder()
    builder.button(text=texts['btn_back'], callback_data="menu_main")
    await callback.message.edit_text(texts['help'], reply_markup=builder.as_markup(), parse_mode="Markdown")
    await callback.answer()


@router.message(Command("help"))
async def cmd_help(message: types.Message):
    settings = await get_user_settings(message.from_user.id)
    lang = settings.get("language", "en")
    await message.answer(LOCALES[lang]['help'], parse_mode="Markdown")


@router.message(Command("status"))
async def cmd_status(message: types.Message):
    settings = await get_user_settings(message.from_user.id)
    lang = settings.get("language", "en")
    texts = LOCALES[lang]
    ai_s    = texts['configured'] if settings.get("ai_api_key") else texts['using_default']
    db_s    = texts['configured'] if settings.get("db_provider") else texts['using_default']
    host_s  = texts['configured'] if settings.get("hosting_token") else texts['using_default']
    await message.answer(texts['ping_status'].format(ai=ai_s, db=db_s, hosting=host_s), parse_mode="Markdown")


@router.message(Command("deploy"))
async def cmd_deploy(message: types.Message):
    settings = await get_user_settings(message.from_user.id)
    lang = settings.get("language", "en")
    await message.answer(LOCALES[lang]['send_file'], parse_mode="Markdown")


@router.message(Command("projects"))
async def cmd_projects(message: types.Message):
    from handlers.dashboard import show_projects_message
    await show_projects_message(message)
