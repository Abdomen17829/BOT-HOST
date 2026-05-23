from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from services.database import get_user_settings, update_user_settings
from services.dynamic_db import ping_database
from utils.locales import LOCALES

router = Router()


class SettingsForm(StatesGroup):
    waiting_ai_key    = State()
    waiting_ai_model  = State()
    waiting_db_creds  = State()
    waiting_host_token = State()


# ── Helper: build settings menu ──────────────────────────────────────────────
async def settings_keyboard(user_id: int, lang: str):
    texts  = LOCALES[lang]
    cfg    = await get_user_settings(user_id)
    auto   = cfg.get("auto_seo", True)
    seo_btn = texts['btn_seo_on'] if auto else texts['btn_seo_off']

    b = InlineKeyboardBuilder()
    b.button(text=texts['btn_ai'],          callback_data="cfg_ai")
    b.button(text=texts['btn_hosting'],     callback_data="cfg_hosting")
    b.button(text=texts['btn_db'],          callback_data="cfg_db")
    b.button(text=texts['btn_lang'],        callback_data="cfg_lang")
    b.button(text=seo_btn,                  callback_data="cfg_toggle_seo")
    b.button(text=texts['btn_ping'],        callback_data="cfg_ping")
    b.button(text=texts['btn_delete_data'], callback_data="cfg_delete_data")
    b.button(text=texts['btn_back'],        callback_data="menu_main")
    b.adjust(2, 2, 1, 1, 1, 1)
    return b.as_markup()


@router.callback_query(F.data == "menu_settings")
async def open_settings(callback: types.CallbackQuery):
    settings = await get_user_settings(callback.from_user.id)
    lang = settings.get("language", "en")
    texts = LOCALES[lang]
    kb = await settings_keyboard(callback.from_user.id, lang)
    await callback.message.edit_text(texts['settings'], reply_markup=kb, parse_mode="Markdown")
    await callback.answer()


# ── Language ─────────────────────────────────────────────────────────────────
@router.callback_query(F.data == "cfg_lang")
async def choose_lang(callback: types.CallbackQuery):
    b = InlineKeyboardBuilder()
    b.button(text="English 🇬🇧", callback_data="setlang_en")
    b.button(text="العربية 🇸🇦", callback_data="setlang_ar")
    b.adjust(2)
    await callback.message.edit_text("🌐 Choose language / اختر اللغة:", reply_markup=b.as_markup())
    await callback.answer()


# ── SEO Toggle ────────────────────────────────────────────────────────────────
@router.callback_query(F.data == "cfg_toggle_seo")
async def toggle_seo(callback: types.CallbackQuery):
    settings = await get_user_settings(callback.from_user.id)
    lang = settings.get("language", "en")
    current = settings.get("auto_seo", True)
    await update_user_settings(callback.from_user.id, {"auto_seo": not current})
    kb = await settings_keyboard(callback.from_user.id, lang)
    await callback.message.edit_reply_markup(reply_markup=kb)
    await callback.answer("✅" if not current else "🔴")


# ── AI Config ─────────────────────────────────────────────────────────────────
@router.callback_query(F.data == "cfg_ai")
async def cfg_ai(callback: types.CallbackQuery, state: FSMContext):
    settings = await get_user_settings(callback.from_user.id)
    lang = settings.get("language", "en")
    texts = LOCALES[lang]
    await state.update_data(lang=lang)
    await state.set_state(SettingsForm.waiting_ai_key)
    b = InlineKeyboardBuilder()
    b.button(text=LOCALES[lang]['btn_back'], callback_data="menu_settings")
    await callback.message.edit_text(texts['ask_ai_key'], reply_markup=b.as_markup(), parse_mode="Markdown")
    await callback.answer()


@router.message(SettingsForm.waiting_ai_key)
async def process_ai_key(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "en")
    texts = LOCALES[lang]
    api_key = message.text.strip()

    msg = await message.answer(texts['checking_ai'])
    try:
        from services.ai_factory import detect_provider_and_fetch_models
        provider, models = await detect_provider_and_fetch_models(api_key)
        await state.update_data(ai_key=api_key, ai_provider=provider)

        b = InlineKeyboardBuilder()
        for m in models[:10]:
            b.button(text=m, callback_data=f"aimodel_{m}")
        b.adjust(1)
        await msg.edit_text(
            texts['ai_detected'].format(provider=provider),
            reply_markup=b.as_markup(),
            parse_mode="Markdown"
        )
    except Exception:
        await msg.edit_text(texts['ai_key_invalid'])
        await state.clear()


@router.callback_query(F.data.startswith("aimodel_"))
async def process_ai_model(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "en")
    texts = LOCALES[lang]
    model = callback.data.replace("aimodel_", "")
    await update_user_settings(callback.from_user.id, {
        "ai_provider":  data.get("ai_provider"),
        "ai_api_key":   data.get("ai_key", ""),
        "ai_model":     model,
    })
    await state.clear()
    await callback.message.edit_text(
        texts['ai_saved'].format(provider=data.get("ai_provider"), model=model),
        parse_mode="Markdown"
    )
    await callback.answer()


# ── DB Config ─────────────────────────────────────────────────────────────────
@router.callback_query(F.data == "cfg_db")
async def cfg_db(callback: types.CallbackQuery):
    settings = await get_user_settings(callback.from_user.id)
    lang = settings.get("language", "en")
    texts = LOCALES[lang]
    b = InlineKeyboardBuilder()
    b.button(text=texts['btn_supabase'], callback_data="dbprov_Supabase")
    b.button(text=texts['btn_mongodb'],  callback_data="dbprov_MongoDB")
    b.button(text=texts['btn_firebase'], callback_data="dbprov_Firebase")
    b.button(text=texts['btn_skip_db'],  callback_data="menu_settings")
    b.adjust(1)
    await callback.message.edit_text(texts['choose_db'], reply_markup=b.as_markup(), parse_mode="Markdown")
    await callback.answer()


@router.callback_query(F.data.startswith("dbprov_"))
async def pick_db_provider(callback: types.CallbackQuery, state: FSMContext):
    settings = await get_user_settings(callback.from_user.id)
    lang = settings.get("language", "en")
    texts = LOCALES[lang]
    provider = callback.data.replace("dbprov_", "")
    await state.update_data(db_provider=provider, lang=lang)
    await state.set_state(SettingsForm.waiting_db_creds)
    b = InlineKeyboardBuilder()
    b.button(text=texts['btn_back'], callback_data="cfg_db")
    await callback.message.edit_text(
        texts['ask_db_creds'].format(provider=provider),
        reply_markup=b.as_markup(),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.message(SettingsForm.waiting_db_creds)
async def process_db_creds(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "en")
    texts = LOCALES[lang]
    provider = data.get("db_provider")
    creds_raw = message.text.strip()
    msg = await message.answer(texts['testing_db'])
    try:
        ok = await ping_database(provider, creds_raw)
        if ok:
            await update_user_settings(message.from_user.id, {
                "db_provider":    provider,
                "db_credentials": creds_raw,
            })
            await msg.edit_text(texts['db_ping_success'].format(provider=provider), parse_mode="Markdown")
        else:
            await msg.edit_text(texts['db_ping_failed'])
    except Exception as e:
        await msg.edit_text(texts['error_parsing_creds'].format(error=str(e)), parse_mode="Markdown")
    finally:
        await state.clear()


# ── Hosting Config ────────────────────────────────────────────────────────────
@router.callback_query(F.data == "cfg_hosting")
async def cfg_hosting(callback: types.CallbackQuery):
    settings = await get_user_settings(callback.from_user.id)
    lang = settings.get("language", "en")
    texts = LOCALES[lang]
    b = InlineKeyboardBuilder()
    b.button(text=texts['btn_netlify'],      callback_data="hostprov_Netlify")
    b.button(text=texts['btn_vercel'],       callback_data="hostprov_Vercel")
    b.button(text=texts['btn_skip_hosting'], callback_data="menu_settings")
    b.adjust(2, 1)
    await callback.message.edit_text(texts['choose_hosting'], reply_markup=b.as_markup(), parse_mode="Markdown")
    await callback.answer()


@router.callback_query(F.data.startswith("hostprov_"))
async def pick_host_provider(callback: types.CallbackQuery, state: FSMContext):
    settings = await get_user_settings(callback.from_user.id)
    lang = settings.get("language", "en")
    texts = LOCALES[lang]
    provider = callback.data.replace("hostprov_", "")
    await state.update_data(host_provider=provider, lang=lang)
    await state.set_state(SettingsForm.waiting_host_token)
    b = InlineKeyboardBuilder()
    b.button(text=texts['btn_back'], callback_data="cfg_hosting")
    await callback.message.edit_text(
        texts['ask_hosting_token'].format(provider=provider),
        reply_markup=b.as_markup(),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.message(SettingsForm.waiting_host_token)
async def process_host_token(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "en")
    texts = LOCALES[lang]
    provider = data.get("host_provider")
    await update_user_settings(message.from_user.id, {
        "hosting_provider": provider,
        "hosting_token":    message.text.strip(),
    })
    await state.clear()
    await message.answer(texts['hosting_saved'].format(provider=provider), parse_mode="Markdown")


# ── Ping Status ───────────────────────────────────────────────────────────────
@router.callback_query(F.data == "cfg_ping")
async def cfg_ping(callback: types.CallbackQuery):
    settings = await get_user_settings(callback.from_user.id)
    lang = settings.get("language", "en")
    texts = LOCALES[lang]
    ai_s   = texts['configured'] if settings.get("ai_api_key") else texts['using_default']
    db_s   = texts['configured'] if settings.get("db_provider") else texts['using_default']
    host_s = texts['configured'] if settings.get("hosting_token") else texts['using_default']
    b = InlineKeyboardBuilder()
    b.button(text=texts['btn_back'], callback_data="menu_settings")
    await callback.message.edit_text(
        texts['ping_status'].format(ai=ai_s, db=db_s, hosting=host_s),
        reply_markup=b.as_markup(),
        parse_mode="Markdown"
    )
    await callback.answer()


# ── Delete Data ───────────────────────────────────────────────────────────────
@router.callback_query(F.data == "cfg_delete_data")
async def confirm_delete(callback: types.CallbackQuery):
    settings = await get_user_settings(callback.from_user.id)
    lang = settings.get("language", "en")
    texts = LOCALES[lang]
    b = InlineKeyboardBuilder()
    b.button(text=texts['btn_confirm_yes'], callback_data="cfg_delete_confirmed")
    b.button(text=texts['btn_confirm_no'],  callback_data="menu_settings")
    b.adjust(1)
    await callback.message.edit_text(texts['confirm_delete_data'], reply_markup=b.as_markup())
    await callback.answer()


@router.callback_query(F.data == "cfg_delete_confirmed")
async def do_delete(callback: types.CallbackQuery):
    settings = await get_user_settings(callback.from_user.id)
    lang = settings.get("language", "en")
    texts = LOCALES[lang]
    await update_user_settings(callback.from_user.id, {
        "ai_provider": None, "ai_api_key": None, "ai_model": None,
        "db_provider": None, "db_credentials": None,
        "hosting_provider": None, "hosting_token": None,
    })
    b = InlineKeyboardBuilder()
    b.button(text=texts['btn_back'], callback_data="menu_main")
    await callback.message.edit_text(texts['data_deleted'], reply_markup=b.as_markup())
    await callback.answer()
