import argparse

import uvicorn

from api import api
from config import AppConfig

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Main')
    parser.add_argument('--env_path', type=str, default="./envs/.env")
    parser.add_argument('--logger_save_path', type=str, default=".")
    parser.add_argument('--prompts_config_path', type=str, default="./analysis/prompts/data.yaml")

    args = parser.parse_args()
    app_config = AppConfig(args.env_path, args.logger_save_path, args.prompts_config_path)

    uvicorn.run(api.app, host="0.0.0.0", port=app_config.port)
