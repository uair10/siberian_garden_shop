 .ONESHELL:

python := python3

package_dir := seeds_shop

code_dir := $(package_dir)


define setup_env
    $(eval ENV_FILE := $(1))
    @echo " - setup env $(ENV_FILE)"
    $(eval include $(1))
    $(eval export)
endef

.PHONY: reformat
reformat:
	black $(package_dir)
	isort $(package_dir) --profile black --filter-files

.PHONY: dev-bot
dev-bot:
	$(call setup_env, .env)
	python3 -Om seeds_shop.tg_bot

.PHONY: dev-admin
dev-admin:
	$(call setup_env, .env)
	gunicorn seeds_shop.admin_panel.wsgi:app --workers=4 --threads=4 -b 0.0.0.0:5000

.PHONY: dev-api
dev-api:
	$(call setup_env, .env)
	python3 -Om seeds_shop.api

.PHONY: dev-worker
dev-worker:
	$(call setup_env, .env)
	python3 -Om seeds_shop.worker
