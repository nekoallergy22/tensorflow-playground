import yaml
from pathlib import Path

def load_config():
    # スクリプトのディレクトリを基準にする
    script_dir = Path(__file__).parent
    config_path = script_dir / 'config.yml'
    
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    
    # プロジェクトルートディレクトリを基準にパスを設定
    project_root = script_dir.parent
    config['LOG_DIR'] = project_root / config['LOG_DIR']
    
    return config

# 設定を読み込む
config = load_config()

# グローバル変数として設定
LOG_DIR = config['LOG_DIR']
