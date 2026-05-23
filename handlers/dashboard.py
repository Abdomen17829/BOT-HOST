from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from services.database import get_user_settings, get_user_projects
from utils.locales import LOCALES

router = Router()


def back_keyboard(lang: str):
    texts = LOCALES[lang]
    b = InlineKeyboardBuilder()
    b.button(text=texts['btn_back'], callback_data="menu_main")
    return b.as_markup()


async def show_projects_message(message: types.Message):
    settings = await get_user_settings(message.from_user.id)
    lang = settings.get("language", "en")
    texts = LOCALES[lang]
    projects = await get_user_projects(message.from_user.id)
    if not projects:
        await message.answer(texts['no_projects'], parse_mode="Markdown")
        return
    header = texts['project_list'].format(count=len(projects))
    lines = [header]
    for p in projects:
        date_str = str(p.get('created_at', ''))[:10]
        lines.append(texts['project_item'].format(
            name=p.get('project_name', ''),
            url=p.get('live_url', ''),
            score=p.get('seo_score', 0),
            date=date_str
        ))
    await message.answer("\n\n".join(lines), parse_mode="Markdown", disable_web_page_preview=True)


@router.callback_query(F.data == "menu_projects")
async def show_projects(callback: types.CallbackQuery):
    settings = await get_user_settings(callback.from_user.id)
    lang = settings.get("language", "en")
    texts = LOCALES[lang]
    projects = await get_user_projects(callback.from_user.id)

    if not projects:
        builder = InlineKeyboardBuilder()
        builder.button(text=texts['btn_deploy_new'], callback_data="menu_deploy")
        builder.button(text=texts['btn_back'], callback_data="menu_main")
        builder.adjust(1)
        await callback.message.edit_text(texts['no_projects'], reply_markup=builder.as_markup(), parse_mode="Markdown")
        await callback.answer()
        return

    header = texts['project_list'].format(count=len(projects))
    lines = [header]
    for p in projects:
        date_str = str(p.get('created_at', ''))[:10]
        lines.append(texts['project_item'].format(
            name=p.get('project_name', ''),
            url=p.get('live_url', ''),
            score=p.get('seo_score', 0),
            date=date_str
        ))

    builder = InlineKeyboardBuilder()
    builder.button(text=texts['btn_deploy_new'], callback_data="menu_deploy")
    builder.button(text=texts['btn_back'], callback_data="menu_main")
    builder.adjust(1)

    await callback.message.edit_text(
        "\n\n".join(lines),
        reply_markup=builder.as_markup(),
        parse_mode="Markdown",
        disable_web_page_preview=True
    )
    await callback.answer()


@router.callback_query(F.data == "menu_deploy")
async def deploy_prompt(callback: types.CallbackQuery):
    settings = await get_user_settings(callback.from_user.id)
    lang = settings.get("language", "en")
    texts = LOCALES[lang]
    builder = InlineKeyboardBuilder()
    builder.button(text=texts['btn_back'], callback_data="menu_main")
    await callback.message.edit_text(texts['send_file'], reply_markup=builder.as_markup(), parse_mode="Markdown")
    await callback.answer()
