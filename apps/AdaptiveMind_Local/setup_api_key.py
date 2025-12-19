#!/usr/bin/env python3

# AdaptiveMind Framework
# Copyright (c) 2025 Jimmy De Jesus
# Licensed under CC-BY 4.0
#
# AdaptiveMind - Intelligent AI Routing & Context Engine
# More info: https://github.com/[username]/adaptivemind
# License: https://creativecommons.org/licenses/by/4.0/



"""Utility script to set the OpenAI API key for AdaptiveMind AI."""
from .tools.key_manager import save_api_key


def main():

    api_key = input("Enter your OpenAI API key: ").strip()

    if not api_key:
        return

    if not api_key.startswith("sk-"):
        confirm = input("Continue anyway? (y/N): ").strip().lower()
        if confirm != 'y':
            return

    success = save_api_key(api_key)
    if success:
        pass
    else:
        pass

if __name__ == "__main__":
    main()
