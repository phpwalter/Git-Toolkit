import os
import yaml
from ruamel.yaml import YAML
from pathlib import Path

# Config paths
SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent.parent
LANG_YAML = SCRIPT_DIR / "lang.yml"
DOCS_DIR = REPO_ROOT / "docs"
MKDOCS_YML = REPO_ROOT / "mkdocs.yml"
REQUIREMENTS = REPO_ROOT / "requirements.txt"
REQUIRED_I18N_PLUGINS = ["mkdocs-static-i18n"]

def load_languages(config_path):
    with open(config_path, 'r', encoding='utf-8') as f:
        cfg = yaml.safe_load(f)
    source = cfg['source']
    targets = cfg['targets']
    return source, targets

def ensure_structure(source, target):
    for root, dirs, files in os.walk(source):
        rel_root = os.path.relpath(root, source)
        target_root = os.path.join(target, rel_root) if rel_root != '.' else target

        if not os.path.exists(target_root):
            os.makedirs(target_root)
            print(f"Created directory: {target_root}")

        for file in files:
            if file.endswith('.md'):
                target_file = os.path.join(target_root, file)
                if not os.path.exists(target_file):
                    with open(target_file, 'w', encoding='utf-8') as f:
                        f.write(f'<!-- TODO: Translate this file from {os.path.relpath(os.path.join(root, file), source)} -->\n')
                    print(f"Created placeholder: {target_file}")

    # Warn about extra files
    for root, dirs, files in os.walk(target):
        rel_root = os.path.relpath(root, target)
        source_root = os.path.join(source, rel_root) if rel_root != '.' else source
        for file in files:
            if file.endswith('.md'):
                if not os.path.exists(os.path.join(source_root, file)):
                    print(f"WARNING: Extra file in {target}: {os.path.join(root, file)}")

def sync_mkdocs_languages(source_lang, target_langs):
    yaml_rt = YAML()
    yaml_rt.preserve_quotes = True
    if not MKDOCS_YML.exists():
        print(f"[ERROR] mkdocs.yml not found at {MKDOCS_YML}")
        return
    with open(MKDOCS_YML, "r", encoding="utf-8") as f:
        data = yaml_rt.load(f)

    updated = False

    # Find i18n plugin config
    plugins = data.get("plugins", [])
    i18n_config = None
    for p in plugins:
        if isinstance(p, dict) and "i18n" in p:
            i18n_config = p["i18n"]
            break
    if not i18n_config:
        print("[ERROR] No 'i18n' plugin block found in mkdocs.yml plugins.")
        return

    # Sync language list
    all_langs = [source_lang] + target_langs
    if i18n_config.get("languages") != all_langs:
        i18n_config["languages"] = all_langs
        print(f"[INFO] Updated 'languages:' in i18n plugin: {all_langs}")
        updated = True

    # Sync nav_translations blocks
    nav_trans = i18n_config.setdefault("nav_translations", {})
    eng_nav = nav_trans.get(source_lang)
    if not eng_nav:
        print(f"[WARNING] No English nav_translations present. Using empty stub.")
        eng_nav = {}

    for lang in target_langs:
        if lang not in nav_trans:
            nav_trans[lang] = {k: v for k, v in eng_nav.items()}
            print(f"[INFO] Created stub nav_translations for: {lang}")
            updated = True
        else:
            # Optionally sync missing keys from English
            missing = set(eng_nav) - set(nav_trans[lang])
            for k in missing:
                nav_trans[lang][k] = eng_nav[k]
                print(f"[INFO] Added missing nav key '{k}' to {lang} nav_translations")
                updated = True

    # Save if any updates
    if updated:
        with open(MKDOCS_YML, "w", encoding="utf-8") as f:
            yaml_rt.dump(data, f)
        print("[INFO] mkdocs.yml updated and saved.")
    else:
        print("[INFO] mkdocs.yml already up to date.")

def check_requirements_txt():
    if not REQUIREMENTS.exists():
        print(f"[WARNING] requirements.txt not found at {REQUIREMENTS}")
        return
    with open(REQUIREMENTS, "r", encoding="utf-8") as f:
        content = f.read()
    missing = [pkg for pkg in REQUIRED_I18N_PLUGINS if pkg not in content]
    if missing:
        print(f"[WARNING] Required i18n plugin(s) missing from requirements.txt: {', '.join(missing)}")
        print("         Please add them to ensure full language support.")
    else:
        print("[INFO] requirements.txt includes all required i18n plugins.")

def main():
    if not LANG_YAML.exists():
        print(f"[ERROR] lang.yml not found at {LANG_YAML}")
        return

    source_lang, target_langs = load_languages(LANG_YAML)

    # Ensure docs structure
    source_path = DOCS_DIR / source_lang
    if not source_path.is_dir():
        print(f"[ERROR] Source docs directory does not exist: {source_path}")
        return

    for lang in target_langs:
        target_path = DOCS_DIR / lang
        print(f"\n--- Syncing: {source_lang} → {lang} ---")
        ensure_structure(str(source_path), str(target_path))

    # Sync mkdocs.yml languages and navigation
    sync_mkdocs_languages(source_lang, target_langs)

    # Check requirements.txt
    check_requirements_txt()

    print("\nStructure and i18n config parity check complete.")

if __name__ == "__main__":
    main()
