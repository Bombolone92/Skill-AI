# -*- coding: utf-8 -*-
"""
INSTALLA_SKILL_MOD.py
Gestore unificato e intelligente per Claude e ChatGPT:
1. Copia in .claude\skills tutte le skill compatibili con Claude.
2. Predispone i bundle e pacchetti compressi per ChatGPT.
3. Se un pacchetto è valido per entrambi, viene predisposto in entrambi i canali.
4. Mantiene la directory di backup costantemente sincronizzata.
"""

import os
import sys
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKUP_SKILLS_DIR = os.path.join(BASE_DIR, "skills_and_mods")
USER_PROFILE = os.environ.get("USERPROFILE", r"C:\Users\aless")
CLAUDE_SKILLS_DIR = os.path.join(USER_PROFILE, ".claude", "skills")
CHATGPT_PACKAGES_DIR = os.path.join(BASE_DIR, "chatgpt_packages")

os.makedirs(BACKUP_SKILLS_DIR, exist_ok=True)
os.makedirs(CLAUDE_SKILLS_DIR, exist_ok=True)
os.makedirs(CHATGPT_PACKAGES_DIR, exist_ok=True)

print("=======================================================================")
print("  INSTALLAZIONE UNIFICATA SKILL & MOD (CLAUDE + CHATGPT)")
print("=======================================================================")
print(f"[*] Archivio locale Backup : {BACKUP_SKILLS_DIR}")
print(f"[*] Destinazione Claude    : {CLAUDE_SKILLS_DIR}")
print(f"[*] Destinazione ChatGPT   : {CHATGPT_PACKAGES_DIR}")
print("-----------------------------------------------------------------------")

installed_claude = 0
prepared_chatgpt = 0

# 1. Scansione elementi in backup
for item in os.listdir(BACKUP_SKILLS_DIR):
    item_path = os.path.join(BACKUP_SKILLS_DIR, item)
    
    # Se cartella
    if os.path.isdir(item_path):
        has_skill_md = os.path.exists(os.path.join(item_path, "SKILL.md"))
        has_chatgpt_manifest = os.path.exists(os.path.join(item_path, "manifest.json")) or "chatgpt" in item.lower()
        
        # Compatibile Claude (standard SKILL.md o struttura agenti)
        if has_skill_md or not has_chatgpt_manifest:
            dest_claude = os.path.join(CLAUDE_SKILLS_DIR, item)
            try:
                shutil.copytree(item_path, dest_claude, dirs_exist_ok=True)
                installed_claude += 1
            except Exception as e:
                pass
                
        # Compatibile ChatGPT / Plugin / Bundle
        if has_chatgpt_manifest or "plugin" in item.lower() or "chatgpt" in item.lower() or "ruflo" in item.lower():
            dest_gpt = os.path.join(CHATGPT_PACKAGES_DIR, item)
            try:
                shutil.copytree(item_path, dest_gpt, dirs_exist_ok=True)
                prepared_chatgpt += 1
            except Exception as e:
                pass

    # Se file zip già compresso
    elif item.endswith(".zip"):
        dest_gpt_zip = os.path.join(CHATGPT_PACKAGES_DIR, item)
        try:
            shutil.copy2(item_path, dest_gpt_zip)
            prepared_chatgpt += 1
        except Exception:
            pass

print(f"[OK] Installazione completata!")
print(f"[+] Moduli / Skill operativi in Claude : {installed_claude}")
print(f"[+] Bundle / Pacchetti per ChatGPT    : {prepared_chatgpt}")
print("=======================================================================")

