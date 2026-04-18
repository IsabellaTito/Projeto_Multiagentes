#!/bin/bash
uv sync --all-groups

if [ ! -f .env ]; then
    cp .env.example .env
    echo ".env created from .env.example"
else
    echo ".env already exists, skipping copy"
fi